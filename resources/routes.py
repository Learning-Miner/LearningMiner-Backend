
from .LogInResource import LoginEndpoint
def initialize_routes(api):
    
    api.add_resource(LoginEndpoint, '/api/login')