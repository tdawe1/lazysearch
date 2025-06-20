import smtplib, mimetypes
from email.message import EmailMessage

def send_application(to_email, subject, body, resume_pdf, sender_email, password):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email
    msg.set_content(body)

    ctype, _ = mimetypes.guess_type(resume_pdf)
    maintype, subtype = ctype.split('/')
    with open(resume_pdf, 'rb') as f:
        msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename="resume.pdf")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)
