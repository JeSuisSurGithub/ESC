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


