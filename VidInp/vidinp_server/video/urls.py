from django.urls import path
# from .views import index, pro, actual
from .views import index, actual, pro, pro_with_id

urlpatterns = [
    path("", index, name="home"),
    path("actual/", actual, name="actual"),
    path(r"pro/<int:id>/", pro_with_id, name="pro"),
    path("pro", pro, name="all_pro")
]
