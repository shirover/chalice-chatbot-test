# Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy source files
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Argument for nginx config file (default to nginx.conf)
ARG NGINX_CONF=nginx.conf

# Copy custom nginx config
COPY ${NGINX_CONF} /etc/nginx/conf.d/default.conf

# Copy built files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Create directory for SSL certificates
RUN mkdir -p /etc/nginx/ssl

# Expose ports
EXPOSE 80 443

# Start nginx
CMD ["nginx", "-g", "daemon off;"]