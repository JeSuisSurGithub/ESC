import nfcpy
import signal

def on_connect(tag):
    print("Tag detected:", tag.identifier)

def on_signal(signal, frame):
    print("Exiting program.")
    clf.close()
    exit(0)

signal.signal(signal.SIGINT, on_signal)

# Créer une instance du lecteur NFC
clf = nfcpy.ContactlessFrontend()

try:
    print("Scanning for NFC tags. Press Ctrl+C to exit.")
    clf.connect(rdwr={'on-connect': on_connect})
    while True:
        pass
except KeyboardInterrupt:
    pass
finally:
    clf.close()



import RPi.GPIO as GPIO
import spidev
import signal
import time

def on_signal(signal, frame):
    print("Exiting program.")
    GPIO.cleanup()
    spi.close()
    exit(0)

signal.signal(signal.SIGINT, on_signal)

# Configuration des broches
RST_PIN = 25
SCK_PIN = 11
MOSI_PIN = 10
MISO_PIN = 9
SS_PIN = 8

# Initialisation de RPi.GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RST_PIN, GPIO.OUT)

# Initialisation de spidev
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

def read_nfc_tag():
    # Mise à jour du GPIO pour réinitialiser le MFRC522
    GPIO.output(RST_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(RST_PIN, GPIO.HIGH)
    time.sleep(0.1)

    # Envoie la commande d'initialisation du MFRC522
    spi.xfer2([0x01, 0x0D << 1, 0x07 << 1, 0x52, 0x00])

    # Envoie la commande de lecture du MFRC522
    response = spi.xfer2([0x02, 0x30, 0x80, 0x00, 0x00])

    # Lit les données de la balise
    if response[1] == 0x30:
        uid = response[2:7]
        return uid
    else:
        return None

try:
    print("Scanning for NFC tags. Press Ctrl+C to exit.")
    while True:
        uid = read_nfc_tag()
        if uid:
            print("Tag UID:", ":".join("{:02x}".format(byte) for byte in uid))
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    spi.close()
