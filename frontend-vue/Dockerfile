FROM nginx

COPY ./default.template.conf /tmp/

COPY ./entrypoint.sh /usr/bin/

COPY ./dist /usr/share/nginx/html

ENTRYPOINT [ "/usr/bin/entrypoint.sh" ]
CMD ["nginx", "-g", "daemon off;"]