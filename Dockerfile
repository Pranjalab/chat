FROM node:22-bullseye

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    make \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy package management files and scripts
COPY moltbot-src/package.json moltbot-src/pnpm-lock.yaml ./moltbot-src/
COPY moltbot-src/scripts ./moltbot-src/scripts

WORKDIR /app/moltbot-src

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy the rest of the source code
COPY moltbot-src/ .

# Skip build step due to missing UI assets
# RUN pnpm build

# Expose the application port
EXPOSE 3000

# Start command: run gateway explicitly
CMD ["node", "scripts/run-node.mjs", "gateway"]
