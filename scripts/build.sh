#!/bin/bash

docker compose down

docker compose rm -f
docker rmi img2url-client img2url-server

docker compose up --build
 