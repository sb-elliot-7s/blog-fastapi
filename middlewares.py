from fastapi.middleware.cors import CORSMiddleware

origins = ["http://127.0.0.1:8000"]

cors_middleware = {'middleware_class': CORSMiddleware,
                   'allow_origins': origins,
                   'allow_credentials': True,
                   'allow_methods': ["*"],
                   'allow_headers': ["*"]}
