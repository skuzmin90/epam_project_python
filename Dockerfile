##FROM tiangolo/uwsgi-nginx-flask:python3.6
#FROM python:3.7
#MAINTAINER sergei_kuzmin1@epam.com
#
#WORKDIR /app
#COPY ./app /app
#
#RUN pip3 install -r requirements.txt
#
#EXPOSE 5000
#CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]

FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY ./app/requirements.txt /app/
RUN pip install -r requirements.txt
COPY ./app /app/
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]