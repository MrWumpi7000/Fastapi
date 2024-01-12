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
  <title>Welcome to Our Community!</title>
</head>
<body style="font-family: 'Arial', sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">

  <div style="text-align: center; padding: 20px; background-color: #fff; border-radius: 10px; max-width: 600px; margin: 20px auto; box-shadow: 0 0 10px rgba(0,0,0,0.1);">

    <h1 style="color: #3498db;">Welcome to Our Community!</h1>
    <p style="color: #555;">Dear {username},</p>
    <p style="color: #555;">Thank you for joining our community. We're thrilled to have you on board!</p>
    <p style="color: #555;">Click the button below to visit our Home page:</p>

    <a href="http://0.0.0.0:8000/" style="display: inline-block; padding: 10px 20px; background-color: #3498db; color: #fff; text-decoration: none; border-radius: 5px; transition: background-color 0.3s;" onmouseover="this.style.backgroundColor='#297fb8'" onmouseout="this.style.backgroundColor='#3498db'">Home Page</a>

    <p style="color: #555;">If you have any questions or need assistance, feel free to reach out. We're here to help!</p>

    <p style="color: #555;">Best regards,<br>Your MrWumpi3000's Team</p>
  </div>

  <script>
    // JavaScript for button hover effect
    document.querySelector('a').addEventListener('mouseover', function() {{
      this.style.backgroundColor = '#297fb8';
    }});

    document.querySelector('a').addEventListener('mouseout', function() {{
      this.style.backgroundColor = '#3498db';
    }});
  </script>

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
	
