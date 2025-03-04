# AI Chatbot Application

This project is a full-stack AI chatbot application inspired by [Stephen Sanwo's blog series](https://blog.stephensanwo.dev/build-a-fullstack-ai-chatbot/series).

## Features
- Interactive AI chatbot
- Full-stack implementation
- Real-time responses
- Redis-based message queue system

## Prerequisites
- Python 3.8 or higher
- pip package manager
- Redis server

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Set up environment variables:

   a. In the server directory, rename `.env1` to `.env` and configure:
   ```env
   # Server Configuration
   HOST=localhost
   PORT=8000

   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   MODEL_NAME=gpt-3.5-turbo

   # Redis Configuration
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_PASSWORD=your_redis_password_here
   ```

   b. In the worker directory, rename `.env1` to `.env` and configure:
   ```env
   # Worker Configuration
   WORKER_NAME=ai_chat_worker

   # Redis Configuration
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_PASSWORD=your_redis_password_here

   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   MODEL_NAME=gpt-3.5-turbo
   ```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Redis server:
```bash
redis-server
```

2. Start the server (in the server directory):
```bash
cd server
python main.py
```

3. Start the worker (in a new terminal, in the worker directory):
```bash
cd worker
python main.py
```

## Important Notes
- Replace `your_openai_api_key_here` with your actual OpenAI API key
- Ensure Redis password matches your Redis server configuration
- Both server and worker must use the same Redis configuration
- Verify that the HOST and PORT values match your desired server setup

## Contributing
Feel free to submit issues and pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Thanks to [Stephen Sanwo](https://blog.stephensanwo.dev/) for the original tutorial