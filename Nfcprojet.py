import nfc

# Utilisez le port GPIO approprié pour votre connexion matérielle
# Remplacez '18' par le numéro de votre port GPIO si différent
port_gpio = '18'
clf = nfc.ContactlessFrontend(f'tty:AMA0:pn532:{port_gpio}')

print("NDEF Reader")

def read_nfc():
    print("\nScan a NFC tag\n")
    tag = clf.connect(rdwr={'on-connect': lambda tag: False})
    print(tag)

try:
    while True:
        read_nfc()
except KeyboardInterrupt:
    pass
finally:
    clf.close()
