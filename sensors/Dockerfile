FROM python:3.7-alpine3.10
LABEL maintainer="Datadog Inc. <brett.langdon@datadoghq.com>"

# Working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache g++ gcc libgcc libstdc++ linux-headers make postgresql-dev python3-dev musl-dev build-base eudev-dev openzwave openzwave-dev

# Install python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy application code
COPY . /app/

# Default command
CMD ["flask", "run", "--port=5001", "--host=0.0.0.0"]
