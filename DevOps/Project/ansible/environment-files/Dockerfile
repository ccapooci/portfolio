FROM python:3-alpine

RUN apk add --update --no-cache bash
RUN apk add nodejs
RUN apk add npm

# https://docs.docker.com/engine/reference/builder/#expose
# Does not publish port, need -p on docker run.
EXPOSE 3000/tcp

WORKDIR /coffee-project

COPY coffee-project ./
RUN npm install
CMD ["node", "app.js"]