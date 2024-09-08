# Client build stage
FROM mcr.microsoft.com/devcontainers/typescript-node AS client-layers

COPY src/app/types/ /app/types/
COPY src/app/client/ /app/client/
WORKDIR /app/client

RUN pnpm install
RUN pnpm build
RUN ls -la /app/client/dist

# Server build stage
FROM oven/bun:latest
ENV NODE_ENV production

# this is weird but we absolute path in one of the ts files
COPY src/grpc_ /workspaces/NIDS/src/grpc_

COPY src/app/types/ /app/types/
COPY src/app/server/ /app/server/
WORKDIR /app/server

RUN bun install --production

# Copy client build output from the previous stage
COPY --from=client-layers /app/client/dist /app/server/dist

CMD ["bun", "run", "src/index.ts"]

EXPOSE 8000
