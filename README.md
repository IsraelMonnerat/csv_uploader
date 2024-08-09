CSV Uploader
Este projeto é uma aplicação para upload, consulta, e manipulação de arquivos CSV. A aplicação é dividida em um backend construído com Python e FastAPI, e um frontend em React.

Pré-requisitos
Docker: Certifique-se de que o Docker está instalado em sua máquina. Se você ainda não tem o Docker instalado, você pode baixá-lo e instalá-lo a partir do site oficial do Docker. (https://www.docker.com/products/docker-desktop/)
Instruções para execução
Clone o repositório:

bash
git clone https://github.com/IsraelMonnerat/csv_uploader.git
cd csv_uploader
Suba os containers com Docker Compose:

Na raiz do projeto, execute o comando abaixo para subir os containers:
docker compose up

Isso irá iniciar os serviços definidos no arquivo docker-compose.yml, incluindo o backend, frontend e banco de dados.

Acesse a aplicação:

Com os containers rodando, você pode acessar a aplicação no seu navegador através do endereço:

http://localhost:8000
Estrutura do Projeto
O projeto está organizado da seguinte forma:

bash
Copiar código
csv_uploader/
├── backend/
│   ├── src/
│   └── ...
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── ...
├── database/
│   ├── init.sql
│   ├── Dockerfile
│   └── ...
├── docker-compose.yml
└── README.md

----------------------
English

CSV Uploader
This project is an application for uploading, querying, and manipulating CSV files. The application is divided into a backend built with Python and FastAPI, and a frontend in React.

Prerequisites
Docker: Make sure Docker is installed on your machine. If you don't have Docker installed yet, you can download and install it from the official Docker website. (https://www.docker.com/products/docker-desktop/)
Instructions for Running
Clone the repository:

git clone https://github.com/IsraelMonnerat/csv_uploader.git
cd csv_uploader
Start the containers with Docker Compose:

In the root of the project, run the command below to start the containers:

docker compose up
This will start the services defined in the docker-compose.yml file, including the backend, frontend, and database.

Access the application:

With the containers running, you can access the application in your browser at:

arduino
Copiar código
http://localhost:8000
Project Structure
The project is organized as follows:

csv_uploader/
├── backend/
│   ├── src/
│   └── ...
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── ...
├── database/
│   ├── init.sql
│   ├── Dockerfile
│   └── ...
├── docker-compose.yml
└── README.md
