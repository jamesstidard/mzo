# Builds the VuePress site and serves it with nginx on port 9012. Built by
# .github/workflows/image.yml into ghcr.io/jamesstidard/mzo-cli and run by the
# homelab's public host.
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run docs:build

FROM nginx:stable-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/docs/.vuepress/dist /usr/share/nginx/html
EXPOSE 9012
CMD ["nginx", "-g", "daemon off;"]
