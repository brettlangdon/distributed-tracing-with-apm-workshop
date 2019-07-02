FROM node:12-alpine
LABEL maintainer="Datadog Inc. <brett.langdon@datadoghq.com>"

# Create app directory
WORKDIR /app

# Install system dependencies
RUN apk --no-cache add g++ gcc libgcc libstdc++ linux-headers make python

# Install dependencies
COPY package*.json ./
RUN npm install -g nodemon
RUN npm install

# Copy application code
COPY . /app/

# Default command to run
CMD ["nodemon", "server.js"]
