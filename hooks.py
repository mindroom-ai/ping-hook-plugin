# ruff: noqa: INP001
"""Minimal ping hook used to verify ctx.send_message()."""

from __future__ import annotations

from mindroom.constants import ROUTER_AGENT_NAME
from mindroom.hooks import MessageReceivedContext, hook

_PING = "!ping-hook"
_PONG = "🏓 Pong from hook!"


@hook(event="message:received", name="ping-hook", agents=(ROUTER_AGENT_NAME,), timeout_ms=30000)
async def handle_ping(ctx: MessageReceivedContext) -> None:
    """Reply to the ping command in the same room and thread."""
    if ctx.envelope.body.strip() != _PING:
        return

    event_id = await ctx.send_message(
        room_id=ctx.envelope.room_id,
        text=_PONG,
        thread_id=ctx.envelope.resolved_thread_id,
    )
    if event_id is None:
        ctx.logger.warning("ping-hook failed to send pong", room_id=ctx.envelope.room_id)
        return

    ctx.suppress = True
