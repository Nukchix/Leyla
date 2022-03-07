import disnake
from disnake.ext import commands


class EmojiRole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def get_data_from_db(self, message):
        if await self.bot.config.DB.emojirole.count_documents({"_id": message}) == 0:
            return False
        else:
            return await self.bot.config.DB.emojirole.find_one({"_id": message})

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: disnake.RawReactionActionEvent):
        if payload.member.bot: return
        if await self.get_data_from_db(payload.message_id):
            data = dict(await self.get_data_from_db(payload.message_id))

            if data['_id'] == payload.message_id:
                if payload.emoji in data['emojis'].keys():
                    for i in data['emojis']:
                        for j in i[payload.emoji]: # {'emojis': [{'here_emoji': 'role_id'}, {'again_emoji': 'role_id'}, ...]}
                            await payload.member.add_roles(self.bot.get_guild(payload.guild_id).get_role(int(j)))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: disnake.RawReactionActionEvent):
        if payload.member.bot: return
        if await self.get_data_from_db(payload.message_id):
            data = dict(await self.get_data_from_db(payload.message_id))

            if data['_id'] == payload.message_id:
                if payload.emoji in data['emojis'].keys():
                    for i in data['emojis']:
                        for j in i[payload.emoji]:
                            await payload.member.remove_roles(self.bot.get_guild(payload.guild_id).get_role(int(j)))


def setup(bot):
    bot.add_cog(EmojiRole(bot))
