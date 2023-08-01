FROM node:16-alpine
WORKDIR /MAR-frontend
RUN rm -rf ./*
COPY . .
RUN npm i --legacy-peer-deps
RUN npm run build