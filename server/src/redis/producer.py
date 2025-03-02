from .config import Redis

class Producer:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    async def add_to_stream(self, data: dict, stream_name: str) -> bool:
        try:
            # Use zadd for Redis Streams
            await self.redis_client.execute_command('XADD', stream_name, '*', *sum(([k, v] for k, v in data.items()), []))
            return True
        except Exception as e:
            print(f"Error adding message to stream: {str(e)}")
            return False