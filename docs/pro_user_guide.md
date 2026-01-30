# Pro User Usage Guide

The Pro User role is designed for trusted collaborators who need advanced capabilities and project-specific file access.

## Access Level
- **Tools**: Access to productivity and search tools, including `browser.read` and standard `fs` operations within the `pro-user` directory.
- **Data Access**: Full Read/Write access to the `/data/pro-user` folder on the host.

## Usage Guidelines
- All tools are executed within an isolated Docker sandbox.
- You can store, edit, and analyze project files located in your assigned directory.
- Ask the agent for help with complex tasks, code analysis, or data manipulation within your sandbox scope.

## Security
- Your activities are logged within the container.
- Raw shell access (`system.run`) is disabled to maintain system integrity.
