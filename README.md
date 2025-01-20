# SimpleChatbot

## How to Build

1. Clone the repository
2. Create a copy of .env.example and name it .env
3. Replace the values in <> for your own values in the .env file
4. Open a terminal in the root of the repository and run:
```
docker compose build
docker compose up -d
```
This will create 2 docker containers:
- Backend container running in localhost:8000
- MariaDB container running in localhost:3306

## How to Run 

Go to the following url to start a conversation with the chatbot:
```
http://localhost:8000/bot
```