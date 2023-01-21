from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

# TODO название файла капсом, не надо

# TODO вынести переменные, какие бы они ни были, в общий файл

# TODO это не модель, зачем она в users/models
SECRET = "SECRET"

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
