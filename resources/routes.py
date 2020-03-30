from .SignUpResource import SignupEndpoint
from .LogInResource import LoginEndpoint
from .ConceptMapResource import CreateConceptMapEndpoint, AlterConceptMapEndpoint, FilterUserConceptMapsEndpoint
from .ReportsResource import CreateReportsEndpoint, RetrieveReportsEndpoint
from .ActivityResource import CreateActivityResource
def initialize_routes(api):   
    api.add_resource(LoginEndpoint, '/api/login')
    api.add_resource(SignupEndpoint, '/api/signup')
    api.add_resource(CreateConceptMapEndpoint, '/api/cpt-map')
    api.add_resource(FilterUserConceptMapsEndpoint, '/api/cpt-map/filter')
    api.add_resource(AlterConceptMapEndpoint, '/api/cpt-map/<id>')
    api.add_resource(CreateReportsEndpoint, '/api/reports/create/<baseId>')
    api.add_resource(RetrieveReportsEndpoint, '/api/reports/retrieve/<baseId>')
    api.add_resource(CreateActivityResource, '/api/activity/create')