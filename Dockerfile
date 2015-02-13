FROM python:2.7
ENV FOO bar
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
RUN pip install honcho
ADD . /code
