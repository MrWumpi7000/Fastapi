import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def SendEmail(email, NameofUser):
	username = NameofUser
# Email configuration
	sender_email = "no-reply@freundchenmail.net"
	receiver_email = email
	subject = "Welcome to Our Community!"
	html_body = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You for Your Support</title>
</head>
<body style="font-family: 'Arial', sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">

    <div style="max-width: 600px; margin: 20px auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
        <h1 style="color: #333;">Thank You for Your Support!</h1>
        <p style="color: #555;">Dear {username},</p>
        <p style="color: #555; line-height: 1.6;">We sincerely appreciate your support. Your contribution makes a significant impact, and we couldn't be more grateful.</p>
        <p style="color: #555;">If you have any questions or need further assistance, feel free to reach out to us.</p>
        <p style="color: #555;">Best regards,<br>MrWumpi3000's Team</p>
    </div>

</body>
</html>

"""
	
	# SMTP server configuration for Gmail
	smtp_server = "w00d7872.kasserver.com"
	smtp_port = 25  # StartTLS port
	
	# Create the email message
	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = receiver_email
	message["Subject"] = subject
	html_part = MIMEText(html_body, "html")
	message.attach(html_part)
	# Connect to the SMTP server using StartTLS
	server = smtplib.SMTP(smtp_server, smtp_port)
	server.starttls()
	
	# Login to the email account
	server.login(sender_email, "jpjpT85gwEJM7Xy7R8wW")
	
	# Send the email
	server.sendmail(sender_email, receiver_email, message.as_string())
	
	# Quit the server
	server.quit()
	
	print("Email sent successfully!")
	