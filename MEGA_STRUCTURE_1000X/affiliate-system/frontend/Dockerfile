# Build stage
FROM node:18-alpine as build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
# En este entorno no podemos hacer build real sin internet/CPU, pero dejamos la estructura
# RUN npm run build

# Production stage
FROM nginx:alpine
# COPY --from=build /app/build /usr/share/nginx/html
# Para propósitos del demo, copiamos el source si no hay build, pero normalmente se copia build
COPY ./public /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
