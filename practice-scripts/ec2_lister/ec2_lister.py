import boto3
import argparse
from botocore.exceptions import ClientError, NoCredentialsError
from rich.table import Table
from rich.console import Console

console = Console()

def list_instances(region: str, tag_key: str, tag_value: str, state_filter: str):
    """
    Query EC2 in a given region, filter by tag and state.
    Returns a list of dicts with instance info.
    """
    ec2 = boto3.client("ec2", region_name=region)

    # Build filters — only add tag filter if both key and value provided
    filters = []
    if tag_key and tag_value:
        filters.append({
            "Name": f"tag:{tag_key}",  # e.g. "tag:Environment"
            "Values": [tag_value]
        })
    if state_filter != "all":
        filters.append({
            "Name": "instance-state-name",
            "Values": [state_filter]
        })

    # describe_instances returns pages — use paginator to get ALL results
    # (a naive call only returns the first page, max 1000 instances)
    paginator = ec2.get_paginator("describe_instances")
    instances = []

    for page in paginator.paginate(Filters=filters):
        for reservation in page["Reservations"]:
            for inst in reservation["Instances"]:
                # Extract the "Name" tag value, default to "(no name)"
                name = next(
                    (t["Value"] for t in inst.get("Tags", []) if t["Key"] == "Name"),
                    "(no name)"
                )
                instances.append({
                    "id":         inst["InstanceId"],
                    "name":       name,
                    "type":       inst["InstanceType"],
                    "state":      inst["State"]["Name"],
                    "az":         inst["Placement"]["AvailabilityZone"],
                    "private_ip": inst.get("PrivateIpAddress", "—"),
                    "public_ip":  inst.get("PublicIpAddress", "—"),
                })

    return instances


def print_table(instances: list, region: str):
    """Render a rich table to the terminal."""
    table = Table(title=f"EC2 instances — {region}", show_lines=False)
    table.add_column("ID",         style="cyan",  no_wrap=True)
    table.add_column("Name",       style="white")
    table.add_column("Type",       style="dim")
    table.add_column("State",      style="white")
    table.add_column("AZ",         style="dim")
    table.add_column("Private IP", style="dim")
    table.add_column("Public IP",  style="dim")

    state_colors = {
        "running":    "green",
        "stopped":    "yellow",
        "terminated": "red",
    }

    for inst in instances:
        color = state_colors.get(inst["state"], "white")
        table.add_row(
            inst["id"],
            inst["name"],
            inst["type"],
            f"[{color}]{inst['state']}[/{color}]",
            inst["az"],
            inst["private_ip"],
            inst["public_ip"],
        )

    console.print(table)
    console.print(f"[dim]Total: {len(instances)} instance(s)[/dim]")


def main():
    parser = argparse.ArgumentParser(description="List EC2 instances with tag filtering")
    parser.add_argument("--region",    default="us-east-1", help="AWS region")
    parser.add_argument("--tag-key",   default="Environment", help="Tag key to filter by")
    parser.add_argument("--tag-value", default="dev",         help="Tag value to filter by")
    parser.add_argument("--state",     default="all",
                        choices=["all", "running", "stopped", "terminated"],
                        help="Filter by instance state")
    args = parser.parse_args()

    try:
        instances = list_instances(
            region=args.region,
            tag_key=args.tag_key,
            tag_value=args.tag_value,
            state_filter=args.state,
        )

        if not instances:
            console.print(f"[yellow]No instances found with tag {args.tag_key}={args.tag_value}[/yellow]")
            return

        print_table(instances, args.region)

    except NoCredentialsError:
        console.print("[red]Error: AWS credentials not configured. Run 'aws configure'.[/red]")
    except ClientError as e:
        console.print(f"[red]AWS error: {e.response['Error']['Message']}[/red]")


if __name__ == "__main__":
    main()