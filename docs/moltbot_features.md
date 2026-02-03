# Moltbot Features & Usage Guide

This document outlines the core features, tools, and capabilities of Moltbot, along with instructions on how to use them via the CLI or through Agent Prompts.

## 🛠️ Core Agent Tools
These tools are native to the agent and can be used directly within a conversation if enabled in the allowlist.

| Feature / Tool | Description | Usage | Agent Prompt Example | Initialization |
| :--- | :--- | :--- | :--- | :--- |
| **Filesystem (`fs`)** | Read, write, and list files in the workspace. | **Agent** | "List files in the current directory."<br>"Read `SOUL.md`." | Enabled by default (group:fs). |
| **Command Execution (`exec`)** | Run shell commands on the host or sandbox. | **Agent** | "Check the current git branch."<br>"Run `npm test`." | Enabled via allowlist (`group:runtime` or `exec`). |
| **Browser (`browser`)** | Navigate websites, click elements, and extract text. | **Agent** | "Go to google.com and search for 'Moltbot'." | Must be enabled in `tools.allow` (`browser`). |
| **Memory Search (`memory`)** | Semantic search over `MEMORY.md` and `memory/*.md`. | **Agent** | "Search memory for 'project context'." | Enabled by default (`group:memory`). |
| **Message (`message`)** | Send messages, reply to threads, and perform channel actions. | **Agent** | "Send a WhatsApp message to +12345." | Enabled by default (`group:web`). |
| **Cron Management (`cron`)** | Schedule recurring jobs or one-off reminders. | **Agent** | "Remind me to check logs every Monday at 9am." | Must be enabled in `tools.allow` (`cron`). |
| **Gateway Control (`gateway`)** | Restart gateway, apply config, or run updates. | **Agent** | "Restart the gateway." | Must be enabled in `tools.allow` (`gateway`). |

---

## 🤖 Automation & Scheduling
Features that allow Moltbot to operate proactively or in the background.

| Feature | Description | Usage | Agent Access | How to Start / Configure |
| :--- | :--- | :--- | :--- | :--- |
| **Heartbeat** | Periodic "poke" to check inbox, calendar, or files. | **CLI / Auto** | **Active**<br>Agent responds to system prompt. | `moltbot system heartbeat enable` |
| **Cron Jobs** | Scheduled tasks running in isolated or main sessions. | **CLI**<br>`moltbot cron add ...` | **Yes**<br>Via `cron` tool. | `moltbot cron add --name "Check" --cron "0 9 * * *" ...` |
| **Webhooks** | Trigger agent actions via HTTP POST (e.g., from Github/Gmail). | **CLI / Config** | **Passive**<br>Agent receives webhook payload. | Enable in `moltbot.json` (`hooks: { enabled: true }`). |

---

## 📡 Communication Channels
Platforms where Moltbot can send and receive messages.

| Channel | Description | Setup Method | Agent Access |
| :--- | :--- | :--- | :--- |
| **WhatsApp** | Primary channel. Requires QR scanning. | `moltbot channels add --channel whatsapp` | Yes (via `message` tool) |
| **Telegram** | Bot API. Supports groups and topics. | `moltbot channels add --channel telegram` | Yes (via `message` tool) |
| **Discord** | Bot API + Gateway. Supports servers/DMs. | `moltbot channels add --channel discord` | Yes (via `message` tool) |
| **Slack** | Workspace apps via Bolt SDK. | `moltbot channels add --channel slack` | Yes (via `message` tool) |
| **Signal** | Privacy-focused. Uses `signal-cli`. | `moltbot channels add --channel signal` | Yes (via `message` tool) |
| **BlueBubbles** | iMessage relay for macOS. | `moltbot channels add --channel bluebubbles` | Yes (via `message` tool) |
| **WebChat** | Browser-based UI for testing. | Built-in | Yes (via `message` tool) |

---

## 🖥️ CLI Management Functions
Administrative commands typically run by the User via terminal. The agent can theoretically run these via `exec` if capable/allowed.

| Command | Purpose | User Command | Agent Prompt (via `exec`) |
| :--- | :--- | :--- | :--- |
| **Setup/Onboard** | Initialize workspace and config. | `moltbot onboard` | *Not recommended for Agent* |
| **Status** | Check health of gateway and channels. | `moltbot status` | "Run `moltbot status` and tell me if WhatsApp is connected." |
| **Agents** | Manage multi-agent setups. | `moltbot agents list`<br>`moltbot agents add ...` | "List all configured agents." |
| **Logs** | View gateway or channel logs. | `moltbot logs` | "Check the last 50 lines of logs." |
| **Plugins** | Install and manage extensions. | `moltbot plugins list` | "List installed plugins." |
| **Security** | Audit configuration for safety. | `moltbot security audit` | "Run a security audit." |

---

## 🧠 Agent Memory & Identity
The "Brain" of the agent, stored in the Workspace (`~/clawd`).

| File | Purpose | How to Use |
| :--- | :--- | :--- |
| `AGENTS.md` | **Operating Instructions**. The agent reads this on every startup. | User manually edits file. Agent follows instructions. |
| `SOUL.md` | **Persona**. Defines personality, tone, and vibes. | User manually edits file. Agent embodies this persona. |
| `MEMORY.md` | **Long-term Memory**. Curated facts and learnings. | User or Agent edits via `fs`. Agent reads on startup. |
| `TOOLS.md` | **Local Notes**. Environment details (e.g., "The server IP is..."). | User manual edits. Agent references for context. |
| `SKILL.md` | **Skill Definitions**. "How-to" guides for specific tasks. | Placed in `skills/` folder. Agent reads when specific skill is selected. |

## 🚀 How to Access Features

### 1. Enabling Tools
To give an agent access to a tool, edit `moltbot.json` or `agent.json` under the `tools.allow` section.
```json
"tools": {
  "allow": [
    "group:fs",
    "group:runtime", // Enables exec
    "browser",       // Enables browser
    "cron"           // Enables cron management
  ]
}
```

### 2. Multi-Agent Routing
To set up multiple agents (e.g., Personal vs Work):
1.  Run `moltbot agents add <id>`.
2.  Configure routing in `moltbot.json` under `bindings`.
    ```json
    "bindings": [
      { "agentId": "work", "match": { "channel": "whatsapp", "accountId": "biz" } }
    ]
    ```

### 3. Using Skills
1.  Create a folder `skills/<skill-name>/`.
2.  Add a `SKILL.md` with instructions.
3.  The agent will automatically index it and "read" the skill when relevant to a user request.
