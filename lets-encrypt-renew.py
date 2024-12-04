import os
import boto3
import paramiko
import logging
import time
from io import StringIO

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def update_route53(domain, txt_name, txt_value, hosted_zone_id):
    """Update Route 53 DNS TXT record."""
    logger.info(f"Updating Route 53 for domain {domain} with TXT {txt_name} = {txt_value}")
    route53 = boto3.client('route53')
    response = route53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': txt_name,
                        'Type': 'TXT',
                        'TTL': 60,
                        'ResourceRecords': [{'Value': f'"{txt_value}"'}],
                    }
                }
            ]
        }
    )
    return response

def ssh_command(host, username, private_key, command):
    """Run a command on the Lightsail instance via SSH."""
    logger.info(f"Running SSH command: {command}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key(StringIO(private_key))
    ssh.connect(hostname=host, username=username, pkey=key)
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode(), stderr.read().decode()

def main():
    # Retrieve secrets from environment variables
    lightsail_host = os.getenv("LIGHTSAIL_HOST")
    lightsail_user = os.getenv("LIGHTSAIL_USER")
    lightsail_private_key = os.getenv("LIGHTSAIL_PRIVATE_KEY")
    hosted_zone_id = os.getenv("ROUTE53_HOSTED_ZONE_ID")

    # Certbot command for DNS challenge
    certbot_command = "sudo certbot certonly --manual --preferred-challenges dns --manual-auth-hook '/path/to/hook-script.sh'"

    # Run Certbot to initiate challenge
    logger.info("Starting Let's Encrypt certificate request...")
    stdout, stderr = ssh_command(lightsail_host, lightsail_user, lightsail_private_key, certbot_command)

    # Mock extracting DNS challenge values (adjust based on Certbot's output)
    domain = "example.com"
    txt_name = "_acme-challenge.example.com"
    txt_value = "mock-txt-value"

    # Update Route 53 with DNS challenge
    update_route53(domain, txt_name, txt_value, hosted_zone_id)

    # Wait for DNS propagation
    logger.info("Waiting for DNS propagation...")
    time.sleep(300)  # Wait 5 minutes

    # Complete the Certbot process
    logger.info("Completing Certbot process...")
    complete_command = "sudo certbot renew"
    stdout, stderr = ssh_command(lightsail_host, lightsail_user, lightsail_private_key, complete_command)

    if stdout:
        logger.info(f"Certbot output: {stdout}")
    if stderr:
        logger.error(f"Certbot error: {stderr}")

    logger.info("Certificate renewal complete!")

if __name__ == "__main__":
    main()
