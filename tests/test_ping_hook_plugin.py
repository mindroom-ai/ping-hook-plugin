# ruff: noqa: INP001
"""Behavior tests for ping-hook plugin."""

from __future__ import annotations

import sys
from importlib import util
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from mindroom.constants import ROUTER_AGENT_NAME
from mindroom.hooks import MessageEnvelope, SenderKind, TurnIntent, TurnOrigin, TurnTrust
from mindroom.hooks.decorators import get_hook_metadata
from mindroom.message_target import MessageTarget


def _load_hooks_module() -> ModuleType:
    hooks_path = Path(__file__).resolve().parents[1] / "hooks.py"
    module_name = "mindroom_test_ping_hook_hooks"
    spec = util.spec_from_file_location(module_name, hooks_path)
    assert spec is not None
    assert spec.loader is not None
    module = util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


hooks = _load_hooks_module()


def _context(body: str, *, event_id: str | None = "$pong") -> SimpleNamespace:
    target = MessageTarget.resolve(
        room_id="!room:localhost",
        thread_id="$thread-root",
        reply_to_event_id=None,
    )
    origin = TurnOrigin(
        transport_sender_id="@user:localhost",
        requester_id="@user:localhost",
        sender_entity_name=None,
        requester_entity_name=None,
        sender_kind=SenderKind.USER,
        requester_kind=SenderKind.USER,
        intent=TurnIntent.USER_MESSAGE,
        source_kind="message",
        trust=TurnTrust.EXTERNAL,
    )
    return SimpleNamespace(
        envelope=MessageEnvelope(
            source_event_id="$ping",
            target=target,
            body=body,
            attachment_ids=(),
            mentioned_agents=(),
            agent_name=ROUTER_AGENT_NAME,
            origin=origin,
        ),
        send_message=AsyncMock(return_value=event_id),
        logger=MagicMock(),
        suppress=False,
    )


def test_hook_metadata_is_router_scoped() -> None:
    """Ping hook should retain router-only command semantics."""
    metadata = get_hook_metadata(hooks.handle_ping)

    assert metadata is not None
    assert metadata.event_name == "message:received"
    assert metadata.hook_name == "ping-hook"
    assert metadata.agents == (ROUTER_AGENT_NAME,)
    assert metadata.timeout_ms == 30000


@pytest.mark.asyncio
async def test_matching_ping_replies_in_same_thread_and_suppresses() -> None:
    """Exact ping command should reply and stop normal dispatch."""
    ctx = _context("  !ping-hook\n")

    await hooks.handle_ping(ctx)

    ctx.send_message.assert_awaited_once_with(
        room_id="!room:localhost",
        text="🏓 Pong from hook!",
        thread_id="$thread-root",
    )
    assert ctx.suppress is True


@pytest.mark.asyncio
async def test_unrelated_message_is_ignored() -> None:
    """Non-command messages should pass through untouched."""
    ctx = _context("hello")

    await hooks.handle_ping(ctx)

    ctx.send_message.assert_not_awaited()
    assert ctx.suppress is False


@pytest.mark.asyncio
async def test_failed_reply_does_not_suppress_dispatch() -> None:
    """Send failure should preserve normal message handling."""
    ctx = _context("!ping-hook", event_id=None)

    await hooks.handle_ping(ctx)

    assert ctx.suppress is False
    ctx.logger.warning.assert_called_once_with(
        "ping-hook failed to send pong",
        room_id="!room:localhost",
    )
