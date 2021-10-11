# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

#upgrade pip to latest version
RUN pip3 install --upgrade pip

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# install requirements
COPY ./requirements.txt /requirements.txt

RUN pip install -U -r /requirements.txt

# copy app files to "app" directory
COPY ./app /app