# Build Stage
FROM node:22-bookworm AS builder

# Install Bun for build scripts
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"
RUN corepack enable

WORKDIR /moltbot-src
# Copy source from moltbot-src directory
COPY moltbot-src/package.json moltbot-src/pnpm-lock.yaml moltbot-src/pnpm-workspace.yaml moltbot-src/.npmrc ./
COPY moltbot-src/ui/package.json ./ui/package.json
COPY moltbot-src/patches ./patches
COPY moltbot-src/scripts ./scripts

RUN pnpm install --frozen-lockfile
COPY moltbot-src .
RUN CLAWDBOT_A2UI_SKIP_MISSING=1 pnpm build
RUN pnpm ui:install
RUN pnpm ui:build

# Production Stage
FROM node:22-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends \
    trash-cli \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN corepack enable

WORKDIR /app
# Copy built files
COPY --from=builder /moltbot-src/dist ./dist
COPY --from=builder /moltbot-src/node_modules ./node_modules
COPY --from=builder /moltbot-src/package.json ./package.json
COPY --from=builder /moltbot-src/moltbot.mjs ./moltbot.mjs
COPY --from=builder /moltbot-src/scripts ./scripts
# Include extensions and skills (required for built-in plugins/functions)
COPY --from=builder /moltbot-src/extensions ./extensions
COPY --from=builder /moltbot-src/skills ./skills

# Set up project directories and copy configurations (from our app)
RUN mkdir -p /app/config /app/data/admin /app/data/pro-user /app/data/user
COPY config/policy.json /app/config/policy.json
COPY config/users.json /app/config/users.json

# Ensure ownership for the node user
RUN chown -R node:node /app

# Expose the gateway port
EXPOSE 18789

# Security: Run as non-root
USER node

# Start moltbot gateway
CMD ["node", "dist/index.js", "gateway"]
