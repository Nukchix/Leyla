from os import environ

import jishaku
from disnake.ext import commands
from jishaku.cog import Jishaku
from jishaku.features.baseclass import Feature


class LeylaJishaku(Jishaku):

    def __init__(self, bot):
        self.bot = bot

    COG_EMOJI = '👑'

    @Feature.Command(parent='jsk', name='test')
    async def test(self, ctx):
        return await ctx.reply('Ok')


def setup(bot: commands.Bot):
    jishaku.Flags.NO_UNDERSCORE = True
    jishaku.Flags.FORCE_PAGINATOR = True
    jishaku.Flags.NO_DM_TRACEBACK = True
    environ['JISHAKU_EMBEDDED_JSK'] = 'true'
    bot.add_cog(LeylaJishaku(bot=bot))
