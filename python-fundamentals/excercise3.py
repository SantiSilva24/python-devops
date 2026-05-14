REQUIRED_KEYS = {'name', 'region', 'status'}
ALLOWED_STATUS = {'active', 'inactive'}


def validate_server(server: dict) -> bool:

    if not isinstance(server, dict):
        return False

    missing_keys = REQUIRED_KEYS - server.keys()

    if missing_keys:
        return False

    name = server['name']
    region = server['region']
    status = server['status']

    if not (
        isinstance(name, str)
        and isinstance(region, str)
        and isinstance(status, str)
    ):
        return False

    if not (name.strip() and region.strip()):
        return False

    if status not in ALLOWED_STATUS:
        return False

    return True


def generate_inventory_report(servers: list[dict]) -> dict:

    if not isinstance(servers, list):
        return {"error": "A list of servers is required"}

    report = {}

    for server in servers:

        if not validate_server(server):
            continue

        name = server['name']
        region = server['region']
        status = server['status']

        # Create region if missing
        if region not in report:
            report[region] = {
                'active': [],
                'inactive': []
            }

        # Add server name to correct status list
        report[region][status].append(name)

    return report


servers = [
    {'name': 'web-01', 'region': 'us-east-1', 'status': 'active'},
    {'name': 'db-01', 'region': 'eu-west-1', 'status': 'active'},
    {'name': 'app-01', 'region': 'us-east-1', 'status': 'inactive'},
    {'name': 'web-02', 'region': 'us-east-1', 'status': 'active'},
    {'name': 'monitor-01', 'region': 'eu-west-1', 'status': 'down'}
]

print(generate_inventory_report(servers))