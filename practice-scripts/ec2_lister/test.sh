# All instances tagged Environment=dev
python ec2_lister.py --tag-key Environment --tag-value dev

# Output:
# (.venv) PS D:\HCI_Academy\python-devops\practice-scripts\ec2_lister> python ec2_lister.py --region us-east-1
#                                         EC2 instances — us-east-1                                        
# ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
# ┃ ID                  ┃ Name         ┃ Type     ┃ State   ┃ AZ         ┃ Private IP    ┃ Public IP      ┃
# ┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
# │ i-0a7ed0f26c6a01d56 │ SecondPython │ t3.micro │ running │ us-east-1d │ 172.31.41.16  │ 54.196.123.163 │
# │ i-0ed20b7a96ee29cd3 │ FirstPython  │ t3.micro │ stopped │ us-east-1d │ 172.31.32.188 │ —              │
# └─────────────────────┴──────────────┴──────────┴─────────┴────────────┴───────────────┴────────────────┘
# Total: 2 instance(s)

# Only running ones
python ec2_lister.py --tag-key Environment --tag-value dev --state running

# Different region, different tag
python ec2_lister.py --region us-west-2 --tag-key App --tag-value myapp