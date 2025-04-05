"""Example script demonstrating the Gemini agent with various tools for travel and scheduling assistance."""

import asyncio

from src.agent import Agent


def get_current_weather(location: str) -> dict:
    """Gets the current weather for a given location.

    Args:
        location: The city name (e.g., "New York")

    Returns:
        dict: Weather data including temperature, unit, and conditions
    """
    if "new york" in location.lower():
        return {"temperature": 22, "unit": "Celsius", "conditions": "Partly Cloudy"}
    elif "london" in location.lower():
        return {"temperature": 15, "unit": "Celsius", "conditions": "Rainy"}
    else:
        return {"temperature": 25, "unit": "Celsius", "conditions": "Sunny"}


def query_calendar(date: str = "today") -> dict:
    """Retrieves user's calendar appointments for a specific date.

    Args:
        date: Date to query, can be "today", "tomorrow", or a specific date
              (e.g., "2023-06-15"). Defaults to "today".

    Returns:
        dict: Collection of appointments with their details
    """
    if date == "today":
        return {
            "appointments": [
                {"id": 101, "time": "09:00-10:30", "title": "Weekly Team Meeting"},
                {"id": 102, "time": "13:00-14:00", "title": "Lunch with Client"},
                {"id": 103, "time": "16:00-17:00", "title": "Project Review"},
            ],
            "date": date,
        }
    elif date in ["tomorrow", "2023-06-15"]:
        return {
            "appointments": [
                {"id": 104, "time": "11:00-12:00", "title": "Dentist Appointment"},
                {"id": 105, "time": "15:00-16:30", "title": "Budget Planning"},
            ],
            "date": date,
        }
    else:
        return {"appointments": [], "date": date}


def cancel_appointment(appointment_id: int) -> dict:
    """Cancels a specific calendar appointment.

    Args:
        appointment_id: The unique identifier of the appointment to cancel

    Returns:
        dict: Operation status and message
    """
    valid_ids = [101, 102, 103, 104, 105]
    if appointment_id in valid_ids:
        return {"status": "success", "message": f"Appointment {appointment_id} canceled successfully"}
    else:
        return {"status": "error", "message": f"Appointment {appointment_id} not found"}


def get_flight_options(origin: str, destination: str, date: str) -> dict:
    """Retrieves available flight options between locations.

    Args:
        origin: Departure city (e.g., "San Francisco")
        destination: Arrival city (e.g., "New York")
        date: Travel date (e.g., "today", "2023-06-15")

    Returns:
        dict: Available flight options with details
    """
    flights = []

    if "san francisco" in origin.lower() and "new york" in destination.lower():
        flights = [
            {
                "flight_number": "AA123",
                "origin": "SFO",
                "destination": "JFK",
                "departure": "08:00",
                "arrival": "11:30",
                "price": 349.99,
                "airline": "American Airlines",
            },
            {
                "flight_number": "DL456",
                "origin": "SFO",
                "destination": "LGA",
                "departure": "10:15",
                "arrival": "13:45",
                "price": 425.50,
                "airline": "Delta",
            },
            {
                "flight_number": "UA789",
                "origin": "SFO",
                "destination": "EWR",
                "departure": "13:45",
                "arrival": "17:15",
                "price": 315.75,
                "airline": "United",
            },
        ]
    elif "new york" in origin.lower() and "san francisco" in destination.lower():
        flights = [
            {
                "flight_number": "AA456",
                "origin": "JFK",
                "destination": "SFO",
                "departure": "09:00",
                "arrival": "12:30",
                "price": 379.99,
                "airline": "American Airlines",
            },
            {
                "flight_number": "DL789",
                "origin": "LGA",
                "destination": "SFO",
                "departure": "11:15",
                "arrival": "14:45",
                "price": 405.50,
                "airline": "Delta",
            },
            {
                "flight_number": "UA321",
                "origin": "EWR",
                "destination": "SFO",
                "departure": "14:45",
                "arrival": "18:15",
                "price": 335.75,
                "airline": "United",
            },
        ]
    elif "london" in origin.lower() and "new york" in destination.lower():
        flights = [
            {
                "flight_number": "BA101",
                "origin": "LHR",
                "destination": "JFK",
                "departure": "10:00",
                "arrival": "13:00",
                "price": 620.00,
                "airline": "British Airways",
            },
            {
                "flight_number": "VS201",
                "origin": "LHR",
                "destination": "JFK",
                "departure": "12:30",
                "arrival": "15:30",
                "price": 580.50,
                "airline": "Virgin Atlantic",
            },
        ]
    else:
        flights = [
            {
                "flight_number": "Generic",
                "origin": origin[:3].upper(),
                "destination": destination[:3].upper(),
                "departure": "09:00",
                "arrival": "11:00",
                "price": 350.00,
                "airline": "Generic Airlines",
            }
        ]

    return {"flights": flights, "origin": origin, "destination": destination, "date": date}


