FROM mcr.microsoft.com/devcontainers/typescript-node as client_ 

COPY src/app/types/ /app/types/
COPY src/app/client/ /app/client/

WORKDIR /app/client
RUN pnpm i && pnpm build

# Build the server
FROM oven/bun:latest

COPY src/app/types/ /app/types/
COPY src/app/server/ /app/server/

WORKDIR /app/server

ENV NODE_ENV production

RUN dir -s  

RUN bun install --production

COPY --from=client_ /app/client/dist /app/server/dist

CMD ["bun", "run", "--watch", "src/index.ts"]

EXPOSE 8000
