import asyncio
import random
from pysecur3.client import MCPClient

from .config import ConfigBiSecur

class BiSecurClient:
    def __init__(self, config: ConfigBiSecur) -> None:
        self.config = config
        self.client = MCPClient(config.ip, 4000, bytes.fromhex(config.source), bytes.fromhex(config.mac))

    async def login(self):
        pass
        # await asyncio.get_event_loop().run_in_executor(None, self.client.login, self.config.user, self.config.password)


    async def get_transition(self, port: int):
        return random.randint(0, 100)
        # return await asyncio.get_event_loop().run_in_executor(None, self.client.get_transition, port)
