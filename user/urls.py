from .views import *
from django.urls import path 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('', HomePage.as_view(),name="home_page"),
    path('home', HomePage.as_view(),name="home_page"),
    path('index', indexPage.as_view(),name="index_page"),
    path('register', Register.as_view(),name="register_page"),
    path('login', Login.as_view(),name="login_page"),
    path('dashboard', dashboad.as_view(),name="dashboard_page"),
    path('verify', Verify.as_view(),name="verify_page"),
    path('logout', logout.as_view(),name="logout_page"),
    path('add_cat', Addcatagory.as_view(),name="addcatagory"),
    path('getcategory', Getcategory.as_view(),name="getcategory"),
    path('<int:id>', Getsubcategory.as_view(),name="getsubcategory"),
    path('add_subcat', Addsubcatagory.as_view(),name="addsubcatagory"),
    path('upoaded_data/<int:id>',UploadedProducts.as_view(),name="UploadedProducts"),
    path('uploadproducts',uploadproducts.as_view(),name='uploadproducts'),
    path('getsubcat/<int:id>', GetsubcategoryAJX.as_view(),name="GetsubcategoryAJX"),
    path('inner/<my_id>',inner.as_view(),name='inner'),
    path('upoaded_data/inner/<my_id>',inner.as_view(),name='inner'),
    

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)