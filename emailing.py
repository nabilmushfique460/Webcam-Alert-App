import smtplib
import mimetypes
import os
from email.message import EmailMessage

sender = "nabil29089@gmail.com"
password = "obqreebbidxalxnf"
receiver = "nabil29089@gmail.com"


def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "Someone Showed Up!"

    # It is good practice to set From and To headers to avoid spam filters
    email_message["From"] = sender
    email_message["To"] = receiver
    email_message.set_content("Hey, There is a man. Please response!")

    with open(image_path, 'rb') as file:
        content = file.read()

    # Dynamically detect image type using mimetypes instead of imghdr
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type and mime_type.startswith('image/'):
        subtype = mime_type.split('/')[1]
    else:
        subtype = 'png'  # Fallback subtype

    # Extract just the file name to display on the attachment
    filename = os.path.basename(image_path)

    # Attach the image properly with the filename included
    email_message.add_attachment(content, maintype="image", subtype=subtype, filename=filename)

    # Send the email
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, receiver, email_message.as_string())
    gmail.quit()



if __name__ == "__main__":
    send_email("Done")