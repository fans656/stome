FROM node:latest
WORKDIR /code
COPY package.json package-lock.json .babelrc next.config.js /code/
RUN npm install
COPY pages/ /code/pages/
COPY src/ /code/src/
RUN npm run build && npm run export
