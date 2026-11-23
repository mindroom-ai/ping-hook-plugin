# Ping Hook

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/mindroom-ai/ping-hook-plugin/actions/workflows/plugin-ci.yml/badge.svg)](https://github.com/mindroom-ai/ping-hook-plugin/actions/workflows/plugin-ci.yml)
[![Docs](https://img.shields.io/badge/docs-plugins-blue)](https://docs.mindroom.chat/plugins/)
[![Hooks](https://img.shields.io/badge/docs-hooks-blue)](https://docs.mindroom.chat/hooks/)

<picture>
  <source media="(prefers-reduced-motion: no-preference)" srcset="https://raw.githubusercontent.com/mindroom-ai/mindroom/main/assets/logo/logo-mark-animated.svg" />
  <img src="https://raw.githubusercontent.com/mindroom-ai/mindroom/main/assets/logo/logo-mark.svg" alt="MindRoom Logo" align="right" width="120" />
</picture>

A minimal [MindRoom](https://github.com/mindroom-ai/mindroom) hook plugin that responds to `!ping-hook` with `🏓 Pong from hook!`.

- **Quick plugin health check:** verify that MindRoom loaded your plugins and can reply directly in a room or thread without calling a model.
- **Minimal starter template:** the entire plugin is 27 lines in [hooks.py](hooks.py) — a clean reference for building custom `!command` hooks that reply in-place and bypass normal agent dispatch.
- **Single reply, zero config:** runs once per incoming message rather than once per bot, with no settings or agent tools required.

```text
You:  !ping-hook
Bot:  🏓 Pong from hook!
```

## Quick start

```bash
mindroom plugins install ping-hook-plugin
```

Add to `config.yaml`:

```yaml
plugins:
  - path: plugins/ping-hook-plugin
```

No plugin settings or agent tools are required.

Update later with `mindroom plugins update ping-hook-plugin` (updating replaces the installed plugin directory, so keep custom edits in a manual checkout).
Needs MindRoom v2026.11.491 or later (plugin API 1.33).

<details>
<summary><b>How it works</b></summary>

1. Registers `ping-hook` on `message:received` with `scope="room"` (so it runs once per incoming room event instead of once per bot) and a `30000 ms` timeout.
2. Checks `ctx.envelope.body.strip() == "!ping-hook"`, ignoring surrounding whitespace and leaving every other message untouched.
3. Replies with `🏓 Pong from hook!` in the same room and resolved thread (`ctx.envelope.target.resolved_thread_id`) using `ctx.send_message()`.
4. Fails open on send failure: if `ctx.send_message()` returns `None`, the hook logs a warning and returns without suppressing normal dispatch.
5. After a successful reply, sets `ctx.suppress = True` so MindRoom skips the normal agent response flow.

</details>

<details>
<summary><b>Manual install</b></summary>

`mindroom plugins install` pins the installed commit in `.mindroom-plugin.lock.json` and validates the plugin before activating it. To install from a manual checkout instead:

1. Clone or copy this repository into `~/.mindroom/plugins/ping-hook-plugin`.
2. Add the plugin to `config.yaml`:
   ```yaml
   plugins:
     - path: ~/.mindroom/plugins/ping-hook-plugin
   ```
3. Restart MindRoom.

</details>

## Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `ping-hook` | `message:received` | Respond to `!ping-hook` with a direct message reply |
