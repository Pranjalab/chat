#!/usr/bin/env python3
import json
import os
import sys
import shutil

CONFIG_DIR = "/root/.clawdbot"
DATA_DIR = "/app/data"
MOLTBOT_CONFIG_FILE = os.path.join(CONFIG_DIR, "moltbot.json")
POLICY_FILE = os.path.join(CONFIG_DIR, "policy.json")

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def bind_user(username, role_name):
    # 1. Load Policy
    try:
        policy = load_json(POLICY_FILE)
    except FileNotFoundError:
        print(f"Error: Policy file not found at {POLICY_FILE}")
        sys.exit(1)

    role_config = policy.get("roles", {}).get(role_name)
    if not role_config:
        print(f"Error: Role '{role_name}' not defined in policy.")
        sys.exit(1)

    print(f"Creating user '{username}' with role '{role_name}'...")

    # 2. Provision Directory
    user_workspace = os.path.join(DATA_DIR, role_name, username)
    if os.path.exists(user_workspace):
        print(f"Warning: Workspace {user_workspace} already exists.")
    else:
        os.makedirs(user_workspace)
        print(f"Created workspace: {user_workspace}")

    # 3. Create Bootstrap Files (AGENTS.md, SOUL.md) based on Role
    agents_md = os.path.join(user_workspace, "AGENTS.md")
    if not os.path.exists(agents_md):
        with open(agents_md, 'w') as f:
            f.write(f"# AGENTS.md - {username}\n\n")
            f.write(f"Role: {role_name}\n")
            f.write(f"Access Description: {role_config.get('description', 'Standard access')}\n")
    
    soul_md = os.path.join(user_workspace, "SOUL.md")
    if not os.path.exists(soul_md):
        with open(soul_md, 'w') as f:
            f.write(f"# SOUL.md - {username}\n\n")
            f.write(f"You are a {role_name} capable assistant.\n")
            if role_name == 'user':
                f.write("You serve a standard user with limited tool access.\n")
            elif role_name == 'pro_user':
                f.write("You serve a professional user with advanced research capabilities.\n")

    # 4. Update Moltbot Config
    try:
        config = load_json(MOLTBOT_CONFIG_FILE)
    except FileNotFoundError:
        print(f"Error: Moltbot config not found at {MOLTBOT_CONFIG_FILE}")
        sys.exit(1)

    # Check if agent already exists
    agent_idx = -1
    for idx, agent in enumerate(config.get("agents", {}).get("list", [])):
        if agent["id"] == username:
            agent_idx = idx
            break

    new_agent = {
        "id": username,
        "name": username.capitalize(),
        "workspace": user_workspace,
        "tools": {
            "allow": role_config.get("tools_allow", []),
            "deny": role_config.get("tools_deny", [])
        },
        "sandbox": {
            "mode": role_config.get("sandbox_mode", "all")
        },
        "model": role_config.get("model", "ollama/llama3.1:8b")
    }

    if agent_idx >= 0:
        print(f"Updating existing agent configuration for '{username}'...")
        config["agents"]["list"][agent_idx] = new_agent
    else:
        print(f"Registering new agent configuration for '{username}'...")
        if "agents" not in config: config["agents"] = {}
        if "list" not in config["agents"]: config["agents"]["list"] = []
        config["agents"]["list"].append(new_agent)

    save_json(MOLTBOT_CONFIG_FILE, config)
    print("Configuration updated successfully.")
    print("NOTE: You must restart the Gateway for changes to take effect.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 create_user.py <username> <role>")
        sys.exit(1)
    
    bind_user(sys.argv[1], sys.argv[2])
