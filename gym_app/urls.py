from django.contrib import admin
from django.urls import path
from gym_app.views import add_product_by_Vendor, add_product_by_admin, add_to_carts, added_products, admin_dashboard, admin_login, admin_logout, admin_product_update, admin_signup, buy_now, buyer_home, buyers_about, buyers_allproducts, buyers_contact, buyers_gymweights, buyers_personalgears, buyers_threadwalk, contact_submit, current_staff, delete_admin_product, delete_from_cart, delete_staff, delete_vendor, delete_vendor_product, existing_vendors, find_product, getupdate,  home, logins, new_vendor, select_user_type, signup, staff_admin_products, staff_dashboard, staff_home, staff_login, staff_signup, update_admin_product, update_vendor_products, upload_product_Admin, user_logout, users_products, vendor_dashboard, vendor_login, vendor_logout, vendor_signup, vendors_home, view_cart, view_vendors 
urlpatterns = [
    path('home',home),
    
    path('adminsign',admin_signup), 
    path('adminlog',admin_login),
    path('admindashboard',admin_dashboard),
    path('adminlogout',admin_logout),
    
    path('upload',upload_product_Admin),
    path('add_product',add_product_by_admin),
    path('all_product',added_products),
######################################################################################################################
    path('', buyer_home),
    path('home/<str:username>/', buyer_home),
    path('select_user/', select_user_type),
    path('signup/', signup),
    path('login/', logins),
    path('logout/',user_logout),
    
    path('add_to_cart/<str:uname>/<int:pid>/', add_to_carts),
    path('view_cart/<str:uname>/', view_cart),
    path('delete_from_cart/<str:uname>/<int:product_id>/', delete_from_cart),
###################################################################################################################################
    path('about',buyers_about),
    path('contact',buyers_contact),
    path('buyerproduct',buyers_allproducts),
    path('threadwalk',buyers_threadwalk),
    path('gymweight',buyers_gymweights),
    path('personalgears',buyers_personalgears),
    path('buy_now/<str:username>/<int:product_id>/',buy_now),
    path('search/', find_product),
    path('contact/submit/', contact_submit),
    
####################################################################################################################################
    path('vendors/',vendors_home),
    path('vendors/existing',existing_vendors),
    path('vendors/new',new_vendor),
    # Vendor Auth
    path('vendor_signup', vendor_signup),
    path('vendor_login',vendor_login),
    path('vendor_logout',vendor_logout),
    # Vendor Dashboard + Product Management
    path('vendor_dashboard/',vendor_dashboard),
    path('add_product_by_Vendor/',add_product_by_Vendor),
    path("view_vendors/",view_vendors),
    path('vendors/delete/<str:vendor_id>/',delete_vendor),
    
   path('vendor/product/<int:product_id>/edit/', getupdate),
   path('vendor/product/<int:product_id>/update/', update_vendor_products),
   path('vendor/product/<int:product_id>/delete/', delete_vendor_product),
#########################################################################################################################
    path('staff/',staff_home),  # Staff menu page
    path('staff/signup/', staff_signup),
    path('staff/login/', staff_login),
    path('staff/dashboard/', staff_dashboard),
    path('staff/list/', current_staff),
    path('staff/delete/<str:staff_id>/', delete_staff),
    path('staff/admin-products/',staff_admin_products),
    path('staff/admin-products/update/<int:product_id>/', admin_product_update),   # Show form
    path('staff/admin-products/update/save/<int:product_id>/', update_admin_product),
    path('staff/admin-products/delete/<int:product_id>/', delete_admin_product),
     path('users/',users_products),
    
    
]