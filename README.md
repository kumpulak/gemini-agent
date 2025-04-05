# Gemini Agent

Agent wrapper for Gemini using the v1alpha Live API.

## Installation

### Regular Installation

Install the package:

    pip install -e .

### Development Installation

Install with development dependencies:

    pip install -e ".[dev]"

## Usage

Run the example script:

    python example.py

## Features

- Function calling with automatic parsing of Python function signatures and docstrings.
- Support for built-in Google Search and Code Execution tools.

## Authentication

Set your Gemini API key in the `.env` file:

    GEMINI_API_KEY=your_api_key_here

## How It Works

The `Agent` wrapper uses the Google Generative AI Python SDK, specifically leveraging the `v1alpha` Live API (`google.genai.live`) for asynchronous interaction and tool handling:

1. Each task execution (`agent.run()`) initiates a connection using the Live API.
2. The agent parses your Python function signatures and docstrings to create tool declarations compatible with the Gemini API.
3. These declarations, along with requests to enable built-in tools (Code Execution, Google Search), are sent to the model.
4. When the model decides to use a tool, it sends a `ToolCall` back.
5. The `Agent` executes the corresponding Python function (or handles built-in tool calls) and sends the results back to the model using a `ToolResponse`.
6. The model incorporates the tool results and generates the final text response.

## Main Example Script

See the `example.py` file for a runnable example demonstrating various features of the `Agent` wrapper, including multiple tool calls and built-in tool usage. 

## Example Outputs

Below are example outputs from running the agent with different tasks, including the tool calls that were made during execution.

### Demo 1: Calendar Management and Weather

**Task:** 
> Could you help me with two things? First, I need to clear my schedule for today - please check my calendar for today's appointments and cancel all of them. After that, let me know what the current weather is like in New York City. Thanks!

**Response:**
> Tool: `query_calendar(date='today')`
>
> OK. It looks like you have three appointments today: "Weekly Team Meeting" at 09:00-10:30 (ID: 101), "Lunch with Client" at 13:00-14:00 (ID: 102), and "Project Review" at 16:00-17:00 (ID: 103). I will now cancel all of these.
>                                                        
> Tool: `cancel_appointment(appointment_id='101')`
>
> Tool: `cancel_appointment(appointment_id='102')`
>
> Tool: `cancel_appointment(appointment_id='103')`
>
> All your appointments for today have been canceled. Now, let me check the weather in New York City.
>
> Tool: `get_current_weather(location='New York City')`
>
> The current weather in New York City is partly cloudy with a temperature of 22 degrees Celsius.

### Demo 2: Travel Booking Assistance with Loyalty Programs

**Task:**
> I need your help with travel planning for a trip to New York today. First, check available flights from San Francisco to New York. Then find me some hotels in New York with at least 4-star ratings. Also check my loyalty program accounts to see what points I have available. Based on all this information, recommend the best flight and hotel options considering both price and my loyalty points.

