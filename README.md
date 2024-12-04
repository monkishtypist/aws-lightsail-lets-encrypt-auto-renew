
## SECRETS

#### LIGHTSAIL_HOST (Public IP)

**What It Is:** The public IP address of your AWS Lightsail instance.

**Where to Find It:**

- Navigate to the AWS Lightsail Console.
- Select your instance from the list.
- Find the Public IP Address in the instance details section. You already have this, so you’re good here.

#### LIGHTSAIL_USER (SSH Username)

**What It Is:** The username used to connect to your Lightsail instance via SSH.

**Default Values:**

- If you used a Bitnami-based Lightsail instance, the default username is likely `bitnami`.
- For Ubuntu-based instances, it’s typically `ubuntu`.

#### LIGHTSAIL_PRIVATE_KEY

**What It Is:** The private SSH key (PEM file) you use to connect to the Lightsail instance.

**Where to Find It:**

- If you downloaded the private key when creating your Lightsail instance, it’s on your local system.
- The default filename is something like LightsailDefaultKey-us-west-2.pem (region-specific).

#### ROUTE53_HOSTED_ZONE_ID

**What It Is:** The unique identifier of your Route 53 hosted zone.

**Where to Find It:**

- Navigate to the Route 53 Console in AWS.
- Select Hosted Zones from the navigation pane.
- Find your domain in the list and click on it.
- Look for the Hosted Zone ID at the top (e.g., Z3M3LMPEXAMPLE).

### Storing Secrets in GitHub Actions

Once you’ve gathered all the information:

1. Navigate to `Settings > Secrets and variables > Actions` in your GitHub repository.
2. Create the following secrets:
   - LIGHTSAIL_HOST: Your Lightsail public IP.
   - LIGHTSAIL_USER: Your SSH username (bitnami or ubuntu).
   - LIGHTSAIL_PRIVATE_KEY: Paste the entire content of your PEM file.
   - ROUTE53_HOSTED_ZONE_ID: Your hosted zone ID from Route 53.