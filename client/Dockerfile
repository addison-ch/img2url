# Build stage
FROM node:20-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of the application
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Expose ports
EXPOSE 80
EXPOSE 443