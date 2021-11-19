# simple-fastapi-blog
API for Blog site using FastAPI

1. git clone
2. pip install -r requirements.txt
3. docker-compose up -d --build
4. alembic revision --autogenerate -m "Added tables"
5. alembic upgrade head
6. create test database in pgadmin = ex ~ db_test
7. add image on article/tests/ with name win11.jpeg or your pic and change in .env file = TEST_IMAGE_PATH
