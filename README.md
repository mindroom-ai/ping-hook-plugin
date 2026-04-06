# Ping Hook

The simplest possible MindRoom hook plugin — use as a starting point for building your own.

Registers a single `message:received` hook that responds to `!ping-hook` with `🏓 Pong from hook!`. The entire plugin is one manifest file and ~20 lines of Python.

## How it works

1. User sends `!ping-hook` in any room
2. Hook fires, sends `🏓 Pong from hook!` via `ctx.send_message()`
3. Sets `ctx.suppress = True` to prevent the normal response pipeline from running

## Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `ping-hook` | `message:received` | Respond to `!ping-hook` command |

## Setup

1. Copy to `~/.mindroom/plugins/ping-hook`
2. Add to `config.yaml`:
   ```yaml
   plugins:
     - path: plugins/ping-hook
   ```
3. Restart MindRoom