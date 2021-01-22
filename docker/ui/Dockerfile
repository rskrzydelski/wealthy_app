# 1 stage: build React static files
FROM node:alpine as build

# create and set working directory
RUN mkdir /wealthy_ui
WORKDIR /wealthy_ui

COPY ./wealthy_ui/package.json /wealthy_ui/
COPY ./wealthy_ui/yarn.lock /wealthy_ui/
RUN yarn install

COPY ./wealthy_ui /wealthy_ui/

RUN yarn build

# 2 stage: copy React static files and start nginx
FROM nginx:stable-alpine
COPY --from=build /wealthy_ui/build /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]
