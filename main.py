import discord
from discord.ext import commands
from discord.ui import Button, View
import aiohttp
import os

# Load the bot token from environment variables 
TOKEN = os.getenv('DISCORD_TOKEN')
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL', 'http://placeholder.com')

# Setup the bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Define the interactive buttons
class PrepMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=" Daily DSA", style=discord.ButtonStyle.primary, custom_id="btn_dsa")
    async def dsa_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Sending DSA request to n8n...", ephemeral=True)
        await self.send_to_n8n("DSA", interaction.user.name)

    @discord.ui.button(label=" Internships", style=discord.ButtonStyle.success, custom_id="btn_intern")
    async def intern_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Scraping internships via n8n...", ephemeral=True)
        await self.send_to_n8n("Internships", interaction.user.name)

    # Function to trigger n8n workflow
    async def send_to_n8n(self, choice, username):
        payload = {"user": username, "selection": choice}
        async with aiohttp.ClientSession() as session:
            try:
                await session.post(N8N_WEBHOOK_URL, json=payload)
                print(f"Webhook sent to n8n: {choice}")
            except Exception as e:
                print(f"Failed to send webhook: {e}")

@bot.event
async def on_ready():
    print(f' Logged in as {bot.user} - Online and Ready!')

# The command to spawn the menu in Discord
@bot.command()
async def prep(ctx):
    view = PrepMenu()
    await ctx.send("Good morning! What are we focusing on today?", view=view)

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("ERROR: DISCORD_TOKEN not found in environment variables.")