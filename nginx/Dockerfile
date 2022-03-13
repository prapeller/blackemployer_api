FROM nginx:alpine

COPY default.conf /etc/nginx/conf.d/default.conf

#COPY  blackemployer.com.crt /etc/ssl/blackemployer.com.crt
#COPY  blackemployer.com.key /etc/ssl/blackemployer.com.key
#COPY  ca.crt /etc/ssl/ca.crt

RUN sudo apt update
RUN sudo apt install snapd
RUN sudo snap install core; sudo snap refresh core

RUN sudo snap install --classic certbot
RUN sudo ln -s /snap/bin/certbot /usr/bin/certbot
RUN sudo certbot --nginx
RUN sudo certbot renew --dry-run
