FROM python:3-alpine

RUN apk add --update --no-cache ansible bash openssh
RUN ansible-galaxy collection install community.docker

WORKDIR /project

ENTRYPOINT []
CMD ["/bin/bash"]