from typing import List, Tuple

# Emission factors (kg CO2 per unit)
CAR_EMISSION = {
    "car": 0.21,      # kg CO2 per km
    "bus": 0.08,      # kg CO2 per km
    "bike": 0,        # kg CO2 per km
    "walk": 0,        # kg CO2 per km
    "ev": 0.05        # kg CO2 per km
}

DIET_EMISSIONS = {
    "veg": 2.0,           # kg CO2 per day
    "mixed": 3.5,         # kg CO2 per day
    "heavy_meat": 7.0     # kg CO2 per day
}

ELECTRICITY_EMISSION = 0.5  # kg CO2 per kWh
WASTE_EMISSION = 0.4        # kg CO2 per kg

def calculate_carbon_footprint(
    transport_method: str,
    transport_km: float,
    electricity_kwh: float,
    diet_type: str,
    waste_kg: float
) -> float:
    """Calculate total carbon footprint in kg CO2"""
    transport_carbon = CAR_EMISSION.get(transport_method, 0.21) * transport_km
    electricity_carbon = electricity_kwh * ELECTRICITY_EMISSION
    diet_carbon = DIET_EMISSIONS.get(diet_type, 3.5)
    waste_carbon = waste_kg * WASTE_EMISSION
    
    total_carbon = transport_carbon + electricity_carbon + diet_carbon + waste_carbon
    return round(total_carbon, 2)

def calculate_water_score(water_liters: float, diet_type: str) -> float:
    """Calculate water footprint in liters"""
    diet_water = {
        "veg": 1500,
        "mixed": 3000,
        "heavy_meat": 5000
    }
    
    total_water = water_liters + diet_water.get(diet_type, 3000)
    return round(total_water, 2)

def calculate_energy_score(electricity_kwh: float, transport_km: float) -> float:
    """Calculate energy score"""
    energy_score = electricity_kwh + (transport_km * 0.5)
    return round(energy_score, 2)

def calculate_waste_score(waste_kg: float) -> float:
    """Calculate waste score"""
    return round(waste_kg, 2)

def get_overall_rating(carbon_score: float) -> str:
    """Determine overall environmental rating"""
    if carbon_score < 5:
        return "Excellent"
    elif carbon_score < 10:
        return "Good"
    elif carbon_score < 15:
        return "Moderate"
    elif carbon_score < 20:
        return "Poor"
    else:
        return "Critical"

def generate_tips(
    transport_method: str,
    transport_km: float,
    electricity_kwh: float,
    diet_type: str,
    waste_kg: float,
    carbon_score: float
) -> List[str]:
    """Generate personalized improvement tips"""
    tips = []
    
    # Transport tips
    if transport_method == "car" and transport_km > 20:
        tips.append("Consider using public transport or carpooling to reduce emissions")
    elif transport_method == "car":
        tips.append("Try cycling or walking for short distances under 5km")
    
    if transport_method not in ["bike", "walk", "ev"] and transport_km > 10:
        tips.append("Switch to electric vehicles or use public transport twice a week")
    
    # Electricity tips
    if electricity_kwh > 10:
        tips.append("Reduce electricity usage by turning off unused appliances")
        tips.append("Consider switching to LED bulbs and energy-efficient appliances")
    elif electricity_kwh > 5:
        tips.append("Unplug devices when not in use to save energy")
    
    # Diet tips
    if diet_type == "heavy_meat":
        tips.append("Reduce red meat consumption to 2-3 times per week")
        tips.append("Try incorporating more plant-based meals into your diet")
    elif diet_type == "mixed":
        tips.append("Consider having one meat-free day per week")
    
    # Waste tips
    if waste_kg > 2:
        tips.append("Increase recycling efforts and reduce single-use plastics")
        tips.append("Compost organic waste to reduce landfill contribution")
    elif waste_kg > 1:
        tips.append("Practice proper waste segregation for better recycling")
    
    # Overall tips
    if carbon_score > 15:
        tips.append("Your carbon footprint is high. Focus on sustainable transportation and energy use")
    
    # Default tip if no specific issues
    if not tips:
        tips.append("Great job! Maintain your eco-friendly habits")
        tips.append("Share your sustainable practices with friends and family")
    
    return tips[:5]  # Return max 5 tips