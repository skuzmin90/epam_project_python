#FROM tiangolo/uwsgi-nginx-flask:python3.6
FROM python:3.7
MAINTAINER sergei_kuzmin1@epam.com

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt

EXPOSE 80
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]
