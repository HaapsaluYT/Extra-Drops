from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from bd_models.models import Ball

DEFAULT_TITLE = "{ball} dropped something!"
DEFAULT_DESCRIPTION = "You have obtained a {drop}."


class ExtraDropRule(models.Model):
    """When `trigger_ball` is caught, roll `chance` for the player to also receive `drop_ball`."""

    trigger_ball = models.ForeignKey(
        Ball,
        on_delete=models.CASCADE,
        related_name="extradrop_triggers",
        help_text="Catching this ball can cause an extra drop.",
    )
    drop_ball = models.ForeignKey(
        Ball,
        on_delete=models.CASCADE,
        related_name="extradrop_drops",
        help_text="The ball that may be given as the extra drop.",
    )
    chance = models.FloatField(
        default=0.1,
        validators=(MinValueValidator(0.0), MaxValueValidator(1.0)),
        help_text="Probability between 0 and 1 (e.g. 0.25 = 25%). Rolled independently on every catch.",
    )
    enabled = models.BooleanField(default=True)

    message_title = models.CharField(
        max_length=256,
        blank=True,
        default=DEFAULT_TITLE,
        help_text=(
            "Title of the announcement embed. Placeholders: {ball} = the caught ball, {drop} = the dropped ball, "
            "{user} = the player's name. Leave blank to use the default."
        ),
    )
    message_description = models.TextField(
        max_length=4096,
        blank=True,
        default=DEFAULT_DESCRIPTION,
        help_text=(
            "Description of the announcement embed. Same placeholders as the title: {ball}, {drop}, {user}. "
            "Leave blank to use the default."
        ),
    )

    class Meta:
        verbose_name = "Extra drop"
        verbose_name_plural = "Extra drops"
        constraints = [
            models.UniqueConstraint(fields=("trigger_ball", "drop_ball"), name="extradrop_unique_rule"),
            models.CheckConstraint(
                condition=models.Q(chance__gte=0.0) & models.Q(chance__lte=1.0), name="extradrop_chance_0_1"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.trigger_ball} -> {self.drop_ball} ({self.chance:.2%})"