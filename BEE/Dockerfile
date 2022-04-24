FROM python:3.8.5 as bee
RUN  apt-get update && apt-get install -y --no-install-recommends nano sudo iputils-ping && rm -rf /var/lib/apt/lists/*
RUN  apt-get update && apt-get install apt-transport-https ca-certificates
COPY /requirements.txt /
RUN  pip install --upgrade pip && pip install -r requirements.txt
RUN  mkdir /home/bee
COPY / /home/bee
ADD  .env /home/bee/.env
WORKDIR /home/bee
RUN python manage.py makemigrations --merge
CMD ["gunicorn", "-w 2", "main.wsgi"]

