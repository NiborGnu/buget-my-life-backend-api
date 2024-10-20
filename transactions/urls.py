from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, TransactionCommentViewSet

router = DefaultRouter()
router.register(
    '', 
    TransactionViewSet, 
    basename='transactions'
)
router.register(
    'comments',
    TransactionCommentViewSet,
    basename='comments'
)

urlpatterns = router.urls
