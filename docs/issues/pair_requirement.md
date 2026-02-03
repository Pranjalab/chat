# Issue: Pairing Required (1008)

If you see the error `disconnected (1008): pairing required` in the Moltbot Control UI or logs, it means the gateway is requesting a device handshake that has not been completed.

## Resolution

Since the gateway is already secured within your internal network, you can safely disable this requirement.

### 1. Update Configuration
Open `config/moltbot.json` and set `dangerouslyDisableDeviceAuth` to `true`:

```json
{
  "gateway": {
    "controlUi": {
      "dangerouslyDisableDeviceAuth": true
    }
  }
}
```

### 2. Restart Gateway
Restart the Moltbot container to apply the change:

```bash
docker compose -f docker/docker-compose.yml restart moltbot
```
