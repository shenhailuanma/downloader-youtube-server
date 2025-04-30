# downloader-youtube-server
downloader-youtube-server


## Docker build 

```sh
docker build --no-cache -t downloader-youtube-server:20250430  -f Dockerfile .
```

## Use docker

```sh
docker run -p 15000:15000 -v /tmp/download:/tmp/download -d downloader-youtube-server:20250430
docker run --restart=always -p 15000:15000 -v /tmp/download:/tmp/download -d downloader-youtube-server:20250430
```

