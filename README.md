## ACCESS CONTROL

### **Step 1: Create an IAM User with Route 53 Permissions**

1.  **Go to the AWS Management Console**: Navigate to **IAM** > **Users**.
    
2.  **Create a New User**:
    
    -   Click **Create User**
    -   Enter a username (e.g., `Route53-access`)
    -   Select **Access Key - Programmatic access** [DEPRECATED]
    -   Click **Next**

3.  **Assign Permissions**:
    
    -   Choose **Attach policies directly**
    -   Add the **AmazonRoute53FullAccess** policy
    -   Click **Next** and **Create User**

4.  **Create and Download Credentials**:
    
    -   After creation, click the newly created user
    -   Click **Create access key**
    -   Select **Application running outside AWS**
    -   Click **Next** then **Create access key**
    -   Download the **Access Key ID** and **Secret Access Key** - save these securely—you won’t be able to retrieve them later
    -   Click **Done**

### **Step 2: Set Environment Variables Locally**

1.  Open your terminal or command prompt.
    
2.  Set the credentials and region:
    
    ```bash    
    export AWS_ACCESS_KEY_ID=your-access-key-id export AWS_SECRET_ACCESS_KEY=your-secret-access-key export AWS_DEFAULT_REGION=your-region
    ```
    
    Replace:
    
    -   `your-access-key-id` with the **Access Key ID**.
    -   `your-secret-access-key` with the **Secret Access Key**.
    -   `your-region` with your AWS region (e.g., `us-east-1`).

3.  Verify the credentials:
    
    ```bash
    aws sts get-caller-identity
    ```
    
    This command should return a JSON response with your account details if the credentials are valid.

## SECRETS

#### AWS_ACCESS_KEY_ID

**What It Is:** The access key created for your *Route53-access* user.

**Where to Find It:**

- Created when you created your *Route53-access* user [credentials](#step-1-create-an-iam-user-with-route-53-permissions) above.

#### AWS_SECRET_ACCESS_KEY

**What It Is:** The secret access key created for your *Route53-access* user.

**Where to Find It:**

- Created when you created your *Route53-access* user [credentials](#step-1-create-an-iam-user-with-route-53-permissions) above.

#### AWS_DEFAULT_REGION

**What It Is:** The default region for your AWS account.

**Where to Find It:**

- Log in to the AWS Management Console.
- Look at the top-right corner of the console.
- The displayed region (e.g., `US West (Oregon)` or `us-west-2`) is your currently active region. This is often the default region for your account.

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