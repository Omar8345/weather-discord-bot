import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils import get_weather


class WeatherCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready():
        print("Weather command is loaded.")

    @app_commands.command(name="weather", description="Fetch weather for a city.")
    async def weather(self, interaction: discord.Interaction, city: str):
        """Fetch weather for a city using a slash command."""
        weather_info = await get_weather(city)
        if weather_info:
            temperature, wind_speed, weather_description, is_day, image, city_name = (
                weather_info
            )
            await interaction.response.send_message(
                f"Weather for {city_name}: {weather_description}\n"
                f"Temperature: {temperature}°C\nWind Speed: {wind_speed} km/h\n"
                f"Day: {'Yes' if is_day else 'No'}\nImage: {image}"
            )
        else:
            await interaction.response.send_message(
                f"Could not retrieve weather data for {city}."
            )


async def setup(bot):
    await bot.add_cog(WeatherCog(bot))
