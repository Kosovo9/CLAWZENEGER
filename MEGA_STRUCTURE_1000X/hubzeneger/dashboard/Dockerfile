
FROM node:18-alpine as build

WORKDIR /app
COPY package.json package-lock.json* ./
# Generar lock si no existe para evitar error en npm ci
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
# Config nginx básica para SPA
RUN echo 'server { listen 80; root /usr/share/nginx/html; index index.html; location / { try_files $uri $uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf
EXPOSE 80