def query_sqlite_hotels(city: str, rating_min: str = None) -> dict:
    """Queries the hotel database for accommodations matching specific criteria.

    Args:
        city: Destination city (e.g., "New York")
        rating_min: Minimum rating value to filter hotels by (e.g., "4")

    Returns:
        dict: Matching hotels with details and counts
    """
    hotels_db = {
        "new york": [
            {
                "id": 1,
                "name": "The Grand Plaza",
                "chain": "Marriott",
                "brand": "JW Marriott",
                "rating": 4.7,
                "price_category": "luxury",
                "price_per_night": 450,
                "neighborhood": "Midtown",
                "amenities": ["spa", "pool", "restaurant"],
                "points_per_night": 50000,
                "loyalty_program": "Marriott Bonvoy",
            },
            {
                "id": 2,
                "name": "City Lights Hotel",
                "chain": "Hilton",
                "brand": "DoubleTree",
                "rating": 4.2,
                "price_category": "moderate",
                "price_per_night": 275,
                "neighborhood": "Times Square",
                "amenities": ["restaurant", "gym"],
                "points_per_night": 70000,
                "loyalty_program": "Hilton Honors",
            },
            {
                "id": 3,
                "name": "Riverside Inn",
                "chain": "IHG",
                "brand": "Holiday Inn",
                "rating": 4.5,
                "price_category": "moderate",
                "price_per_night": 320,
                "neighborhood": "Upper West Side",
                "amenities": ["restaurant", "laundry"],
                "points_per_night": 35000,
                "loyalty_program": "IHG Rewards",
            },
            {
                "id": 4,
                "name": "Budget Stay",
                "chain": "Independent",
                "rating": 3.8,
                "price_category": "budget",
                "price_per_night": 150,
                "neighborhood": "Queens",
                "amenities": ["free wifi", "breakfast"],
            },
            {
                "id": 5,
                "name": "Luxury Towers",
                "chain": "Marriott",
                "brand": "The Ritz-Carlton",
                "rating": 4.9,
                "price_category": "luxury",
                "price_per_night": 550,
                "neighborhood": "Financial District",
                "amenities": ["spa", "pool", "restaurant", "gym", "concierge"],
                "points_per_night": 85000,
                "loyalty_program": "Marriott Bonvoy",
            },
            {
                "id": 6,
                "name": "Hilton Midtown",
                "chain": "Hilton",
                "brand": "Hilton",
                "rating": 4.6,
                "price_category": "luxury",
                "price_per_night": 425,
                "neighborhood": "Midtown",
                "amenities": ["spa", "restaurant", "gym"],
                "points_per_night": 80000,
                "loyalty_program": "Hilton Honors",
            },
            {
                "id": 7,
                "name": "Kimpton Hotel",
                "chain": "IHG",
                "brand": "Kimpton",
                "rating": 4.4,
                "price_category": "moderate",
                "price_per_night": 310,
                "neighborhood": "Chelsea",
                "amenities": ["restaurant", "bar", "gym"],
                "points_per_night": 40000,
                "loyalty_program": "IHG Rewards",
            },
        ],
        "london": [
            {
                "id": 101,
                "name": "The Wellington",
                "chain": "Marriott",
                "brand": "Autograph Collection",
                "rating": 4.6,
                "price_category": "luxury",
                "price_per_night": 420,
                "amenities": ["spa", "restaurant"],
                "points_per_night": 60000,
                "loyalty_program": "Marriott Bonvoy",
            },
            {
                "id": 102,
                "name": "Covent Garden Hotel",
                "chain": "Hilton",
                "brand": "Conrad",
                "rating": 4.3,
                "price_category": "moderate",
                "price_per_night": 290,
                "amenities": ["gym", "restaurant"],
                "points_per_night": 65000,
                "loyalty_program": "Hilton Honors",
            },
        ],
    }

    if city.lower() not in hotels_db:
        return {"status": "error", "message": f"No hotel data available for {city}"}

    results = hotels_db[city.lower()]

    if rating_min is not None:
        min_rating = float(rating_min)
        results = [hotel for hotel in results if hotel["rating"] >= min_rating]

    return {"status": "success", "city": city, "hotels": results, "result_count": len(results)}


