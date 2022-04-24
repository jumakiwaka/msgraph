FROM node:14.15.1 as builder
RUN npm install webpack -g


RUN mkdir -p /opt/app
COPY . /opt/app
WORKDIR /opt/app/
RUN npm install
RUN npm run build

FROM nginx:1.21.6 as nginx
COPY conf/nginx-template.conf /etc/nginx/nginx.conf
RUN rm /usr/share/nginx/html/*

COPY --from=builder /opt/app/build /usr/share/nginx/html
WORKDIR /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]
