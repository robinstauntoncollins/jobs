FROM python:3.7-alpine

RUN adduser -D jobsapi

WORKDIR /home/jobsapi

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY api api
COPY migrations migrations
COPY jobsapi.py app.db config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R jobsapi:jobsapi ./
USER jobsapi

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
