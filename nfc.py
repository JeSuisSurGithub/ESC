import RPi.GPIO as GPIO
import MFRC522
import signal

def lire_uid_nfc():
    continue_reading = True

    def end_read(signal, frame):
        nonlocal continue_reading
        print("Lecture terminée")
        continue_reading = False
        GPIO.cleanup()

    signal.signal(signal.SIGINT, end_read)
    MIFAREReader = MFRC522.MFRC522()

    print("Passer le tag RFID à lire")

    while continue_reading:

        # Detecter les tags
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # Une carte est detectee
        if status == MIFAREReader.MI_OK:
            print("Carte détectée")

            # Recuperation UID
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:
                return uid

                # Clee d'authentification par defaut
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                # Selection du tag
                MIFAREReader.MFRC522_SelectTag(uid)

                # Authentification
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                if status == MIFAREReader.MI_OK:
                    MIFAREReader.MFRC522_Read(8)
                    MIFAREReader.MFRC522_StopCrypto1()
                else:
                    print("Erreur d'Authentification")

# Utilisez la fonction pour lire l'UID
uid_carte_nfc = lire_uid_nfc()
print("UID de la carte NFC détectée :", ".".join(map(str, uid_carte_nfc)))

