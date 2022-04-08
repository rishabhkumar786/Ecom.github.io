from django.urls import path
from .import views
urlpatterns = [
   path("", views.index, name="ShopHome"),
   path("about/", views.about, name="aboutus"),
   path("contact/", views.contact, name="contactus"),
   path("search/", views.search, name="search"),
   path("history/", views.history, name="search"),
   path("tracker/", views.tracker, name="search"),
   path("products/<int:myid>", views.productView, name="search"),
   path("checkout/", views.checkout, name="search"),
   path("handlerequest/", views.handlerequest, name="HandleRequest"),
]