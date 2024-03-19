import discord
import requests
import os
import json
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='!', intents=discord.Intents.default())
session = requests.Session()

with open('descriptions.json', 'r') as file:
    descriptions = json.load(file)

def get_weather(city):
    """
    Gets the weather information (temperature, wind speed, and weather description) for a given city
    """
    try:
        # Get latitude and longitude of the city
        url = f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json'
        response = session.get(url)
        response.raise_for_status()
        data = response.json()

        latitude = data['results'][0]['latitude']
        longitude = data['results'][0]['longitude']
        city_name = data['results'][0]['name']

        # Get weather information
        url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,is_day,weather_code,wind_speed_10m'
        response = session.get(url)
        response.raise_for_status()
        data = response.json()

        current_weather = data['current']
        temperature = current_weather['temperature_2m']
        wind_speed = current_weather['wind_speed_10m']
        weather_code = current_weather['weather_code']
        is_day = current_weather['is_day'] == 1

        if is_day:
            weather_description = descriptions[str(weather_code)]['day']['description']
            image = descriptions[str(weather_code)]['day']['image']
        else:
            weather_description = descriptions[str(weather_code)]['night']['description']
            image = descriptions[str(weather_code)]['night']['image']

        temperature = int(temperature) if temperature.is_integer() else temperature
        wind_speed = int(wind_speed) if wind_speed.is_integer() else wind_speed

        return temperature, wind_speed, weather_description, is_day, image, city_name

    except Exception as e:
        print(f"Error getting weather information: {e}")
        return

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    try:
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@client.tree.command(name='weather', description='Get the weather information for a given city')
@app_commands.describe(city='The city to get the weather information for')
async def weather(interaction: discord.Interaction, city: str):
    await interaction.response.defer()
    weather_info = get_weather(city)
    if weather_info:
        temperature, wind_speed, weather_description, is_day, image, city_name = weather_info
        time = "Day" if is_day else "Night"
        embed = discord.Embed(title=f'Weather in {city_name}', description=f"## {weather_description}", color=0x00ff00)
        embed.add_field(name='Temperature 🌡️', value=f'{temperature} °C')
        embed.add_field(name='Wind Speed 💨', value=f'{wind_speed} Km/h')
        embed.add_field(name='Day/Night 🏙️', value=time)
        embed.set_image(url=image)
        await interaction.followup.send(embed=embed)
    else:
        embed = discord.Embed(title='Error', description='An error occurred while getting the weather information', color=0xff0000)
        await interaction.followup.send(embed=embed)

client.run(TOKEN)
