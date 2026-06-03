# All instances tagged Environment=dev
python ec2_lister.py --tag-key Environment --tag-value dev

# Only running ones
python ec2_lister.py --tag-key Environment --tag-value dev --state running

# Different region, different tag
python ec2_lister.py --region us-west-2 --tag-key App --tag-value myapp