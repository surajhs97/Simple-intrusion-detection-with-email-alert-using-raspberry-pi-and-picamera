import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.image import MIMEImage

def mailAlert(path):
    #sender's email id
    fromaddr = ""
    #Sender's password
    password = ""
    #Receiver's email id
    toaddr = ""

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Intrusion detected"
    body = "Image of the intrusion"
    msg.attach(MIMEText(body, 'plain'))

    #Attach the image
    fp = open(path,'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr,password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

    print "Email sent"

