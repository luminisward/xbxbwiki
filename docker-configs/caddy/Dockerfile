FROM abiosoft/caddy:php
ARG address
COPY ./Caddyfile /etc/tmpCaddyfile
RUN echo ${address} > /etc/Caddyfile && cat /etc/tmpCaddyfile >> /etc/Caddyfile
