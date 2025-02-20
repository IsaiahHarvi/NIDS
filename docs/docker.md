# Common Docker commands
**Start Components**
```
docker compose --profile gui up
```

**Start Components w/o Logs**
```
docker compose --profile gui up -d
```
**Start Components w/o Registry**
```
docker compose --profile gui up --build
```
**Stop Components**
```
docker compose --profile gui down
```

**Rebuild Components**
```
docker compose --profile gui up --build
```

**View logs**
```
docker compose logs -f
```

**List running containers**
```
docker ps
```
