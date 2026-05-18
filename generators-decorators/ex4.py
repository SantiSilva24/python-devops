# Decorator factory that performs an action validating a required permission

from functools import wraps

class AuthorizationError(Exception):
    def __init__(self, user_name, required_role):
        self.user_name = user_name
        self.required_role = required_role
        message = f"User '{user_name}' lacks the required role: '{required_role}'"
        super().__init__(message)

def require_role(required_role):
    """
    A decorator factory that creates a decorator to check for a specific user role.

    Args:
        required_role (str): The role string that the user must have.

    Returns:
        A decorator function.
    """
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('user')

            if not user:
                raise ValueError("A 'user' keyword argument is required")
            
            roles = user.get('roles')
            if not (len(roles) > 0 and isinstance(roles, list)):
                raise ValueError("The roles list must not be empty")

            if not required_role in roles:
                raise AuthorizationError(user.get('name'), required_role)
            value = func(*args, **kwargs)
            return value
        return wrapper
    return decorator
            
    
 
@require_role('admin')
def restart_server(*, user, server_id):
    """Restarts a server after a permission check."""
    message = f"Server {server_id} restart initiated by {user['name']}."
    print(message)
    return message
 
admin_user = {'name': 'alice', 'roles': ['admin', 'viewer']}
viewer_user = {'name': 'bob', 'roles': ['viewer']}
 
# This call will succeed
restart_server(user=admin_user, server_id='web-01')
 
# This call will raise a PermissionError
#restart_server(user=viewer_user, server_id='db-01')
   