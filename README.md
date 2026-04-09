# Ping Hook

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-plugins-blue)](https://docs.mindroom.chat/plugins/)
[![Hooks](https://img.shields.io/badge/docs-hooks-blue)](https://docs.mindroom.chat/hooks/)

<img src="https://media.githubusercontent.com/media/mindroom-ai/mindroom/refs/heads/main/frontend/public/logo.png" alt="MindRoom Logo" align="right" width="120" />

The simplest possible [MindRoom](https://github.com/mindroom-ai/mindroom) hook plugin. Use it as a starting point for building your own hook-only plugin.

It registers a single `message:received` hook that responds to `!ping-hook` with `🏓 Pong from hook!`. The implementation is intentionally tiny, but it still demonstrates the key pieces most hook plugins need: event filtering, sending a message, and suppressing the normal response pipeline.

## Features

- Registers a router-scoped `message:received` hook
- Responds to the exact command `!ping-hook`
- Sends the reply into the current room and thread with `ctx.send_message()`
- Sets `ctx.suppress = True` so MindRoom does not continue with the normal response flow
- Minimal example repo for plugin manifests, hook registration, and message handling

## How It Works

1. A user sends `!ping-hook` in a room or thread.
2. The `ping-hook` hook checks the incoming message body.
3. If it matches, the hook posts `🏓 Pong from hook!` back into the same room and thread.
4. The hook suppresses the rest of the message pipeline so the command behaves like a lightweight built-in action.

## Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `ping-hook` | `message:received` | Respond to `!ping-hook` with a direct message reply |

## Setup

1. Copy this plugin to `~/.mindroom/plugins/ping-hook`.
2. Add the plugin to `config.yaml`:
   ```yaml
   plugins:
     - path: plugins/ping-hook
   ```
3. Restart MindRoom.

No agent tools or plugin settings are required.
