#! /usr/bin/bash
set -e

docker build -t ktracker .
docker run -td --restart=always --name ktracker -e KTRACKER_CHAT_ID="${KTRACKER_CHAT_ID}" -e KTRACKER_BOT_ID="${KTRACKER_BOT_ID}" ktracker
echo "Container started with name \"ktracker\". Check logs via \`docker container logs ktracker\`."
