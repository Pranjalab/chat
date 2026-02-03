# Issue: WhatsApp Not Connected

If Moltbot is not receiving or sending messages via WhatsApp, the provider session may have expired or failed to initialize.

## Troubleshooting & Resolution

### 1. Check Logs
Check for authentication or connection errors in the gateway logs:
```bash
docker logs moltbot-gateway | grep whatsapp
```

### 2. Re-pair WhatsApp
If the session is invalid, you may need to re-link your device via the Moltbot Control UI. 

1. Open the UI at `http://localhost:18789`.
2. Locate the WhatsApp channel.
3. Scan the QR code if prompted.

### 3. Restart Provider
In some cases, restarting the container can force a reconnection:
```bash
docker compose -f docker/docker-compose.yml restart moltbot
```

### 4. Verify Policy
Ensure the user has permissions to use the WhatsApp tool in `config/policy.json`.
