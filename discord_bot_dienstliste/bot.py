import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

role_hierarchy = ["Chefarzt", "Praxisleitung", "Arzt", "Ausbildung", "Praktikant"]
status_dict = {}

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

@bot.command()
async def liste(ctx, *, namen):
    name_list = [name.strip() for name in namen.split(",")]
    guild = ctx.guild

    sorted_roles = {role: [] for role in role_hierarchy}
    status_dict[ctx.message.id] = {name: "❌" for name in name_list}

    for name in name_list:
        member = discord.utils.find(lambda m: m.display_name == name, guild.members)
        if member:
            for role in member.roles:
                if role.name in sorted_roles:
                    sorted_roles[role.name].append((name, "❌"))
                    break

    embed = discord.Embed(title="Dienstübersicht", description="Reagiere mit ✅ oder ❌ um deinen Status zu ändern", color=0x2f3136)
    for role in role_hierarchy:
        if sorted_roles[role]:
            embed.add_field(
                name=f"__{role}__",
                value="\n".join([f"{entry[0]} {entry[1]}" for entry in sorted_roles[role]]),
                inline=False
            )

    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    status_dict[message.id] = {name: "❌" for name in name_list}

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot or reaction.message.id not in status_dict:
        return
    name = user.display_name
    if name not in status_dict[reaction.message.id]:
        return

    if reaction.emoji == "✅":
        status_dict[reaction.message.id][name] = "✅"
    elif reaction.emoji == "❌":
        status_dict[reaction.message.id][name] = "❌"

    await update_embed(reaction.message)

async def update_embed(message):
    embed = message.embeds[0]
    new_embed = discord.Embed(title="Dienstübersicht", description=embed.description, color=0x2f3136)

    guild = message.guild
    current_status = status_dict[message.id]

    sorted_roles = {role: [] for role in role_hierarchy}
    for name, symbol in current_status.items():
        member = discord.utils.find(lambda m: m.display_name == name, guild.members)
        if member:
            for role in member.roles:
                if role.name in sorted_roles:
                    sorted_roles[role.name].append((name, symbol))
                    break

    for role in role_hierarchy:
        if sorted_roles[role]:
            new_embed.add_field(
                name=f"__{role}__",
                value="\n".join([f"{name} {symbol}" for name, symbol in sorted_roles[role]]),
                inline=False
            )

    await message.edit(embed=new_embed)

# Optional für dauerhaften Betrieb
try:
    import keep_alive
    keep_alive.keep_alive()
except:
    pass

bot.run(TOKEN)
