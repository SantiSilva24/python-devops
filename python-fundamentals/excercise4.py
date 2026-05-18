class Deployment:
    """
    Manages the state and version history of a software deployment.
    """

    def __init__(self, service_name: str, environment: str):

        if not (isinstance(service_name, str) and isinstance(environment, str)):
            raise TypeError("Invalid type, both service name and environment must be strings")
            
        if not (service_name.strip() and environment.strip()):
            raise ValueError("Both service name and environment must be non-empty strings")
        
        self.service_name = service_name
        self.environment = environment
        self.status = 'pending'
        self.version = None

        # Store version history
        self.previous_versions = []

    def deploy(self, new_version: str):

        if not isinstance(new_version, str):
            raise TypeError("New version arguement must be string")
            
        if not new_version.strip():
            raise ValueError("New version must be a non-empty string")

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