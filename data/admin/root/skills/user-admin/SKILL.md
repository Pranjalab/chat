---
name: user-admin
description: Tools for managing Chat system users (create, list, delete, update).
---

# User Administration Skill

You are the Admin. You can manage the users of the system using the `manage_users.py` script.
**IMPORTANT**: Users are identified by their Phone Number (e.g., `+1555...`).

## Capabilities

### 1. List Users
To see all registered users and their roles:
`python3 /app/data/admin/bin/manage_users.py list`

### 2. Create / Add User
To grant access to a phone number:
`python3 /app/data/admin/bin/manage_users.py add <phone_number> <role>`
*   **Roles**: `user`, `pro_user`, `admin`
*   Example: "Add +15550001234 as a pro user" -> `... add +15550001234 pro_user`

### 3. Update User Role
To change a user's role:
`python3 /app/data/admin/bin/manage_users.py update <phone_number> <new_role>`

### 4. Delete User
To revoke access:
`python3 /app/data/admin/bin/manage_users.py delete <phone_number>`

## Important Notes
- **Restart Required**: After any add, update, or delete operation, you MUST restart the gateway for changes to take effect.
- **Restart Command**: `moltbot gateway restart` (or use the `gateway` tool if available).
- **Notify**: "Applied changes for user [Phone]. Restarting gateway..."
