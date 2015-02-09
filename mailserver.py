import smtpd
import asyncore
import mail
import logins

class PrivateSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        print rcpttos

        for to in rcpttos:
            x = to.split('@')

            if len(x) != 2:
                continue

            usr, dom = x

            if dom == "privatemail.in":
                pk = logins.public_key(usr)

                if not pk:
                    continue

                mail.receive_message(usr, pk, str(data).encode("ascii"))

        return

server = PrivateSMTPServer(('0.0.0.0', 25), None)
#server = smtpd.DebuggingServer(('0.0.0.0', 25), None)

asyncore.loop()
