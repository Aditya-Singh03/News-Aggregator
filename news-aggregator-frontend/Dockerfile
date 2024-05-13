FROM node:alpine


WORKDIR /code

COPY ./package.json ./
RUN npm install -g embla-carousel-react
RUN npm install .

# Make sure you delete node_modules on your host, before building the image
COPY ./ ./

CMD ["npm", "run", "dev"]