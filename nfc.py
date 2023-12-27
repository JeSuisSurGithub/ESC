# Décommenter sur RPi
# import RPi.GPIO as GPIO
# import MFRC522
# import signal
from timeout_decorator import TimeoutError
import erreurs

def lire_uid_nfc() -> str:
    # Commenter sur RPi
    return (erreurs.ER_NFC_CAPTEUR_DESACTIVE, None)
    try:
        continue_reading = True

        def end_read(signal, frame):
            nonlocal continue_reading
            continue_reading = False
            GPIO.cleanup()

        signal.signal(signal.SIGINT, end_read)
        MIFAREReader = MFRC522.MFRC522()

        while continue_reading:

            # Detecter les tags
            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            # Une carte est detectee
            if status == MIFAREReader.MI_OK:

                # Recuperation UID
                (status, uid) = MIFAREReader.MFRC522_Anticoll()

                if status == MIFAREReader.MI_OK:
                    uid_hexa = "".join([format(int(part), '02X') for part in uid])
                    return (erreurs.OK_NFC_CAPTEUR_UID, uid_hexa)

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
                        return (erreurs.ER_NFC_CAPTEUR_AUTORISATION, None)
    except TimeoutError:
        return (erreurs.ER_NFC_CAPTEUR_TIMEOUT, None)