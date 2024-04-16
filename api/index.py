from api_py.run import create_api
from mangum import Mangum

print('No index.py')
created_app = create_api()
app = Mangum(created_app, lifespan="on")

