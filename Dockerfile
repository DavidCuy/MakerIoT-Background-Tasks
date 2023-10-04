FROM python:3.7-slim

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt requirements.txt

# install dependencies
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main.py"]

