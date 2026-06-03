# Launch a t2.micro (free tier) in your console OR via CLI:
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t2.micro \
  --count 1 \
  --tag-specifications \
    'ResourceType=instance,Tags=[{Key=Environment,Value=dev},{Key=App,Value=myapp}]'

# Note the InstanceId in the output — you'll see it in your script
# STOP it after testing (not terminate) to avoid charges:
# aws ec2 stop-instances --instance-ids i-XXXXXXXXX