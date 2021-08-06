#FROM tiangolo/uwsgi-nginx-flask:python3.6
FROM python:3.7
MAINTAINER sergei_kuzmin1@epam.com

ARG DB_HOST
ENV DB_HOST=$DB_HOST
ARG DB_USER
ENV DB_USER=$DB_USER
ARG DB_NAME
ENV DB_HOST=$DB_NAME
ARG DB_PASSWORD
ENV DB_PASSWORD=$DB_PASSWORD

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
