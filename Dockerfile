FROM ubuntu

# Copy files
COPY . /covidflow
WORKDIR /covidflow

# Install Python and dependencies
RUN apt update
RUN apt install -y python3-pip

# Install Firefox and FirefoxDriver and dependencies for Selenium
# RUN apt install -y wget
# RUN wget http://security.ubuntu.com/ubuntu/pool/main/f/firefox/firefox_115.0.2+build1-0ubuntu0.20.04.1_amd64.deb -O /tmp/firefox.deb
# RUN apt install -y /tmp/firefox.deb 
# RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz
# RUN tar -C /opt -xzf /tmp/geckodriver.tar.gz
# RUN chmod 755 /opt/geckodriver
# RUN ln -fs /opt/geckodriver /usr/bin/geckodriver
# RUN ln -fs /opt/geckodriver /usr/local/bin/geckodriver

# Install Python dependencies
RUN pip install -r actual_requirements.txt

# RUN python3 /covidflow/ScrapeQuestions.py
CMD ["python3", "-m" , "gunicorn", "-w", "8", "-b", "0.0.0.0:8000", "covidsite.routes:app"]
