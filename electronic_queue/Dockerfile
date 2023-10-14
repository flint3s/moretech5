FROM python:3.10

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN apt-get install gcc

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["python", "./add_statistics.py"]
