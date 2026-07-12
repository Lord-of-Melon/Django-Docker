from ninja import Router

from .courses import router as course_router
from .auth import router as auth_router
from .enrollments import router as enrollment_router

from .reviews import router as review_router
from .wishlist import router as wishlist_router
from .dashboard import router as dashboard_router

router = Router()

router.add_router("/enrollments", enrollment_router)
router.add_router("/courses", course_router)
router.add_router("/reviews", review_router)
router.add_router("/auth", auth_router)
router.add_router("/wishlist",wishlist_router)
router.add_router("/dashboard",dashboard_router)