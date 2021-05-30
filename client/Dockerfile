# syntax=docker/dockerfile:1

FROM node:12.22

ENV NODE_ENV=production

WORKDIR /app

COPY ["package.json", "package-lock.json", "/app/"]

RUN npm ci --also=dev

COPY . /app

CMD [ "npm", "run", "build" ]