FROM node:11.12.0-alpine as build-vue
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./client/package*.json ./
RUN npm install
COPY ./client .
RUN npm run build

FROM nginx:1.17.6 AS build-python

# install python
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3 python3-venv

# virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# add and install requirements
RUN pip install --upgrade pip
COPY ./server/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

FROM nginx:1.17.6 AS production

# install python3 & netcat
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 netcat-openbsd

# copy Python dependencies from build image
COPY --from=build-python /opt/venv /opt/venv
# copy React app from react build image
COPY --from=build-vue /app/dist /usr/share/nginx/html

# copy nginx
# COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# set working directory
WORKDIR /app

# add permissions for nginx user
RUN chown -R nginx:nginx /app && chmod -R 755 /app && \
        chown -R nginx:nginx /var/cache/nginx && \
        chown -R nginx:nginx /var/log/nginx && \
        chown -R nginx:nginx /etc/nginx/conf.d
RUN touch /var/run/nginx.pid && \
        chown -R nginx:nginx /var/run/nginx.pid
USER nginx

# add Python app
COPY ./server .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV production
ENV APP_SETTINGS project.config.ProductionConfig
ENV PATH="/opt/venv/bin:$PATH"
ARG SECRET_KEY=my_precious
ENV SECRET_KEY $SECRET_KEY

# run server
CMD gunicorn -b 0.0.0.0:5000 app:app --daemon && \
      sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && \
      nginx -g 'daemon off;'
