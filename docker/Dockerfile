FROM moltbot/moltbot:latest

# Set up project directories
RUN mkdir -p /app/config /app/data/admin /app/data/pro-user /app/data/user

# Copy configuration templates
COPY config/policy.json /app/config/policy.json
COPY config/users.json /app/config/users.json

# Expose the gateway port
EXPOSE 18789

# Set the working directory
WORKDIR /app

# The base image already has the entrypoint to start moltbot
CMD ["start"]
