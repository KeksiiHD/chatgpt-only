import discord
from utils import create_embed

class DienstListe:
    def __init__(self):
        self.nutzer = {}  # user_id: status (True = Haken, False = X)
        self.msg = None

    def add(self, member):
        self.nutzer[member.id] = False  # Standard = X

    def set_message(self, msg):
        self.msg = msg

    def clear(self):
        self.nutzer = {}
        self.msg = None

    async def handle_reaction(self, bot, payload):
        if payload.user_id == bot.user.id or self.msg is None or payload.message_id != self.msg.id:
            return

        emoji = str(payload.emoji)
        user_id = payload.user_id

        if user_id in self.nutzer:
            if emoji == "✅":
                self.nutzer[user_id] = True
            elif emoji == "❌":
                self.nutzer[user_id] = False

            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(user_id)
            embed = await create_embed(guild, self)
            await self.msg.edit(embed=embed)

    def get_status(self, user_id):
        return self.nutzer.get(user_id, False)

    def get_members(self):
        return self.nutzer.keys()