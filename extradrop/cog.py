from __future__ import annotations

import logging
import random
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from ballsdex.core.events import BallCaughtEvent
from bd_models.models import BallInstance
from settings.models import settings

from .models import DEFAULT_DESCRIPTION, DEFAULT_TITLE, ExtraDropRule

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

log = logging.getLogger(__name__)


def render(template: str, default: str, **values: str) -> str:
    """
    Fill {placeholders} in an admin-written template. Uses plain replacement instead of str.format so
    stray braces in the text can never raise an error.
    """
    text = template.strip() or default
    for key, value in values.items():
        text = text.replace("{" + key + "}", value)
    return text


class ExtraDrop(commands.Cog):
    """Gives a chance of an extra countryball when a specific one is caught."""

    def __init__(self, bot: "BallsDexBot"):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ballsdex_ball_caught(self, event: BallCaughtEvent):
        if event.dropped:
            return

        caught = event.ball_instance
        rules = [
            rule
            async for rule in ExtraDropRule.objects.filter(
                trigger_ball_id=caught.ball_id, enabled=True
            ).select_related("drop_ball")
        ]
        if not rules:
            return

        channel = event.view.message.channel

        for rule in rules:
            if random.random() >= rule.chance:
                continue

            drop = rule.drop_ball
            try:
                instance = await BallInstance.objects.acreate(
                    ball=drop,
                    player=event.player,
                    attack_bonus=random.randint(-settings.max_attack_bonus, settings.max_attack_bonus),
                    health_bonus=random.randint(-settings.max_health_bonus, settings.max_health_bonus),
                    server_id=event.guild.id if event.guild else None,
                )
            except Exception:
                log.exception("Failed to create extra drop %s for player %s", drop, event.player.pk)
                continue

            log.info(
                f"{event.user} received extra {settings.collectible_name} {drop.country} (`{instance.pk:0X}`) "
                f"from catching {caught.countryball.country}. "
                f"(ATK={instance.attack_bonus:+d} HP={instance.health_bonus:+d})."
            )

            placeholders = {
                "ball": caught.countryball.country,
                "drop": drop.country,
                "user": event.user.display_name,
            }
            embed = discord.Embed(
                title=render(rule.message_title, DEFAULT_TITLE, **placeholders)[:256],
                description=render(rule.message_description, DEFAULT_DESCRIPTION, **placeholders)[:4096],
                color=discord.Color.blurple(),
            )
            embed.set_author(name=event.user.display_name, icon_url=event.user.display_avatar.url)
            embed.set_footer(text=f"ATK: {instance.attack_bonus:+d} • HP: {instance.health_bonus:+d}")
            try:
                file = discord.File(drop.wild_card.path, filename="countryball.png")
                embed.set_thumbnail(url="attachment://countryball.png")
                await channel.send(content=event.user.mention, embed=embed, file=file)
            except Exception:
                log.exception("Failed to announce extra drop %s", drop)


async def setup(bot: "BallsDexBot"):
    await bot.add_cog(ExtraDrop(bot))