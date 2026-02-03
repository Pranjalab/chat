#!/usr/bin/env python3
import json
import os
import sys
import argparse

CONFIG_DIR = "/root/.moltbot"
DATA_DIR = "/app/data"
MOLTBOT_CONFIG_FILE = os.path.join(CONFIG_DIR, "moltbot.json")
POLICY_FILE = os.path.join(CONFIG_DIR, "policy.json")

def load_json(path):
    if not os.path.exists(path): return {}
    with open(path, 'r') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def get_policy():
    return load_json(POLICY_FILE)

def get_config():
    return load_json(MOLTBOT_CONFIG_FILE)

def list_users():
    config = get_config()
    agents = config.get("agents", {}).get("list", [])
    print(f"{'PHONE/ID':<20} {'ROLE':<15} {'WORKSPACE'}")
    print("-" * 60)
    for agent in agents:
        ws = agent.get("workspace", "")
        role = "unknown"
        if "/admin/" in ws: role = "admin"
        elif "/pro_user/" in ws: role = "pro_user"
        elif "/user/" in ws: role = "user"
        
        print(f"{agent.get('id'):<20} {role:<15} {ws}")

def add_user(phone_number, role_name):
    # Basic validation (simple check for now)
    if not phone_number.startswith("+"):
        print("Warning: Phone number should typically start with '+' (e.g., +1555...). Proceeding anyway.")

    policy = get_policy()
    role_config = policy.get("roles", {}).get(role_name)
    if not role_config:
        print(f"Error: Role '{role_name}' not defined in policy. Available: {list(policy.get('roles', {}).keys())}")
        sys.exit(1)

    print(f"Provisioning user '{phone_number}' with role '{role_name}'...")
    
    # 1. Access Control: Provision Workspace
    # Sanitize phone for directory name if needed, but keeping it simple for now
    safe_dirname = phone_number.replace("+", "")
    user_workspace = os.path.join(DATA_DIR, role_name, safe_dirname)
    
    if not os.path.exists(user_workspace):
        os.makedirs(user_workspace)
        
    # 2. Bootstrap Files
    with open(os.path.join(user_workspace, "AGENTS.md"), 'w') as f:
        f.write(f"# AGENTS.md - {phone_number}\nRole: {role_name}\n")
    
    with open(os.path.join(user_workspace, "SOUL.md"), 'w') as f:
        f.write(f"# SOUL.md - {phone_number}\nYou are a {role_name} assistant for user {phone_number}.\n")

    # 3. Update Agent Config
    config = get_config()
    
    # Remove existing agent definition if exists
    agents = config.get("agents", {}).get("list", [])
    agents = [a for a in agents if a["id"] != phone_number]
    
    new_agent = {
        "id": phone_number,
        "name": phone_number,
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
    
    if "agents" not in config: config["agents"] = {}
    if "list" not in config["agents"]: config["agents"]["list"] = []
    config["agents"]["list"] = agents + [new_agent]

    # 4. Update Bindings (The Routing Layer)
    # Ensure bindings structure exists
    if "bindings" not in config: config["bindings"] = []
    
    # Remove existing binding for this phone number if any
    bindings = config.get("bindings", [])
    if isinstance(bindings, dict): bindings = [] # Safety check if schema was wrong before
    
    # Filter out any binding that matches this phone/agent
    bindings = [b for b in bindings if b.get("agentId") != phone_number]

    # Create new binding: Match WhatsApp messages FROM this number -> Route to THIS Agent
    new_binding = {
        "agentId": phone_number,
        "match": {
             "channel": "whatsapp",
             "peer": {
                 "kind": "dm",
                 "id": phone_number
             }
        }
    }
    
    bindings.append(new_binding)
    config["bindings"] = bindings

    save_json(MOLTBOT_CONFIG_FILE, config)
    print(f"User '{phone_number}' added and bound to WhatsApp channel. Restart gateway to apply.")

def delete_user(phone_number):
    config = get_config()
    
    # Remove agent
    agents = config.get("agents", {}).get("list", [])
    original_count = len(agents)
    config["agents"]["list"] = [a for a in agents if a["id"] != phone_number]
    
    # Remove binding
    bindings = config.get("bindings", [])
    config["bindings"] = [b for b in bindings if b.get("agentId") != phone_number]
    
    save_json(MOLTBOT_CONFIG_FILE, config)
    
    if len(config["agents"]["list"]) < original_count:
        print(f"User '{phone_number}' removed from config. Restart gateway to apply.")
    else:
        print(f"User '{phone_number}' not found.")

def update_role(phone_number, role_name):
    add_user(phone_number, role_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage Chat Users")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # List
    subparsers.add_parser("list", help="List all users")
    
    # Add
    add_parser = subparsers.add_parser("add", help="Add a new user")
    add_parser.add_argument("phone", help="Phone Number (e.g. +1234567890)")
    add_parser.add_argument("role", help="Role (user, pro_user, admin)")
    
    # Delete
    del_parser = subparsers.add_parser("delete", help="Delete a user")
    del_parser.add_argument("phone", help="Phone Number")
    
    # Update
    upd_parser = subparsers.add_parser("update", help="Update user role")
    upd_parser.add_argument("phone", help="Phone Number")
    upd_parser.add_argument("role", help="New Role")

    args = parser.parse_args()
    
    if args.command == "list":
        list_users()
    elif args.command == "add":
        add_user(args.phone, args.role)
    elif args.command == "delete":
        delete_user(args.phone)
    elif args.command == "update":
        update_role(args.phone, args.role)
