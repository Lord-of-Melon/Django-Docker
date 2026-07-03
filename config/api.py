from ninja import NinjaAPI
from apps.api.router import router

api = NinjaAPI(
    title="E-Learning API",
    version="1.0.0",
    description="REST API untuk sistem E-Learning"
)

api.add_router("", router)