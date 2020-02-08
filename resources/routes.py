from .SignUpResource import SignupEndpoint
from .LogInResource import LoginEndpoint
def initialize_routes(api):   
    api.add_resource(LoginEndpoint, '/api/login')
    api.add_resource(SignupEndpoint, '/api/signup')