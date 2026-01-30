# Admin Setup & Usage Guide

As the Admin of the Moltbot service, you have full control over the gateway, configuration, and all data folders.

## Responsibilities
- **User Approval**: Reviewing and approving pairing codes for new users.
- **Policy Management**: Updating `policy.json` to adjust tool or folder access.
- **System Maintenance**: Monitoring Docker container health and running internal diagnostics.

## Key Admin Tools
- **`system.run`**: Direct access to the sandbox shell.
- **`fs.*`**: Full read/write access to all data directories (`admin`, `pro-user`, `user`).
- **`browser.*`**: Complete web browsing capabilities with no URL restrictions.

## Security Reminders
- Regularly verify authorized users in the `users.json` database.
- Use `python3 src/main.py health-check` to identify permission issues or missing folders.
- Ensure the gateway is strictly bound to `localhost` and access it only via SSH tunneling.
