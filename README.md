# BeSecure3 to MQTT

MQTT wrapper around the python BiSecur Gateway 
It's based on library developed by [pysecur3](https://github.com/skelsec/pysecur3) @skelsec for Hormann Bisecure Gateway devices.

## Instalation

```bash
sudo mkdir /opt/bs2mqtt
sudo chown -R ${USER}: /opt/bs2mqtt

git clone https://github.com/Microweb/bs2mqtt.git /opt/bs2mqtt

cd /opt/bs2mqtt
./update.sh
bs2 scan # find available gateway device in your local networl
```

## Configuring

Before you start bs2mqtt (BeSecure3 to MQTT) you need to create file `configuration.json`


Open configuration file and write:

```bash
vi /opt/bs2mqtt/configuration.json
```

Basic configuration can looks like that:

```json
{
    "mqtt": {
        "base_topic": "bs3mqtt",
        "server": "mqtt://localhost",
        "user": "",
        "password": ""
    },
    "devices": {
        "1": "door1",
        "2": "gate1"
    }
}
```

## Starting bs2mqtt

```bash
bs3 serve --config /opt/bs2mqtt/configuration.json
```