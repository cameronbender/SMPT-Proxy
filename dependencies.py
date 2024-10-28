import ssl
import smtplib
import asyncio

# SSL dependency setup
def create_ssl_context(certfile, keyfile):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    return context

# SSL certificates
CERTFILE = "path/to/cert.pem"
KEYFILE = "path/to/key.pem"

# SMTP server details
SMTP_SERVER = "smtp.yourmailserver.com"
SMTP_PORT = 587  # Change if your server requires SSL directly

async def handle_client(reader, writer, sender=None, recipient=None):
    client_address = writer.get_extra_info("peername")
    print(f"Received connection from {client_address}")

    try:
        # Establish connection to the actual SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=create_ssl_context(CERTFILE, KEYFILE))

            while True:
                data = await reader.read(1024)
                if not data:
                    break
                message = data.decode()
                print(f"Received message: {message}")
                server.sendmail(from_addr=sender, to_addrs=recipient, msg=message)
                writer.write(b"250 OK\r\n")
                await writer.drain()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 2525)
    async with server:
        await server.serve_forever()

# Run the proxy server
asyncio.run(main())