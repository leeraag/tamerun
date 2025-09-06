# pull official base image
FROM node:22-alpine3.22

# set working directory
WORKDIR /opt/build

# add `/app/node_modules/.bin` to $PATH
ENV PATH=/opt/build/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
#COPY package-lock.json ./
COPY yarn.lock ./
RUN yarn install

# add app
COPY . ./

EXPOSE 80

# start app
CMD ["yarn", "dev"]
