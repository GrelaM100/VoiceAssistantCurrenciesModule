import currencies_module as cm
import paho.mqtt.client as mqtt
import time

BROKER = "localhost"
# BROKER = "mqtt.lab.ii.agh.edu.pl"
ID = "grelam"


def send(topic, payload):
    global client
    print("snd", topic, payload)
    client.publish(topic, payload, retain=False)


def on_message(client, userdata, message):
    topic = message.topic
    payload = str(message.payload.decode("utf-8"))
    print("rcv", topic, payload)
    answer = cm.prepare_answer(payload.lower())
    if answer is not None:
        save_to_log('Q: ' + payload + '\n')
        save_to_log('A: ' + answer + '\n\n')
        send("cmd/tts/" + ID, answer)


def init():
    global client
    client = mqtt.Client(ID)
    client.on_message = on_message
    client.connect(BROKER)
    client.loop_start()
    client.subscribe(("sig/stt/#", 0))


def save_to_log(information):
    with open("log.txt", "a") as file_log:
        file_log.write(information)


if __name__ == '__main__':
    init()
    while True:
        time.sleep(1)
        # query = input()
        # print(cm.prepare_answer(query))
