#!/bin/bash

cd /covidflow
time=$(date)
echo "Starting updating questions at $time" >> /cron_log.txt
python3 /covidflow/UpdateQuestions.py >> /cron_log.txt 2>&1 

if [ $? -eq 0 ]; then
    time=$(date)
    echo "Updated questions at $time" >> /cron_log.txt
else
    time=$(date)
    echo "Update failed at $time" >> /cron_log.txt
fi
