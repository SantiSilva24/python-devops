# Decorator factory that performs an action validating a required permission

from functools import wraps

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
            roles = user.get('roles') if user else None
            if not roles:
                return None
            if not required_role in roles:
                print(f"The user {user['name']} does not have the required_role {required_role}")
                raise PermissionError
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
   