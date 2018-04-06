FROM node:8.6 as node

WORKDIR /app
COPY package.json /app/
RUN npm install
COPY ./ /app/
RUN npm install -g @angular/cli --unsafe-perm
CMD ng serve --host=0.0.0.0
