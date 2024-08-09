# Etapa: Construção
FROM node:18-alpine

WORKDIR /main

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 8000

CMD ["npm", "run", "dev"]
