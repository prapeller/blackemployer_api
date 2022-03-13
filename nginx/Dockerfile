FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY  ../app/app/settings/blackemployer.com.crt /etc/ssl/blackemployer.com.crt
COPY  ../app/app/settings/blackemployer.com.key /etc/ssl/blackemployer.com.key
COPY  ../app/app/settings/ca.crt /etc/ssl/ca.crt
