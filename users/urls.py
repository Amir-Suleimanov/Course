from users.views import UserView, UsersViewSet

from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedDefaultRouter

app_name = 'users'


router = SimpleRouter()
router.register(r"", UsersViewSet, basename="users")
router.register(r'', UserView, basename='user')

balance_router = NestedDefaultRouter(parent_router=router, parent_prefix='',lookup='user')
# balance_router.register(r'balance', UserBalanceViewSet, basename='balance')

urlpatterns = router.urls + balance_router.urls
