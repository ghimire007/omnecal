FROM python:3.10
WORKDIR /app

RUN apt-get update \
    && apt-get install binutils libproj-dev gdal-bin -y

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt
COPY ./ /app/

EXPOSE 7777


CMD [ "uvicorn", "main:app" ,"--host=0.0.0.0","--port" ,"7777" ]
