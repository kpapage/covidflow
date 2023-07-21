#!/bin/bash
sudo docker cp ./covidflow/ScrapeQuestions.py backend:/covidflow
sudo docker exec backend python3 /covidflow/ScrapeQuestions.py
