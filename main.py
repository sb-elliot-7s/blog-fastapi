from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from articles.controllers import articles_router
from auth.auth_controllers import auth_router
from comments.controllers import comments_router
from auth.user_contollers import user_router

from middlewares import cors_middleware

app = FastAPI(default_response_class=ORJSONResponse)
app.include_router(articles_router)
app.include_router(auth_router)
app.include_router(comments_router)
app.include_router(user_router)

app.add_middleware(**cors_middleware)
