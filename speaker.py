import paho.mqtt.client as mqtt
import time
import pyttsx3 as tts

BROKER = "localhost"
# BROKER = "mqtt.lab.ii.agh.edu.pl"

def send(topic, payload):
    global client
    client.publish(topic, payload, retain=False)


def on_message(client, userdata, message):
    global kk

    topic = message.topic
    payload = str(message.payload.decode("utf-8"))

    print("rcv", topic, payload)
    kk.append(payload)


def init():
    global client
    client = mqtt.Client("spk-pc")
    client.on_message = on_message
    print("connecting to broker")
    client.connect(BROKER)
    client.loop_start()
    client.subscribe(("cmd/tts/grelam", 0))


def loop():
    global kk
    engine = tts.init()
    engine.setProperty('volume', 0.7)
    engine.setProperty('rate', 190)

    kk = []

    while True:
        while len(kk) > 0:
            engine.say(kk.pop(0))
            engine.runAndWait()
            time.sleep(1)


if __name__ == '__main__':
    init()
    loop()
