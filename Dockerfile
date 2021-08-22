#FROM tiangolo/uwsgi-nginx-flask:python3.6
FROM python:3.7
MAINTAINER sergei_kuzmin1@epam.com

ENV DB_HOST: ${{ secrets.DB_HOST }}
ENV DB_NAME: ${{ secrets.DB_NAME }}
ENV DB_USER: ${{ secrets.DB_USER }}
ENV DB_PASSWORD: ${{ secrets.DB_PASSWORD }}

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt

EXPOSE 80
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]
