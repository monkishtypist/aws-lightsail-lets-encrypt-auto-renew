#!/bin/bash
# Certbot Authentication Hook: Updates Route 53 DNS records for Let's Encrypt validation.

DOMAIN="_acme-challenge.$CERTBOT_DOMAIN"
VALUE=$CERTBOT_VALIDATION
HOSTED_ZONE_ID=$ROUTE53_HOSTED_ZONE_ID

# Log for debugging
echo "Updating DNS record for domain $DOMAIN with value $VALUE"

# Add the DNS TXT record to Route 53
aws route53 change-resource-record-sets \
    --hosted-zone-id "$HOSTED_ZONE_ID" \
    --change-batch "{\"Changes\":[{\"Action\":\"UPSERT\",\"ResourceRecordSet\":{\"Name\":\"$DOMAIN\",\"Type\":\"TXT\",\"TTL\":60,\"ResourceRecords\":[{\"Value\":\"\\\"$VALUE\\\"\"}]}}]}"
