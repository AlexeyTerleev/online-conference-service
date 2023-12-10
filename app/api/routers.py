from api.auth import router as auth_router
from api.users import router as users_router
from api.courses import router as courses_router

all_routers = [
    auth_router,
    users_router,
    courses_router,
]
