# Launch a t2.micro (free tier) in your console OR via CLI:

# for linux/macOS
aws ec2 run-instances \
  --image-id ami-0f3caa1cf4417e51b \
  --instance-type t3.micro \
  --count 1 \
  --tag-specifications \
    'ResourceType=instance,Tags=[{Key=Environment,Value=dev},{Key=App,Value=myapp}]'

# for Windows
aws ec2 run-instances `
  --image-id ami-0f3caa1cf4417e51b `
  --instance-type t3.micro `
  --count 1 `
  --tag-specifications "ResourceType=instance,Tags=[{Key=Environment,Value=dev},{Key=App,Value=myapp},{Key=Name,Value=SecondPython}]"

# Note the InstanceId in the output — you'll see it in your script
# STOP it after testing (not terminate) to avoid charges:
# aws ec2 stop-instances --instance-ids i-XXXXXXXXX