# Client build stage
FROM mcr.microsoft.com/devcontainers/typescript-node AS client-layers

WORKDIR /app/client

COPY src/app/types/ /app/types/
COPY src/app/client/ /app/client/

RUN pnpm install && pnpm build

# Server build stage
FROM oven/bun:latest

WORKDIR /app/server

COPY src/app/types/ /app/types/
COPY src/app/server/ /app/server/
ENV NODE_ENV production

RUN bun install --production

# Copy client build output from the previous stage
COPY --from=client-layers /app/client/ /app/server/client
# RUN ls -al /app/server/client

CMD ["bun", "run", "src/index.ts"]

EXPOSE 8000
