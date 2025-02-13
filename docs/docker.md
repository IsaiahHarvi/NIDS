# Common Docker commands
**Start Components**
```
docker compose --profile gui up
```

**Stop Components**
```
docker compose --profile gui down
```

**Rebuild Components**
```
docker compose --profile gui up --build
```

**Push updates to registry**
```
docker compose --profile gui push
```

**View logs**
```
docker compose logs -f
```

**List running containers**
```
docker ps
```
