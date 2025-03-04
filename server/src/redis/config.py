import os
from dotenv import load_dotenv
#import aioredis 
from redis import asyncio as aioredis
from redis.commands.json.path import Path
import redis

load_dotenv()

class Redis():
    def __init__(self):
        self.REDIS_URL = os.environ.get("REDIS_HOST")
        self.REDIS_PORT = os.environ.get("REDIS_PORT")
        self.REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
        self.REDIS_DB = os.environ.get("REDIS_DB")
        self.REDIS_USER = os.environ.get("REDIS_USERNAME")

        self.connection_url =  f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_URL}:{self.REDIS_PORT}/{self.REDIS_DB}"

    async def create_connection(self):
        self.connection = aioredis.from_url(self.connection_url)

        return self.connection
    
    def create_rejson_connection(self):
        self.redisJson = redis.Redis(
            host=self.REDIS_URL, 
            port=self.REDIS_PORT, 
            username=self.REDIS_USER, 
            password=self.REDIS_PASSWORD, 
            decode_responses=True)
        
        return self.redisJson