FROM python:3.7-alpine3.10
LABEL maintainer="Datadog Inc. <brett.langdon@datadoghq.com>"

# Working directory
WORKDIR /app

# Install psycopg requirements
RUN apk add --no-cache g++ gcc libgcc libstdc++ linux-headers make postgresql-dev python3-dev musl-dev

# install requirements
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the the rest of the app over
COPY . /app/

# Default command to run
CMD ["flask", "run", "--port=5000", "--host=0.0.0.0"]
