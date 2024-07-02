docker image rm dmr-database-tool
docker buildx prune -f
docker build -t dmr-database-tool https://raw.githubusercontent.com/DMR-Database/dmr-database-tool/main/Docker/Dockerfile
