FROM python

ENV APP_HOME=/home/app/web

RUN mkdir -p $APP_HOME

WORKDIR $APP_HOME

RUN apt update && apt install python3 netcat -y

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . $APP_HOME

RUN pip install -r requirements.txt

RUN chmod +x /home/app/web/entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]