FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY  blackemployer.com.crt /etc/ssl/blackemployer.com.crt
COPY  blackemployer.com.key /etc/ssl/blackemployer.com.key
COPY  ca.crt /etc/ssl/ca.crt
