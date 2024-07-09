from fastapi import FastAPI, Depends
from .routers import admin, customers, delivery, auth
from . import models, database
from .routers.auth import get_current_admin_user, get_current_user, get_current_delivery_partner

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(admin.router, prefix="/admin", tags=["admin"], dependencies=[Depends(get_current_admin_user)])
app.include_router(customers.router, prefix="/customer", tags=["customer"], dependencies=[Depends(get_current_user)])
app.include_router(delivery.router, prefix="/delivery", tags=["delivery"], dependencies=[Depends(get_current_delivery_partner)])
