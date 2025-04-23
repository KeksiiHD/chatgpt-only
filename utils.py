import discord

RANG_ORDER = [
    "Chefarzt",
    "Praxisleitung",
    "Arzt",
    "Ausbildung",
    "Praktikant"
]

async def create_embed(guild, dienst_liste):
    embed = discord.Embed(title="📋 Dienstliste", color=discord.Color.blue())
    rollen_dict = {}

    for user_id in dienst_liste.get_members():
        member = guild.get_member(user_id)
        if not member:
            continue
        status = dienst_liste.get_status(user_id)
        emoji = "✅" if status else "❌"

        rang = get_rang(member)
        if rang not in rollen_dict:
            rollen_dict[rang] = []
        rollen_dict[rang].append(f"{member.display_name} {emoji}")

    for rang in RANG_ORDER:
        if rang in rollen_dict:
            embed.add_field(name=f"__{rang}__", value="\n".join(rollen_dict[rang]), inline=False)

    return embed

def get_rang(member):
    member_roles = [role.name for role in member.roles]
    for rang in RANG_ORDER:
        if rang in member_roles:
            return rang
    return "Unbekannt"