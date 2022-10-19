import asyncio
import contextlib
from http import client
import json
import random
import asyncio_mqtt as aiomqtt
import typing as t
import dataclasses as dc

from ..consts import MQTT_PREFIX, TIMER_INVERVAL
from ..bisecure import BiSecurClient
from ..config import read_config
from ..abc import ICommmand


async def print_command(messages):
    async for message in messages:
        print(f"command=", message.payload)


async def cancel_tasks(tasks):
    for task in tasks:
        if task.done():
            continue
        try:
            task.cancel()
            await task
        except asyncio.CancelledError:
            pass


async def timer(ctx, devices):
    await ctx.publish("/status", "online")
    while True:
        try:
            for device, port in devices:
                status = await ctx.read_device_status(port)
                await ctx.publish(f"/device/{device}", { "status": status, "port": port, "device": device })
            await asyncio.sleep(TIMER_INVERVAL)
        except asyncio.CancelledError:
            break


class Context:
    def __init__(self, mqtt, bisecur) -> None:
        self.mqtt = mqtt
        self.bisecur = bisecur

    async def publish(self, topic: str, value: str) -> None:
        await self.mqtt.publish(f"{MQTT_PREFIX}{topic}", json.dumps(value))

    async def read_device_status(self, port: int) -> str:
        return await self.bisecur.get_transition(port)


class ServeCommand(ICommmand):
    async def execute(self, args):
        config = await read_config(args.config)
        async with contextlib.AsyncExitStack() as stack:
            tasks = []
            stack.push_async_callback(cancel_tasks, tasks)
            while True:
                try:
                    mqtt = aiomqtt.Client(
                        client_id = config.mqtt.client_id,
                        hostname = config.mqtt.host,
                        port = config.mqtt.port,
                        username = config.mqtt.user,
                        password = config.mqtt.password,
                    )

                    await stack.enter_async_context(mqtt)
                    bisecur = BiSecurClient(config.bisecur)
                    await bisecur.login()

                    manager = mqtt.filtered_messages(f"{MQTT_PREFIX}/command")
                    messages = await stack.enter_async_context(manager)
                    task = asyncio.create_task(print_command(messages))
                    tasks.append(task)

                    # messages = await stack.enter_async_context(client.unfiltered_messages())
                    # task = asyncio.create_task(print_messages(messages, "[unfiltered] {}"))
                    # tasks.append(task)

                    task = asyncio.create_task(timer(Context(mqtt, bisecur), config.devices))
                    tasks.append(task)

                    await mqtt.subscribe(f"{MQTT_PREFIX}/#")

                    await asyncio.gather(*tasks)
                except aiomqtt.error.MqttError as ex:
                    print(ex)
                    await asyncio.sleep(10)

