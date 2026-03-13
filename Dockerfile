# Dockerfile
# Use Nginx as a lightweight web server
FROM nginx:alpine

# Copy your app files (e.g., index.html) into the container
COPY index.html /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Nginx runs automatically as the container's entrypoint
