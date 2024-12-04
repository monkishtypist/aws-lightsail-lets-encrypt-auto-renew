import boto3
import paramiko
import os
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# AWS Clients
route53 = boto3.client('route53')
secretsmanager = boto3.client('secretsmanager')

def get_secret(secret_name):
    """Retrieve a secret from AWS Secrets Manager."""
    response = secretsmanager.get_secret_value(SecretId=secret_name)
    return response['SecretString']

def update_route53(domain, txt_name, txt_value):
    """Update TXT record for domain validation."""
    logger.info(f"Updating Route 53 for {domain} with TXT {txt_name} = {txt_value}")
    hosted_zone_id = os.environ['ROUTE53_HOSTED_ZONE_ID']
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
    """Execute a command on the Lightsail instance via SSH."""
    logger.info(f"Connecting to {host} via SSH to run: {command}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key(private_key)
    ssh.connect(host, username=username, pkey=key)
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode(), stderr.read().decode()

def renew_certificate():
    """Main process to renew Let's Encrypt certificate."""
    logger.info("Starting certificate renewal process")
    # Get Lightsail SSH details from Secrets Manager
    lightsail_secret = get_secret("LIGHTSAIL_SECRET_NAME")
    ssh_host = lightsail_secret['host']
    ssh_user = lightsail_secret['user']
    private_key_data = lightsail_secret['private_key']

    private_key = paramiko.RSAKey.from_private_key_string(private_key_data)

    # Certbot command for DNS challenge
    certbot_command = "sudo certbot certonly --manual --preferred-challenges dns"

    # Run certbot on Lightsail instance
    stdout, stderr = ssh_command(ssh_host, ssh_user, private_key, certbot_command)
    logger.info(f"Certbot output: {stdout}")
    if stderr:
        logger.error(f"Certbot error: {stderr}")

    # Extract DNS challenge details
    # (You'll need to parse stdout to get the domain and TXT value)

    domain = "example.com"
    txt_name = "_acme-challenge.example.com"
    txt_value = "sample-value"

    # Update Route 53 with the TXT record
    update_route53(domain, txt_name, txt_value)

    # Wait for DNS propagation
    logger.info("Waiting for DNS propagation...")
    time.sleep(300)  # 5 minutes

    # Complete the challenge (rerun certbot)
    complete_command = "sudo certbot renew"
    stdout, stderr = ssh_command(ssh_host, ssh_user, private_key, complete_command)
    logger.info(f"Renewal output: {stdout}")
    if stderr:
        logger.error(f"Renewal error: {stderr}")

    logger.info("Certificate renewal complete!")

if __name__ == "__main__":
    renew_certificate()
