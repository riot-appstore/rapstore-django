FROM node:8.9 as node

WORKDIR /app
RUN npm install npm@latest -g
COPY package.json /app/
RUN npm install
COPY ./ /app/
RUN npm install -g @angular/cli --unsafe-perm
RUN test -z "$NGBUILD" && ng build --prod --aot=false  $AFLAGS
