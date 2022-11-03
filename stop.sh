#! /usr/bin/bash
set -e

echo "Stopping the container..."
docker container update --restart=no ktracker > /dev/null
docker container stop ktracker > /dev/null
docker container rm ktracker > /dev/null
echo "Container stopped."
