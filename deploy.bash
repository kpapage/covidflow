#!/bin/bash

touch ./cron_log.txt
sudo docker compose down
sudo docker compose up --build