from .SignUpResource import SignupEndpoint

def initialize_routes(api):
    api.add_resource(SignupEndpoint, '/api/signup')