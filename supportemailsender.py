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
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>User Message</title>
</head>
<body style="font-family: Arial, sans-serif; text-align: center; margin: 50px;">

  <h1 style="color: #333;">Message from Admin</h1>

  <!-- Display the message from the admin -->
  <p style="margin-top: 20px; font-size: 18px;" id="admin-message">{username}</p>

  <!-- Additional text -->
  <p style="font-size: 18px;">Thank you for using our services. If you have any further questions or concerns, please don't hesitate to reach out to our support team.</p>

  <!-- Buttons for homepage and support page -->
  <a style="display: inline-block; margin: 10px; padding: 15px 30px; text-decoration: none; color: #FFF; background-color: #3498db; border-radius: 5px; font-size: 18px;" href="http://0.0.0.0:8000/">Homepage</a>
  <a style="display: inline-block; margin: 10px; padding: 15px 30px; text-decoration: none; color: #FFF; background-color: #3498db; border-radius: 5px; font-size: 18px;" href="http://0.0.0.0:8000/SupportPage">Support</a>

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
	
