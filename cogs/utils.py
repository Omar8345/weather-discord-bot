import aiohttp
import json
from pathlib import Path

DESCRIPTIONS_FILE = Path("./config/descriptions.json")
if not DESCRIPTIONS_FILE.is_file():
    raise FileNotFoundError(f"Descriptions file not found: {DESCRIPTIONS_FILE}")

with DESCRIPTIONS_FILE.open("r") as file:
    descriptions = json.load(file)


async def get_weather(city: str):
    """
    Fetches weather information for a given city.
    """
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        async with aiohttp.ClientSession() as session:
            async with session.get(geo_url) as geo_response:
                geo_data = await geo_response.json()
                latitude = geo_data["results"][0]["latitude"]
                longitude = geo_data["results"][0]["longitude"]
                city_name = geo_data["results"][0]["name"]

            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
            async with session.get(weather_url) as weather_response:
                weather_data = await weather_response.json()
                current_weather = weather_data["current_weather"]
                temperature = current_weather["temperature"]
                wind_speed = current_weather["windspeed"]
                weather_code = current_weather["weathercode"]
                is_day = current_weather["is_day"] == 1

                if is_day:
                    weather_description = descriptions[str(weather_code)]["day"][
                        "description"
                    ]
                    image = descriptions[str(weather_code)]["day"]["image"]
                else:
                    weather_description = descriptions[str(weather_code)]["night"][
                        "description"
                    ]
                    image = descriptions[str(weather_code)]["night"]["image"]

                return (
                    temperature,
                    wind_speed,
                    weather_description,
                    is_day,
                    image,
                    city_name,
                )

    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None
