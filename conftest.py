import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from auth.token_service import TokenService
from endpoint import PrefixRoute, Endpoint
from main import app
from database import Base, get_db
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from settings_config import get_settings

settings = get_settings()


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session')
def get_token_service():
    return TokenService()


url = get_settings().test_database_url
test_engine = create_async_engine(url, future=True)


@pytest.fixture(scope='module')
async def db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='module')
@pytest.mark.asyncio
async def client_without_jwt(db_session) -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client


async def save_user(client, email, password):
    data = {'email': email, 'password': password}
    res = await client.post(PrefixRoute.auth + Endpoint.signup, json=data)
    return res.json()


@pytest.fixture(scope='module')
async def first_user(client_without_jwt):
    return await save_user(client_without_jwt, email='first_user@example.com', password='1234567890')


@pytest.fixture(scope='module')
async def second_user(client_without_jwt):
    return await save_user(client_without_jwt, email='second_user@example.com', password='1234567890')


async def retrieve_access_token(token_service: TokenService, email: str):
    kw = {'secret_key': settings.secret_key, 'exp_time': settings.access_token_expire_minutes, 'algorithm': settings.algorithm}
    access_token = await token_service.create_token_for_user(data={'sub': email}, **kw)
    return access_token


@pytest.fixture(scope='module')
@pytest.mark.asyncio
async def first_client_with_jwt_token(get_token_service: TokenService, first_user) -> AsyncClient:
    token = await retrieve_access_token(token_service=get_token_service, email=first_user['email'])
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        client.headers.update({'Authorization': f'Bearer {token}'})
        yield client


@pytest.fixture(scope='module')
@pytest.mark.asyncio
async def second_client_with_jwt_token(get_token_service: TokenService, second_user) -> AsyncClient:
    token = await retrieve_access_token(token_service=get_token_service, email=second_user['email'])
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        client.headers.update({'Authorization': f'Bearer {token}'})
        yield client


async def get_test_db():
    async_session = sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


app.dependency_overrides[get_db] = get_test_db
