#FROM tiangolo/uwsgi-nginx-flask:python3.6
FROM python:3.7
MAINTAINER sergei_kuzmin1@epam.com

ENV DB_HOST=$DB_HOST
ENV DB_USER=$DB_USER
ENV DB_HOST=$DB_NAME
ENV DB_PASSWORD=$DB_PASSWORD

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
