import asyncio
from os import environ

import disnake
from core import Leyla
from config import Config

config = Config()

async def init_and_run_bot(token: str) -> None:
    bot = Leyla(
        owner_ids=[848593011038224405, 880028714841305150, 598387707311554570],
        command_prefix="l.",
        allowed_mentions=disnake.AllowedMentions(
            everyone=False,
            replied_user=True,
            roles=False,
            users=False,
        ),
        strip_after_prefix=True,
        case_insensitive=True,
        status=disnake.Status.dnd,
        intents=disnake.Intents.all(),
        sync_commands=True,
        enable_debug_events=True,
        help_command=None
    )
    bot.config = config
    await bot.start(token)

loop = asyncio.get_event_loop()
loop.run_until_complete(init_and_run_bot(environ['TOKEN']))
