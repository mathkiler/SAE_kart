import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# Configuration des GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_INPUT_PIN = 12  # GPIO pour recevoir l'activation MLI 
GPIO_OUTPUT_PIN = 13  # GPIO pour activer la charge 
GPIO.setup(GPIO_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(GPIO_OUTPUT_PIN, GPIO.OUT)

# Configuration MQTT
BROKER = "localhost"  
PORT = 1883  # Port par défaut pour MQTT
TOPIC_MLI = "charge/mli"
TOPIC_CONTROL = "charge/control"

# Fonction appelée lorsque le client reçoit un message MQTT
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        topic = msg.topic

        if topic == TOPIC_CONTROL:
            if payload == "ON":
                GPIO.output(GPIO_OUTPUT_PIN, GPIO.HIGH)
                client.publish("charge/status", "ON")
            elif payload == "OFF":
                GPIO.output(GPIO_OUTPUT_PIN, GPIO.LOW)
                client.publish("charge/status", "OFF")

    except Exception as e:
        print(f"Erreur lors du traitement du message: {e}")

# Initialisation du client MQTT
client = mqtt.Client()
client.on_message = on_message

try:
    client.connect(BROKER, PORT, 60)
    client.subscribe([(TOPIC_MLI, 0), (TOPIC_CONTROL, 0)])

    client.loop_start()

    while True:
        # Vérifie l'état du GPIO_INPUT_PIN
        if GPIO.input(GPIO_INPUT_PIN) == GPIO.HIGH:
            client.publish(TOPIC_MLI, "ON")
        else:
            client.publish(TOPIC_MLI, "OFF")

        time.sleep(1)  # Pause pour éviter une surcharge

except KeyboardInterrupt:
    print("Interruption par l'utilisateur")

finally:
    print("Nettoyage GPIO et déconnexion MQTT")
    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()
