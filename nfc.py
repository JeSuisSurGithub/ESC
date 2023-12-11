import time
import nfc

# Créez une instance de l'objet ContactlessFrontend pour le lecteur NFC I2C
clf = nfc.ContactlessFrontend('tty:AMA0:pn532')

def read_nfc():
    print("Approchez un tag NFC...")
    try:
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        print("Tag NFC lu :")
        print(tag)
    except Exception as e:
        print(f"Erreur lors de la lecture du tag NFC : {e}")

try:
    while True:
        read_nfc()
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    clf.close()
