from .SignUpResource import SignupEndpoint
from .LogInResource import LoginEndpoint
from .ConceptMapResource import CreateConceptMapEndpoint, AlterConceptMapEndpoint
def initialize_routes(api):   
    api.add_resource(LoginEndpoint, '/api/login')
    api.add_resource(SignupEndpoint, '/api/signup')
    api.add_resource(CreateConceptMapEndpoint, '/api/cpt-map')
    api.add_resource(AlterConceptMapEndpoint, '/api/cpt-map/<id>')