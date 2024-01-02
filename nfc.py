# IMPORTE
# GPIO, MFRC522 et signal pour la lecture du capteur NFC
# timeout_decorator pour le timeout de 10 secondes
#
# PLAN DES DEFINITIONS
#
# FONCTIONS:
# Lecture de l'UID du tag nfc

import RPi.GPIO as GPIO
import MFRC522

from timeout_decorator import TimeoutError

import signal

import erreurs

def nfc_lire_uid():
    try:
        continue_reading = True

        def end_read(signal, frame):
            nonlocal continue_reading
            continue_reading = False
            GPIO.cleanup()

        signal.signal(signal.SIGINT, end_read)
        MIFAREReader = MFRC522.MFRC522()

        while continue_reading:

            # Détecter les tags
            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            # Une carte est detectee
            if status == MIFAREReader.MI_OK:

                # Récuperation UID
                (status, uid) = MIFAREReader.MFRC522_Anticoll()

                if status == MIFAREReader.MI_OK:
                    uid_hexa = "".join([format(int(part), '02X') for part in uid])
                    return (erreurs.OK_NFC_CAPTEUR_UID, uid_hexa)

                    # Clée d'authentification par defaut
                    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                    # Selection du tag
                    MIFAREReader.MFRC522_SelectTag(uid)

                    # Authentification
                    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                    if status == MIFAREReader.MI_OK:
                        MIFAREReader.MFRC522_Read(8)
                        MIFAREReader.MFRC522_StopCrypto1()
                    else:
                        return (erreurs.ER_NFC_CAPTEUR_AUTORISATION, None)
    except TimeoutError:
        return (erreurs.ER_NFC_CAPTEUR_TIMEOUT, None)