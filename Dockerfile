# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

# Make sure in the logs that we have all the files we need
RUN ls -l
COPY . ./
RUN ls -l

# Install production dependencies
RUN pip install --no-cache-dir -r src/requirements.txt

# Kedro dependency
RUN mkdir -p /app/conf/local

# Start the pipeline
RUN kedro run