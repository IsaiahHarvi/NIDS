FROM mcr.microsoft.com/devcontainers/typescript-node AS client-layers

WORKDIR /app/client

COPY src/app/types/ /app/types/
COPY src/app/client/ /app/client/

RUN pnpm i && pnpm build

# Build the server
FROM oven/bun:latest

WORKDIR /app/server

COPY src/app/types/ /app/types/
COPY src/app/server/ /app/server/

ENV NODE_ENV production

RUN dir -s  

RUN bun install --production

COPY --from=client-layers /app/client/dist /app/server/dist

CMD ["bun", "run"]

EXPOSE 8000
