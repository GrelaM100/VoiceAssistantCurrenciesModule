import paho.mqtt.client as mqtt
import speech_recognition as sr

BROKER = "localhost"
# BROKER = 'mqtt.lab.ii.agh.edu.pl'


def send(topic, payload):
    global client
    client.publish(topic, payload, retain=False)


def on_message(client, userdata, message):
    topic = message.topic
    payload = str(message.payload.decode("utf-8"))


def init():
    global client
    global recognizer

    client = mqtt.Client("mic-pc")
    client.connect(BROKER)
    client.loop_start()
    #  client.subscribe([("xxxcmd/tts/pc",0),("ola/#",0)])

    recognizer = sr.Recognizer()


def loop():
    global recognizer
    while True:
        tekst = input(">>")
        if len(tekst) > 0:
            send("sig/stt/pc", tekst)
        else:
            with sr.Microphone() as source:
                print("slucham ...")
                audio = recognizer.listen(source)
                try:
                    tekst = recognizer.recognize_google(audio, language='pl_PL')
                    send("sig/stt/pc", tekst)
                    print(tekst)
                    if tekst == 'koniec':
                        break
                except sr.UnknownValueError:
                    print('nie rozumiem')
                except sr.RequestError as e:
                    print('error:', e)


if __name__ == '__main__':
    init()
    loop()