**Response:**
> Tool: `get_flight_options(date='today', origin='San Francisco', destination='New York')`
>
> Tool: `query_sqlite_hotels(city='New York', rating_min='4')`
>
> Tool: `query_loyalty_programs(destination='New York')`
>
> Okay, here's a breakdown of your travel options and recommendations:
>
> **Flights:**
>
> * American Airlines (AA123): SFO to JFK, departs 8:00 AM, arrives 11:30 AM, $349.99.
> * Delta (DL456): SFO to LGA, departs 10:15 AM, arrives 1:45 PM, $425.50.
> * United (UA789): SFO to EWR, departs 1:45 PM, arrives 5:15 PM, $315.75
>
> **Hotels (4-star and above):**
>
> * The Grand Plaza (JW Marriott): 4.7 rating, Midtown, $450/night or 50,000 Marriott Bonvoy points.
> * City Lights Hotel (DoubleTree): 4.2 rating, Times Square, $275/night or 70,000 Hilton Honors points.
> * Riverside Inn (Holiday Inn): 4.5 rating, Upper West Side, $320/night or 35,000 IHG Rewards points.
> * Luxury Towers (Ritz-Carlton): 4.9 rating, Financial District, $550/night or 85,000 Marriott Bonvoy points.
> * Hilton Midtown: 4.6 rating, Midtown, $425/night or 80,000 Hilton Honors points.
> * Kimpton Hotel: 4.4 rating, Chelsea, $310/night or 40,000 IHG Rewards points.
>
> **Loyalty Programs:**
>
> * Airline Points:
>   * United MileagePlus: 32,000
>   * Delta SkyMiles: 47,500
>   * American AAdvantage: 18,750
> * Hotel Points:
>   * Hilton Honors: 125,000
>   * Marriott Bonvoy: 68,000
>   * IHG Rewards: 42,000
> * Notable Redemption Opportunities:
>   * Free night at JW Marriott Essex House for 50,000 Marriott Bonvoy points (valued at $650)
>   * Economy round-trip ticket with Delta for 25,000 SkyMiles (valued at $450)
>   * Luxury weekend package at Waldorf Astoria with Hilton for 95,000 points (valued at $750)
>
> **Recommendations:**
>
> 1. **Flights:** The United flight (UA789) is the most affordable at $315.75 and gets you to New York in the afternoon. However, if you want an early start to your day in New York the American Airlines flight may be a better option for a slightly higher price of $349.99. Also, you have some Delta SkyMiles available, but it doesn't look like you have enough to redeem for a flight today.
> 2. **Hotels:** Given your points balances, using Marriott Bonvoy or Hilton Honors is the best value. The JW Marriott is a high-end option that you can use points for. Alternatively, the Hilton Midtown or DoubleTree are good options with strong ratings and less points. You can use your Hilton points for Hilton Midtown for 80,000 points. Considering value and your points, use 50,000 Marriott points for The Grand Plaza is a great way to maximize your points for a luxury stay. This could also be paired with the 25% discount off Broadway shows with Marriott Platinum status.
>
> **Summary:**
>
> For the best value, consider the United flight to EWR, for $315.75, paired with the JW Marriott The Grand Plaza, using 50,000 Marriott Bonvoy points.

### Demo 3: Attraction Planning with Google Search and Code Execution

**Task:**
> Search Google for best attractions in New York City for a one-day visit. I'd like you to create an itinerary with 3-4 popular attractions arranged in a sensible order based on their locations. Please include the approximate costs for each place. Take into account the current weather in New York and mention any applicable loyalty program benefits for New York City or discounts I might be eligible for. Finally, wrap up with a brief summary of the day's plan.

**Response:**
> Okay, based on the search results, here's a possible itinerary for a one-day visit to New York City, keeping in mind popular attractions, location, and potential costs:
>                            
> **Weather Check:**
>
> Tool: `get_current_weather(location='New York')`
>
> Okay, it's partly cloudy and 22°C in New York, which is a pleasant temperature for exploring.
>
> **Itinerary:**
>
> 1. **Top of the Rock Observation Deck (Morning):**
>    * Description: Start your day with panoramic views of the city from the Top of the Rock. This offers great views of Central Park and the Empire State Building.
>    * Location: Rockefeller Center, Midtown
>    * Estimated Cost: Around $40-$65 per person.
> 2. **New York Public Library & Bryant Park (Mid-day):**
>    * Description: Walk a few blocks to visit the iconic NYPL, admire its architecture and grand reading rooms, and then relax in the adjacent Bryant Park.
>    * Location: Midtown, near Grand Central Terminal
>    * Estimated Cost: Free
> 3. **Grand Central Terminal (Mid-day/Afternoon):**
>    * Description: Marvel at the architecture and celestial ceiling of this beautiful transportation hub.
>    * Location: Midtown
>    * Estimated Cost: Free
>
> **Loyalty Program Benefits & Discounts:**
>
> Tool: `query_loyalty_programs(destination='New York')`
>
> Based on your loyalty program data, you have some great opportunities!
>
> * Top of the Rock: It appears you have a Chase Sapphire Reserve card, which gives you priority access and 15% off admission. Be sure to use this discount.
> * Potential points redemption: With Marriott Bonvoy points, you could consider using points for a free night at the JW Marriott Essex House for future travel.
>                            
> **Summary of the Day's Plan:**
>
> You will begin your day with breathtaking views from Top of the Rock, taking advantage of your Chase Sapphire Reserve discount. You will then head to the New York Public Library and relax in nearby Bryant Park for a mid-day break, then head over to the iconic Grand Central Terminal before ending your day. This plan focuses on popular landmarks in midtown Manhattan, is walkable, and uses your loyalty program benefits. Remember that weather is pleasant for today. Have a great time exploring NYC! 