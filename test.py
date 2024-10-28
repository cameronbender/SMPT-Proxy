import smtplib

proxy_host = '127.0.0.1'
proxy_port = 2525

with smtplib.SMTP(proxy_host, proxy_port) as client:
    client.ehlo()
    client.starttls()  # This will only work if the proxy supports starttls
    client.sendmail('sender@example.com', 'recipient@example.com', 'Subject: Test\n\nThis is a test email.')
    print("Email sent through proxy.")