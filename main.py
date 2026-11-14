import os
import threading
from flask import Flask
import discord
from discord.ext import commands

app = Flask(__name__)

@app.route(/)
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Bot con song ne!")

@bot.command()
async def like(ctx, amount: int = 1000):
    for emoji in ["][:amount]:
        try:
            await ctx.message.add_reaction(emoji)
        except:
            pass
    await ctx.send(f"Da buff {amount} like roi 100% thanh cong!")

TOKEN = os.environ.get("DISCORD_TOKEN")
bot.run(TOKEN)
