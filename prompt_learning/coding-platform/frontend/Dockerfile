FROM node:18-alpine

# Install dependencies for development
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all application files
COPY . .

# Expose port
EXPOSE 3000

# Set environment variables
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=development

# Run in development mode (no build step)
CMD ["npm", "run", "dev"]
