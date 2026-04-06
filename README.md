# Ping Hook

Place this plugin at a path MindRoom can resolve from `config.yaml`.
If you use `/home/basnijholt/.mindroom-chat/config.yaml`, the simplest option is to copy or symlink this directory into `/home/basnijholt/.mindroom-chat/plugins/ping-hook`.

Add this plugin entry to `config.yaml`.

```yaml
plugins:
  - path: plugins/ping-hook
```

Restart MindRoom after saving the config.
Send `!ping-hook` in a room the router can see.
The hook replies with `🏓 Pong from hook!` via `ctx.send_message()` and suppresses the normal unknown-command response.
