import json
import typing as t
import dataclasses as dc
import aiofiles


@dc.dataclass(slots=True, frozen=True)
class ConfigMqtt:
    base_topic: str = "bs3mqtt"
    client_id: str = "bs3mqtt"
    host: str = "localhost"
    port: int = 1883
    user: str = None
    password: str = None


@dc.dataclass(slots=True, frozen=True)
class ConfigBiSecur:
    ip: str
    mac: str
    user: str
    password: str
    source: str = "FF:FF:FF:FF:FF:FF".replace(".", "")


@dc.dataclass(slots=True, frozen=True)
class Config:
    mqtt: ConfigMqtt
    bisecur: ConfigBiSecur
    devices: t.List


async def read_config(path: str) -> Config:
    try:
        async with aiofiles.open(path) as f:
            text = await f.read()
            data = json.loads(text)
    except FileNotFoundError:
        print(f"Not found config file: {path}")
    else:
        mqtt = {}
        bisecur = {}
        if "mqtt" in data:
            names = [field for field in dc.fields(ConfigMqtt)]
            mqtt = {name: data['mqtt'][name] for name in names if name in data['mqtt']}

        bisecur = {
            field.name: data['bisecur'][field.name]
            for field in dc.fields(ConfigBiSecur)
        }

        return Config(
            mqtt = ConfigMqtt(**mqtt),
            bisecur = ConfigBiSecur(**bisecur),
            devices = list(data['devices'].items())
        )

