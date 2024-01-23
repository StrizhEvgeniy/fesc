# Как запускать...

## Сбилдить контейнер
```shell
docker build -f Dockerfile -t react-flask-app .
```

## Поднять контейнер на 80 порту
```shell
docker run -d -p 80:3000 react-flask-app
```

# Адрес для подключения через ssh

```shell
ssh root@45.153.69.218
```

# Root-pass

```shell
nP9hvSux?iwH3X
```

# Важно!!!
## Ни в коем случае не менять расположение папок
## Не удалять роут из фласка с путем /
