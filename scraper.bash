#!/bin/bash

cd /covidflow
time=$(date)
echo "Starting scraping questions at $time" >> /cron_log.txt
python3 /covidflow/ScrapeQuestions.py >> /cron_log.txt 2>&1

if [ $? -eq 0 ]; then
    time=$(date)
    echo "Scraped questions at $time" >> /cron_log.txt
else
    time=$(date)
    echo "Scrape failed at $time" >> /cron_log.txt
fi
