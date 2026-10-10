import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

log = logging.getLogger("ballsdex.packages.extradrop")

async def setup(bot: "BallsDexBot"):
    log.info("Loading ExtraDrop package...")
    from .cog import ExtraDrop
    await bot.add_cog(ExtraDrop(bot))
    log.info("ExtraDrop package loaded successfully!")
