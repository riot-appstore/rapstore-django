FROM node:8.9 as node

WORKDIR /app
COPY package.json /app/
RUN npm install
COPY ./ /app/
RUN npm install -g @angular/cli --unsafe-perm
