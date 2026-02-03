# Features Guide

This document outlines the current status of Moltbot features and upcoming integrations.

## Current Features

### 🟢 WhatsApp Integration
- **Status**: Active
- **How to use**: Link your WhatsApp account via the Control UI. The bot can then send and receive messages from authorized users.
- **Permissions**: Defined in `policy.json`.

### 🟢 Local LLM (Ollama)
- **Status**: Active
- **How to use**: Configure `moltbot.json` with the `ollama` provider. Supports GPU acceleration for high performance.
- **Verified Models**: `llama3.1:8b`.

### 🟢 File System & Terminal Access
- **Status**: Active (Admin/Pro-User)
- **How to use**: Agents can read/write files in dedicated workspaces and execute safe terminal commands.

#### Quick Guide: Prompt to Feature

| Goal | Example Prompt |
| :--- | :--- |
| **List Files** | "What files are in my admin folder?" |
| **Read File** | "Open and read the contents of `IDENTITY.md`" |
| **Discuss File** | "Analyze the contents of `moltbot.json` and explain the agents list." |
| **Add Content** | "Append 'Task complete' to the end of `TODO.txt`" |
| **Soft Delete** | "Delete `old_log.txt` (Move to `.bin` folder)" |
| **Google Search** | "Search Google for latest Node.js release notes" |
| **Scan/Explain URL** | "Scan https://docs.molt.bot and explain the gateway settings." |

---

## Upcoming Features (Roadmap)

### 📧 Mail (Gmail/Outlook)
- **Status**: 🛠️ Development
- **Feature**: Automated email triage, drafting replies, and following up on threads.
- **Integration**: OAuth-based secure access.

### 📝 Notion Integration
- **Status**: 🛠️ Development
- **Feature**: Syncing tasks, managing databases, and capturing notes directly from chat.
- **Integration**: Notion API (Internal Integrations).

### 🗄️ MongoDB Database
- **Status**: 🛠️ Development
- **Feature**: Persistent long-term memory for agents and unified storage for harvested data.
- **Integration**: Connection via `MONGODB_URI`.

### 🗓️ Calendar (Google/iCal)
- **Status**: 📅 Planned
- **Feature**: Scheduling meetings and providing daily agenda summaries.
