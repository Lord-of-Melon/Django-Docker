from ninja import Router

from .courses import router as course_router
from .auth import router as auth_router

router = Router()

router.add_router("/courses", course_router)
router.add_router("/auth", auth_router)