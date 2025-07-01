import discord
from discord.ext import commands
from discord import app_commands
import json
import os

TOKEN = os.getenv("TOKEN")
LOG_FILE = "flight_logs.json"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump({}, f, indent=2)

def log_flight(user_id, log_data):
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    logs.setdefault(str(user_id), []).append(log_data)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ UAL Service Bot is online as {bot.user}")

@bot.tree.command(name="start_flight", description="Start logging your United VA flight.")
@app_commands.describe(callsign="Your callsign (e.g. UAL123)", aircraft="Aircraft type (e.g. B738)", departure="Departure airport ICAO", arrival="Arrival airport ICAO", cruise_alt="Cruise altitude (feet)")
async def start_flight(interaction: discord.Interaction, callsign: str, aircraft: str, departure: str, arrival: str, cruise_alt: int):
    embed = discord.Embed(title="🛫 Flight Started", color=0x1d4ed8)
    embed.add_field(name="Callsign", value=callsign)
    embed.add_field(name="Aircraft", value=aircraft)
    embed.add_field(name="Route", value=f"{departure} ➡ {arrival}")
    embed.add_field(name="Cruise Altitude", value=f"{cruise_alt} ft")
    embed.set_footer(text=f"Pilot: {interaction.user.display_name}")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="end_flight", description="End and log your United VA flight.")
@app_commands.describe(screenshot="Link to a screenshot of your completed flight.", remarks="Any remarks you have (optional).")
async def end_flight(interaction: discord.Interaction, screenshot: str, remarks: str = "None"):
    log_data = {"screenshot": screenshot, "remarks": remarks}
    log_flight(interaction.user.id, log_data)
    embed = discord.Embed(title="✅ Flight Logged Successfully", color=0x22c55e)
    embed.add_field(name="Screenshot", value=screenshot, inline=False)
    embed.add_field(name="Remarks", value=remarks, inline=False)
    embed.set_footer(text=f"Pilot: {interaction.user.display_name}")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="stats", description="View your United VA flight statistics.")
async def stats(interaction: discord.Interaction):
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    user_logs = logs.get(str(interaction.user.id), [])
    embed = discord.Embed(title="📊 Flight Statistics", color=0xfacc15)
    embed.add_field(name="Flights Logged", value=str(len(user_logs)), inline=False)
    embed.set_footer(text=f"Pilot: {interaction.user.display_name}")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="view_flight", description="View your most recent United VA flight log.")
async def view_flight(interaction: discord.Interaction):
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    user_logs = logs.get(str(interaction.user.id), [])
    if not user_logs:
        await interaction.response.send_message("❌ You have no flights logged yet.", ephemeral=True)
        return
    last_flight = user_logs[-1]
    embed = discord.Embed(title="📝 Most Recent Flight Log", color=0x60a5fa)
    embed.add_field(name="Screenshot", value=last_flight["screenshot"], inline=False)
    embed.add_field(name="Remarks", value=last_flight["remarks"], inline=False)
    embed.set_footer(text=f"Pilot: {interaction.user.display_name}")
    await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run(TOKEN)
