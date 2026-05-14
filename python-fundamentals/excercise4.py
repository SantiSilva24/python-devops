class Deployment:
    """
    Manages the state and version history of a software deployment.
    """

    def __init__(self, service_name: str, environment: str):
        self.service_name = service_name
        self.environment = environment
        self.status = 'pending'
        self.version = None

        # Store version history
        self.previous_versions = []

    def deploy(self, new_version: str):

        # Save current version before replacing it
        if self.version is not None:
            self.previous_versions.append(self.version)

        self.version = new_version
        self.status = 'deployed'

    def rollback(self) -> bool:

        # No history available
        if not self.previous_versions:
            return False

        # Restore last version
        self.version = self.previous_versions.pop()
        self.status = 'rolled_back'

        return True

    def check_status(self) -> dict:
        return {
            'service_name': self.service_name,
            'environment': self.environment,
            'status': self.status,
            'version': self.version
        }