import discord
from discord.ext import commands
from discord import Embed
from utils import get_sorted_roles, create_embed
from dienstliste import DienstListe

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

dienst_liste = DienstListe()

TOKEN = "MTM2MzYxMzY0MjI2MzYyOTkzNQ.GFhuJy.ccMaDcDCdUaHcBsvzml5CoLhr0SZlQm-y5s8vQ"  # <-- Hier dein Token

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

@bot.command()
async def liste(ctx, *, namen: str):
    member_ids = [m.id for m in ctx.guild.members]
    dienst_liste.clear()

    namen_liste = [name.strip() for name in namen.split(",")]
    for name in namen_liste:
        member = discord.utils.find(lambda m: m.display_name.lower() == name.lower(), ctx.guild.members)
        if member:
            dienst_liste.add(member)

    embed = await create_embed(ctx.guild, dienst_liste)
    msg = await ctx.send(embed=embed)

    await msg.add_reaction("✅")
    await msg.add_reaction("❌")
    dienst_liste.set_message(msg)

@bot.event
async def on_raw_reaction_add(payload):
    await dienst_liste.handle_reaction(bot, payload)

@bot.event
async def on_raw_reaction_remove(payload):
    await dienst_liste.handle_reaction(bot, payload)

bot.run(TOKEN)