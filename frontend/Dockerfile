# Use official NGINX image as base
FROM nginx:alpine

# Set working directory inside the container
WORKDIR /usr/share/nginx/html

# Remove default NGINX website
RUN rm -rf ./*

# Copy your frontend files (HTML, CSS, JS) into container
COPY . .

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# NGINX will automatically serve the files
CMD ["nginx", "-g", "daemon off;"]
