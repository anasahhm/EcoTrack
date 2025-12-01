from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.impact import ImpactInput, ImpactResponse, ImpactHistory
from app.auth.dependencies import get_current_user
from app.database import get_database
from app.utils.calculations import (
    calculate_carbon_footprint,
    calculate_water_score,
    calculate_energy_score,
    calculate_waste_score,
    get_overall_rating,
)
from app.utils.ai_service import generate_ai_tips, generate_ai_analysis  # NEW
from datetime import datetime
from bson import ObjectId
from typing import List
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/calculate", response_model=ImpactResponse, status_code=status.HTTP_201_CREATED)
async def calculate_impact(
    impact_data: ImpactInput,
    current_user: dict = Depends(get_current_user)
):
    # Calculate scores
    carbon_score = calculate_carbon_footprint(
        impact_data.transport_method,
        impact_data.transport_km,
        impact_data.electricity_kwh,
        impact_data.diet_type,
        impact_data.waste_kg
    )
    
    water_score = calculate_water_score(
        impact_data.water_liters,
        impact_data.diet_type
    )
    
    energy_score = calculate_energy_score(
        impact_data.electricity_kwh,
        impact_data.transport_km
    )
    
    waste_score = calculate_waste_score(impact_data.waste_kg)
    
    overall_rating = get_overall_rating(carbon_score)
    
    # UPDATED: Use AI-powered tips
    tips = generate_ai_tips(
        impact_data.transport_method,
        impact_data.transport_km,
        impact_data.electricity_kwh,
        impact_data.water_liters,
        impact_data.diet_type,
        impact_data.waste_kg,
        carbon_score,
        overall_rating
    )
    
    # NEW: Generate AI analysis
    ai_analysis = generate_ai_analysis(
        carbon_score,
        water_score,
        energy_score,
        waste_score,
        overall_rating,
        impact_data.transport_method,
        impact_data.diet_type
    )
    
    # Save to database
    db = await get_database()
    
    impact_log = {
        "user_id": current_user["id"],
        "transport_method": impact_data.transport_method,
        "transport_km": impact_data.transport_km,
        "electricity_kwh": impact_data.electricity_kwh,
        "water_liters": impact_data.water_liters,
        "diet_type": impact_data.diet_type,
        "waste_kg": impact_data.waste_kg,
        "carbon_score": carbon_score,
        "water_score": water_score,
        "energy_score": energy_score,
        "waste_score": waste_score,
        "overall_rating": overall_rating,
        "tips": tips,
        "ai_analysis": ai_analysis,  # NEW
        "created_at": datetime.utcnow()
    }
    
    result = await db.impact_logs.insert_one(impact_log)
    
    return ImpactResponse(
        id=str(result.inserted_id),
        carbon_score=carbon_score,
        water_score=water_score,
        energy_score=energy_score,
        waste_score=waste_score,
        overall_rating=overall_rating,
        tips=tips,
        ai_analysis=ai_analysis,  # NEW
        created_at=impact_log["created_at"]
    )

@router.get("/history", response_model=ImpactHistory)
async def get_impact_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    db = await get_database()
    
    # Count total documents
    total = await db.impact_logs.count_documents({"user_id": current_user["id"]})
    
    # Fetch paginated data
    skip = (page - 1) * page_size
    cursor = db.impact_logs.find({"user_id": current_user["id"]}) \
        .sort("created_at", -1) \
        .skip(skip) \
        .limit(page_size)
    
    logs = await cursor.to_list(length=page_size)
    
    data = [
        ImpactResponse(
            id=str(log["_id"]),
            carbon_score=log["carbon_score"],
            water_score=log["water_score"],
            energy_score=log["energy_score"],
            waste_score=log["waste_score"],
            overall_rating=log["overall_rating"],
            tips=log["tips"],
            created_at=log["created_at"]
        )
        for log in logs
    ]
    
    return ImpactHistory(
        total=total,
        page=page,
        page_size=page_size,
        data=data
    )
@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(
    chat_request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    from app.utils.ai_service import chat_with_ai
    
    db = await get_database()
    
    # Get user's latest impact data for context
    latest_log = await db.impact_logs.find_one(
        {"user_id": current_user["id"]},
        sort=[("created_at", -1)]
    )
    
    context = None
    if latest_log:
        context = {
            "carbon_score": latest_log.get("carbon_score"),
            "overall_rating": latest_log.get("overall_rating"),
            "transport_method": latest_log.get("transport_method"),
            "diet_type": latest_log.get("diet_type")
        }
    
    response = chat_with_ai(chat_request.message, context)
    
    return ChatResponse(response=response)