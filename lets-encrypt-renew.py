import os
import paramiko
import logging
from io import StringIO

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def ssh_command(host, username, private_key, command):
    """Run a command on the Lightsail instance via SSH."""
    logger.info(f"Running SSH command: {command}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key(StringIO(private_key))
    ssh.connect(hostname=host, username=username, pkey=key)
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode(), stderr.read().decode()

def parse_final_certbot_output(output):
    """Extract final certificate details from Certbot output."""
    lines = output.splitlines()
    cert_paths = []
    for line in lines:
        if "Your certificate and chain have been saved at:" in line:
            cert_path = line.split(":")[1].strip()
            cert_paths.append(cert_path)
    return cert_paths

def main():
    # Retrieve secrets from environment variables
    lightsail_host = os.getenv("LIGHTSAIL_HOST")
    lightsail_user = os.getenv("LIGHTSAIL_USER")
    lightsail_private_key = os.getenv("LIGHTSAIL_PRIVATE_KEY")

    # Certbot command for non-interactive renewal
    certbot_command = "sudo certbot renew --non-interactive"

    # Run Certbot for renewal
    logger.info("Starting Let's Encrypt certificate renewal...")
    stdout, stderr = ssh_command(lightsail_host, lightsail_user, lightsail_private_key, certbot_command)

    # Log Certbot output
    logger.info(f"Certbot stdout:\n{stdout}")
    logger.error(f"Certbot stderr:\n{stderr}")

    # Parse Certbot output to extract renewed certificate paths
    logger.info("Parsing final Certbot output...")
    cert_paths = parse_final_certbot_output(stdout)

    if cert_paths:
        for path in cert_paths:
            logger.info(f"Certificate renewed and saved at: {path}")
    else:
        logger.warning("No certificates were renewed.")

    logger.info("Certificate renewal process complete!")

if __name__ == "__main__":
    main()
