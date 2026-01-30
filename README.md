# Moltbot Secure Service Bot

A professional, well-structured deployment of [Moltbot](https://github.com/moltbot/moltbot) as a 24/7 secure service on Linux.

## Features
- **Local-first Gateway**: Single control plane for sessions, channels, tools, and events.
- **Multi-channel Inbox**: Connect to WhatsApp, Telegram, Slack, Discord, and more.
- **Role-Based Access Control (RBAC)**: Centralized `policy.json` to manage tool and data access.
- **Dockerized Sandbox**: Ephemeral environments for all tool executions.
- **Voice & Talk Mode**: Integration-ready for ElevenLabs and voice interfaces.

## Project Structure
- `config/`: Contains `policy.json` (access rules) and `users.json` (user database).
- `data/`: Isolated folders for `admin`, `pro-user`, and `user` roles.
- `docker/`: Build files for containerized deployment.

## Access Control Matrix

| Role | Tool Access | Data Access | Sandbox Permissions |
| :--- | :--- | :--- | :--- |
| **Admin** | Full (`*`) | Full Subtree | `operator.admin` |
| **Pro-User** | Browser (Read), FS (Read/Write), Logic | `/data/pro-user` | Contained |
| **User** | FS (Read Only), Logic | `/data/user` | Read-Only |

## Installation

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.x (for the management utility)
- SSH Access to your Linux system

### 2. Setup
Clone this repository and move into the directory:
```bash
git clone <your-repo-url>
cd moltbot-service
```

### 3. Deployment
Start the services with Docker Compose:
```bash
docker-compose -f docker/docker-compose.yml up -d
```

## How to Use This App

This project consists of the **Moltbot AI Engine** (running in Docker) and a **Management CLI** (Python) to handle your users and policies.

### 1. Initial Access
Once the bot is running, connect your messaging channel (e.g., Telegram) via the Moltbot Control UI at `http://localhost:18789`.

### 2. Managing Users & Roles
Use the provided management utility in the `src/` folder to manage your user database:

**Run a health check:**
```bash
python3 src/main.py health-check
```

**Run Moltbot Engine Diagnostic (Doctor):**
*Note: The container must be running.*
```bash
python3 src/main.py moltbot-doctor
```

**Add a new user:**
```bash
python3 src/main.py add-user --role pro_user --name "John Doe" --email "john@example.com" --phone "+12345"
```

### 3. Messaging Flow
- **Step 1**: An unknown user messages your bot.
- **Step 2**: The bot replies with a **Pairing Code**.
- **Step 3**: You (the Admin) approve the pairing code using the Moltbot UI or CLI.
- **Step 4**: The bot automatically applies the permissions defined for that user in `policy.json`.

---

## Secure Access
The management UI is bound to `localhost` for security. Access it via an SSH tunnel:
```bash
ssh -L 18789:localhost:18789 user@your-linux-server
```
Then visit `http://localhost:18789` in your local browser.

## Configuration

### Policy Management (`config/policy.json`)
Define role-specific tools and scopes here. Changes require a restart of the `moltbot-gateway` container.

### User Management (`config/users.json`)
Add or remove users from the dictionary-based JSON store. Each user should be assigned an ID used for pairing on messaging channels.

## Security Note
- **Never** expose port `18789` to the public internet.
- Regularly audit your `users.json` and `policy.json` files.
- Run `moltbot doctor` within the container to check for configuration risks.

## Port Security & Hardening

To ensure your gateway is not accessible to unauthorized users, follow these hardening steps:

### 1. Localhost Binding (Default)
The `docker-compose.yml` is already configured to bind the gateway port only to the internal loopback interface:
```yaml
ports:
  - "127.0.0.1:18789:18789"
```
This prevents external IPs from reaching the port directly even if your firewall is open.

### 2. Firewall (UFW)
On your Linux server, it is recommended to explicitly block external access to this port while allowing SSH:
```bash
sudo ufw allow ssh
sudo ufw deny 18789
sudo ufw enable
```

### 3. Secure Access via SSH Tunnel
Since the port is bound to `127.0.0.1`, you must use an SSH tunnel to access the UI from your local machine:
```bash
ssh -L 18789:localhost:18789 user@your-linux-server
```
Once the tunnel is active, you can safely browse to `http://localhost:18789` locally. The traffic is encrypted through your SSH session.
