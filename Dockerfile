# Dockerfile

# pull the official docker image
FROM python:3.11-slim-buster

# set work directory
WORKDIR /app

# install dependencies
COPY requirements.txt . 
RUN pip install -r requirements.txt

# copy project
COPY . .


EXPOSE 8000

# launching the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
