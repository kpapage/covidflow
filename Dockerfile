FROM ubuntu

# Copy files
COPY . /covidflow
WORKDIR /covidflow

# Install Python and dependencies
RUN apt update
RUN apt install -y python3-pip cron

# Install Python dependencies
RUN mv /covidflow/env/lib/python3.10/site-packages/* /usr/local/lib/python3.10/dist-packages
RUN pip install -r requirements.txt

# Run cron jobs
RUN chmod +x /covidflow/scraper.bash
RUN chmod +x /covidflow/updater.bash
RUN echo "@weekly root bash /covidflow/scraper.bash" >> /etc/crontab
RUN echo "@monthly root bash /covidflow/updater.bash" >> /etc/crontab

CMD cron && python3 -m gunicorn -w 8 -b 0.0.0.0:8000 covidsite.routes:app
