# Ping Hook

**The simplest possible MindRoom hook plugin.** Use this as a starting point when building your own hooks.

It registers a single `message:received` hook that responds to `!ping-hook` with `🏓 Pong from hook!` — that's it. The entire plugin is one manifest file and ~20 lines of Python.

## What it demonstrates

- Declaring a plugin via `mindroom.plugin.json`
- Registering a hook with `@hook(event="message:received", ...)`
- Using `ctx.send_message()` to reply in the same room/thread
- Setting `ctx.suppress = True` to prevent the normal response pipeline

## Setup

1. Copy to `~/.mindroom-chat/plugins/ping-hook`
2. Add to `config.yaml`:
   ```yaml
   plugins:
     - path: plugins/ping-hook
   ```
3. Restart MindRoom
4. Send `!ping-hook` in any room → `🏓 Pong from hook!`