def query_loyalty_programs(destination: str | None = None) -> dict:
    """Retrieves user's loyalty program points and eligible travel discounts.

    Args:
        destination: Optional city to filter for location-specific deals

    Returns:
        dict: Available loyalty points, status levels, and special offers
    """
    user_programs = {
        "airline_points": {"Delta SkyMiles": 47500, "United MileagePlus": 32000, "American AAdvantage": 18750},
        "hotel_points": {"Marriott Bonvoy": 68000, "Hilton Honors": 125000, "IHG Rewards": 42000},
        "status_levels": {"Delta": "Gold", "Marriott": "Platinum", "Hertz": "President's Circle", "Chase": "Sapphire Reserve", "Amex": "Platinum"},
    }

    city_offers = {
        "new york": [
            {"partner": "MoMA", "discount": "20% off admission with Marriott Platinum status"},
            {"partner": "Bergdorf Goodman", "discount": "10% off purchases with Amex Platinum"},
            {"partner": "Citi Bike", "discount": "Free day pass with Delta Gold status"},
            {"partner": "Empire State Building", "discount": "Priority access and 15% off admission with Chase Sapphire Reserve"},
            {"partner": "Michelin Star Restaurants", "discount": "Priority reservations at selected restaurants with Amex Platinum"},
            {"partner": "Broadway Shows", "discount": "25% off select shows with Marriott Platinum status"},
            {"partner": "Metropolitan Museum of Art", "discount": "2-for-1 admission with United MileagePlus status"},
            {"partner": "Central Park Zoo", "discount": "15% off admission with IHG Rewards membership"},
            {"partner": "NYC Airport Express", "discount": "Free airport transfer with minimum 3-night Hilton stay"},
        ],
        "london": [
            {"partner": "Harrods", "discount": "VIP shopping experience with Marriott Platinum"},
            {"partner": "The Tube", "discount": "50% off 7-day travel card with British Airways Silver"},
        ],
    }

    result = {"loyalty_programs": user_programs, "point_redemption_opportunities": []}

    if destination and destination.lower() in city_offers:
        result["destination_offers"] = city_offers[destination.lower()]

    if destination and destination.lower() == "new york":
        result["point_redemption_opportunities"] = [
            {"program": "Marriott Bonvoy", "opportunity": "Free night at JW Marriott Essex House", "points_required": 50000, "cash_value": "$650"},
            {"program": "Delta SkyMiles", "opportunity": "Economy round-trip ticket (available for your dates)", "points_required": 25000, "cash_value": "$450"},
            {"program": "Hilton Honors", "opportunity": "Luxury weekend package: 1 night at Waldorf Astoria + spa treatment", "points_required": 95000, "cash_value": "$750"},
            {"program": "United MileagePlus", "opportunity": "VIP helicopter tour of Manhattan", "points_required": 20000, "cash_value": "$350"},
        ]

    return result


def main():
    """Run demo scenarios showcasing the Gemini agent with different tool combinations."""
    agent = Agent(
        model="gemini-2.0-flash-exp",
        system_instruction=(
            "You are a helpful travel and scheduling assistant. Be concise, informative, and focus on "
            "providing practical information. When giving recommendations, prioritize options that make "
            "the best use of the user's loyalty program points."
        ),
    )

    tools = [get_current_weather, query_calendar, cancel_appointment, get_flight_options, query_sqlite_hotels, query_loyalty_programs]

    for tool in tools:
        agent.add_tool(tool)

    print("\nDemo 1: Calendar Management and Weather")
    task1 = (
        "Could you help me with two things? First, I need to clear my schedule for today - "
        "please check my calendar for today's appointments and cancel all of them. "
        "After that, let me know what the current weather is like in New York City. "
        "Thanks!"
    )
    result1 = asyncio.run(agent.run(task1, enable_code_execution=True, enable_google_search=False))

    print("\n--- Demo 1 Results ---")
    print(result1)
    print("--------------------")

    print("\nDemo 2: Travel Booking Assistance with Loyalty Programs")
    task2 = (
        "I need your help with travel planning for a trip to New York today. First, check available flights from San Francisco to New York. "
        "Then find me some hotels in New York with at least 4-star ratings. "
        "Also check my loyalty program accounts to see what points I have available. "
        "Based on all this information, recommend the best flight and hotel options considering both price and my loyalty points."
    )
    result2 = asyncio.run(agent.run(task2, enable_code_execution=True, enable_google_search=False))

    print("\n--- Demo 2 Results ---")
    print(result2)
    print("--------------------")

    print("\nDemo 3: Attraction Planning with Google Search and Code Execution")
    task3 = (
        "Search Google for best attractions in New York City for a one-day visit. I'd like you to create an "
        "itinerary with 3-4 popular attractions arranged in a sensible order based on their locations. "
        "Please include the approximate costs for each place. Take into account the current weather in New York "
        "and mention any applicable loyalty program benefits for New York City or discounts I might be eligible for. "
        "Finally, wrap up with a brief summary of the day's plan."
    )
    result3 = asyncio.run(agent.run(task3, enable_code_execution=True, enable_google_search=True))

    print("\n--- Demo 3 Results ---")
    print(result3)
    print("--------------------")


if __name__ == "__main__":
    main()
