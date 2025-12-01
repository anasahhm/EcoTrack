import google.generativeai as genai
import os
from typing import List, Dict
import json

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_ai_enabled() -> bool:
    """Check if AI is enabled"""
    return bool(GEMINI_API_KEY)

def generate_ai_tips(
    transport_method: str,
    transport_km: float,
    electricity_kwh: float,
    water_liters: float,
    diet_type: str,
    waste_kg: float,
    carbon_score: float,
    overall_rating: str
) -> List[str]:
    """Generate personalized tips using Gemini AI"""
    
    if not get_ai_enabled():
        # Fallback to rule-based tips
        from app.utils.calculations import generate_tips
        return generate_tips(
            transport_method, transport_km, electricity_kwh,
            diet_type, waste_kg, carbon_score
        )
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""You are an environmental sustainability expert. Based on the following daily habits, provide exactly 5 personalized, actionable tips to reduce environmental impact.

User's Daily Habits:
- Transportation: {transport_method}, {transport_km} km traveled
- Electricity Usage: {electricity_kwh} kWh
- Water Usage: {water_liters} liters
- Diet Type: {diet_type}
- Waste Generated: {waste_kg} kg
- Carbon Footprint: {carbon_score} kg CO2
- Overall Rating: {overall_rating}

Requirements:
1. Provide exactly 5 specific, actionable tips
2. Prioritize tips based on their highest impact areas
3. Make tips practical and achievable
4. Include specific numbers where possible
5. Be encouraging and positive

Format: Return only a JSON array of 5 strings, nothing else.
Example: ["Tip 1", "Tip 2", "Tip 3", "Tip 4", "Tip 5"]"""

        response = model.generate_content(prompt)
        tips_text = response.text.strip()
        
        # Parse JSON response
        if tips_text.startswith('[') and tips_text.endswith(']'):
            tips = json.loads(tips_text)
            return tips[:5]  # Ensure max 5 tips
        else:
            # If not JSON, split by newlines
            tips = [tip.strip('- ').strip() for tip in tips_text.split('\n') if tip.strip()]
            return tips[:5]
    
    except Exception as e:
        print(f"AI tip generation failed: {e}")
        # Fallback to rule-based tips
        from app.utils.calculations import generate_tips
        return generate_tips(
            transport_method, transport_km, electricity_kwh,
            diet_type, waste_kg, carbon_score
        )

def generate_ai_analysis(
    carbon_score: float,
    water_score: float,
    energy_score: float,
    waste_score: float,
    overall_rating: str,
    transport_method: str,
    diet_type: str
) -> str:
    """Generate AI-powered environmental impact analysis"""
    
    if not get_ai_enabled():
        return f"Your environmental rating is {overall_rating}. Focus on reducing your carbon footprint through sustainable transportation and energy conservation."
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""You are an environmental data analyst. Provide a concise analysis (3-4 sentences) of this person's environmental impact:

Scores:
- Carbon Footprint: {carbon_score} kg CO2
- Water Usage: {water_score} liters
- Energy Score: {energy_score} kWh
- Waste: {waste_score} kg
- Overall Rating: {overall_rating}
- Main Transport: {transport_method}
- Diet: {diet_type}

Provide an insightful, data-driven analysis that:
1. Compares their impact to average benchmarks
2. Identifies their biggest impact areas
3. Highlights what they're doing well
4. Suggests the most impactful improvement area

Keep it concise, encouraging, and actionable."""

        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        print(f"AI analysis generation failed: {e}")
        return f"Your environmental rating is {overall_rating} with a carbon footprint of {carbon_score} kg CO2. Focus on your highest impact areas."

def generate_comparison_insight(user_carbon: float, avg_carbon: float = 12.0) -> str:
    """Generate AI comparison with average person"""
    
    if not get_ai_enabled():
        diff = user_carbon - avg_carbon
        if diff > 0:
            return f"Your carbon footprint is {abs(diff):.1f} kg CO2 higher than average."
        else:
            return f"Great job! Your carbon footprint is {abs(diff):.1f} kg CO2 lower than average."
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""Compare this person's carbon footprint to the average:
- Their carbon footprint: {user_carbon} kg CO2
- Average carbon footprint: {avg_carbon} kg CO2

Provide one encouraging sentence (max 20 words) about their comparison."""

        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        print(f"AI comparison failed: {e}")
        diff = user_carbon - avg_carbon
        return f"Your footprint differs by {abs(diff):.1f} kg CO2 from average."

def chat_with_ai(message: str, context: Dict = None) -> str:
    """AI chatbot for environmental questions"""
    
    if not get_ai_enabled():
        return "AI chatbot is not available. Please configure GEMINI_API_KEY."
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        context_str = ""
        if context:
            context_str = f"\n\nUser's Environmental Profile:\n{json.dumps(context, indent=2)}"
        
        prompt = f"""You are EcoBot, an expert environmental sustainability assistant for EcoTrack app. 
Answer the user's question in a helpful, concise way (2-3 sentences max).
{context_str}

User Question: {message}

Provide a helpful, actionable answer focused on environmental sustainability."""

        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        print(f"AI chat failed: {e}")
        return "I'm having trouble processing your question. Please try again."