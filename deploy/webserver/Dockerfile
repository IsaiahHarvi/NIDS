# # Client build stage
# FROM mcr.microsoft.com/devcontainers/typescript-node AS client-layers

# COPY src/app/types/ /app/types/
# COPY src/app/client/ /app/client/
# WORKDIR /app/client

# RUN pnpm install
# RUN pnpm build
# RUN ls -la /app/client/dist

# # Server build stage
# FROM oven/bun:latest
# ENV NODE_ENV production

# # this is weird but we absolute path in one of the ts files
# COPY src/grpc_ /workspaces/NIDS/src/grpc_

# COPY src/app/types/ /app/types/
# COPY src/app/server/ /app/server/
# WORKDIR /app/server

# RUN bun install --production

# # Copy client build output from the previous stage
# COPY --from=client-layers /app/client/dist /app/server/dist

# CMD ["bun", "run", "--watch", "src/index.ts"]

# EXPOSE 8000

# Temporary Workaround
FROM mcr.microsoft.com/devcontainers/typescript-node
COPY src/grpc_ /workspaces/NIDS/src/grpc_

COPY src/app/ /app/src/app/
RUN npm i -g bun

WORKDIR /app/src/app/client
RUN bun i

WORKDIR /app/src/app/server
RUN bun i

EXPOSE 8000 5073

CMD bash -c "cd /app/src/app/client && bun dev & cd /app/src/app/server && bun dev"
