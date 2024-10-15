FROM node:slim AS base

# Use /usr/src/app as the working directory of the container
WORKDIR /usr/src/app
COPY . /usr/src/app

# Install deps
RUN npm ci

# Build Next.js prod app
RUN npm run build 

EXPOSE 3000
CMD ["npm", "start"]
