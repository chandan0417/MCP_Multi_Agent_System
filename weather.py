from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get the current weather for a specific location.
    
    Args:
        location: City name and optional country code (e.g., 'London,uk' or 'New York')
        
    Returns:
        Weather information as a string
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        return "Error: OPENWEATHERMAP_API_KEY not found in environment variables"
    
    try:
        # First, get coordinates for the location
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        
        if not geo_data:
            return f"Could not find location: {location}"
            
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        
        # Get weather data
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        if weather_response.status_code != 200:
            return f"Error getting weather data: {weather_data.get('message', 'Unknown error')}"
        
        # Format the response
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        
        return (
            f"Weather in {location}:\n"
            f"- Temperature: {temp}°C (feels like {feels_like}°C)\n"
            f"- Conditions: {description}\n"
            f"- Humidity: {humidity}%\n"
            f"- Wind: {wind_speed} m/s"
        )
        
    except Exception as e:
        return f"Error getting weather: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
