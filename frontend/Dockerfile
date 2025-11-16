# ============================
# 1. BUILD ANGULAR APP
# ============================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy only package files first (for caching)
COPY book_exchange/package*.json ./

RUN npm install --legacy-peer-deps

# Copy all Angular source
COPY book_exchange/ .

# Build Angular project
RUN npm run build


# ============================
# 2. NGINX FOR PRODUCTION
# ============================
FROM nginx:alpine

# Copy custom nginx config
COPY book_exchange/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built Angular files
COPY --from=builder /app/dist/book_exchange/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
