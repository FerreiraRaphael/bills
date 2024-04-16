from api_py.run import create_api
from mangum import Mangum

print('No index.py')
app = create_api()
handler = Mangum(app, lifespan="on")

