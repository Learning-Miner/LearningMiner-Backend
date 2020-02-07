from .SignUpResource import SignupEndpoint
from .LogInResource import LoginEndpoint
from .ConceptMapResource import ConceptMapEndpoint
def initialize_routes(api):   
    api.add_resource(LoginEndpoint, '/api/login')
    api.add_resource(SignupEndpoint, '/api/signup')
    api.add_resource(ConceptMapEndpoint, '/api/cpt-map')