import os
import argparse
import subprocess
import json
from pathlib import Path

# Paths to our configuration files
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
USERS_FILE = CONFIG_DIR / "users.json"
POLICY_FILE = CONFIG_DIR / "policy.json"

def load_json(file_path):
    if not file_path.exists():
        return {}
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def health_check():
    """Comprehensive check of the project's health and readiness."""
    print("=== Moltbot Project Health Check ===")
    
    # 1. Check Configuration Files
    config_files = [USERS_FILE, POLICY_FILE]
    for f in config_files:
        if f.exists():
            try:
                load_json(f)
                print(f"[✓] {f.name:<15}: Exists and valid JSON")
            except Exception as e:
                print(f"[✗] {f.name:<15}: Invalid JSON - {e}")
        else:
            print(f"[✗] {f.name:<15}: MISSING")

    # 2. Check Docker Files
    docker_dir = BASE_DIR / "docker"
    docker_files = ["Dockerfile", "docker-compose.yml"]
    for df in docker_files:
        path = docker_dir / df
        if path.exists():
            print(f"[✓] {df:<15}: Exists")
        else:
            print(f"[✗] {df:<15}: MISSING in docker/ folder")

    # 3. Check Data Folders (Based on Policy)
    print("\n--- Folder Isolation Check ---")
    policies = load_json(POLICY_FILE)
    if policies:
        required_folders = set()
        for role, details in policies.get("roles", {}).items():
            required_folders.update(details.get("data_access", []))
        
        for folder in required_folders:
            folder_path = DATA_DIR / folder
            if folder_path.exists():
                print(f"[✓] Data folder '{folder}': Exists")
            else:
                print(f"[!] Data folder '{folder}': MISSING (Action: run 'mkdir -p data/{folder}')")

    # 4. User Database Summary
    users = load_json(USERS_FILE)
    if users:
        print("\n--- User Database Summary ---")
        for role, role_users in users.items():
            print(f"{role.capitalize():<12}: {len(role_users)} users registered")
    
    print("\n====================================")

def moltbot_doctor():
    """Runs the internal Moltbot doctor command inside the container."""
    print("=== Running Moltbot Engine Doctor Audit ===")
    try:
        # We use docker exec to run the command inside the running container
        result = subprocess.run(
            ["docker", "exec", "moltbot-gateway", "node", "dist/index.js", "doctor"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("[!] Error running moltbot doctor. Is the container running?")
            print(result.stderr)
    except FileNotFoundError:
        print("[!] Docker command not found. Please ensure Docker is installed and in your PATH.")
    except Exception as e:
        print(f"[!] An error occurred: {e}")

def add_user(role, name, email, phone):
    """Adds a new user to the users.json database."""
    users = load_json(USERS_FILE)
    if role not in users:
        users[role] = []
        
    user_id = f"{role}_{len(users[role]) + 1:03}"
    new_user = {
        "name": name,
        "gmail": email,
        "phone": phone,
        "id": user_id
    }
    users[role].append(new_user)
    save_json(USERS_FILE, users)
    print(f"User added successfully! ID: {user_id}")

def main():
    parser = argparse.ArgumentParser(description="Moltbot Project Management Utility")
    subparsers = parser.add_subparsers(dest="command")

    # Health-check command
    subparsers.add_parser("health-check", help="Run a full project health check")
    
    # Moltbot Doctor command
    subparsers.add_parser("moltbot-doctor", help="Run the Moltbot engine diagnostic (Internal)")

    # Add-user command
    add_user_parser = subparsers.add_parser("add-user", help="Add a new user")
    add_user_parser.add_argument("--role", required=True, choices=["admin", "pro_user", "user"], help="User role")
    add_user_parser.add_argument("--name", required=True, help="User full name")
    add_user_parser.add_argument("--email", required=True, help="User email")
    add_user_parser.add_argument("--phone", required=True, help="User phone number")

    args = parser.parse_args()

    if args.command == "health-check":
        health_check()
    elif args.command == "moltbot-doctor":
        moltbot_doctor()
    elif args.command == "add-user":
        add_user(args.role, args.name, args.email, args.phone)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
