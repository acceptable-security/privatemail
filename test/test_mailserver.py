import smtplib
import email.utils
from email.mime.text import MIMEText

# Create the message
msg = MIMEText('This is the body of the message.')
msg['To'] = email.utils.formataddr(('Recipient', 'bsmith@privatemail.in'))
msg['From'] = email.utils.formataddr(('Author', 'nsa@google.com'))
msg['Subject'] = 'we r watching'

server = smtplib.SMTP('localhost', 25)
server.set_debuglevel(True) # show communication with the server
try:
    server.sendmail('nsa@google.com', ['bsmith@privatemail.in'], msg.as_string())
finally:
    server.quit()
