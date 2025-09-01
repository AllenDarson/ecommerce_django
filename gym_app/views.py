from typing import DefaultDict
from django.db.models import Q
from django.shortcuts import redirect, render

from gym_app.models import AdminUsers, Buyer, Cart, Carts, Product_add
from .models import Order, Product_add, Product_vendor, Staff, Vendor

from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

from django.contrib.auth import authenticate, login  ,logout 
from django.contrib.auth.models import User

from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'home.html')

def upload_product_Admin(request):
    return render(request,"upload_product_A.html")

def admin(request):
    return render(request, 'admin_login.html')

def signup(request):
    return render(request, 'admin_signup.html')

def admin_signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # Check if email already exists
        if AdminUsers.objects.filter(email=email).exists():
            return render(request, 'admin_signup.html', {'error': 'Email already exists'})

        # Save admin user
        AdminUsers.objects.create(name=name, email=email, password=password)
        return redirect('adminlogin')
    
    return render(request, 'admin_signup.html')

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = AdminUsers.objects.filter(email=email, password=password).first()

        if user:
            request.session['admin_user'] = email  # Save session
            return redirect(admin_dashboard)
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials'})

    return render(request, 'admin_login.html')


def admin_dashboard(request):
    return render(request, 'admin_dashboard.html',{'username': request.session['admin_user']})


def admin_logout(request):
    return redirect(admin_login)

def add_product_by_admin(request):
    if request.method == 'POST':
        
        product_brand = request.POST.get('product_brand')
        name = request.POST.get('product_name')
        desc = request.POST.get('description')
        cat = request.POST.get('category')
        price = request.POST.get('price')
        mfg_date = request.POST.get('manufacturing_date')
        to_date = request.POST.get('expiry_date')
        image_file = request.FILES.get('image')
        print(product_brand)
        Product_vendor.objects.create(
            product_brand=product_brand,
            product_name=name,
            description=desc,
            category=cat,
            price=price,
            Manufacturing_date=mfg_date,   # ✅ match model field name
            expiry_date=to_date,
            image=image_file
        )
        return redirect(added_products)

    return render(request, 'a_upload_product.html')

def added_products(request):
    all_products = Product_vendor.objects.all()
    return render(request, "added_products.html", {'products': all_products})
###################################################################################################################################################
def buyer_home(request, username=None):
    best_selling_products = Product_vendor.objects.filter(category="Best Selling")
    return render(request, 'buyers_home.html', {
        'products': best_selling_products,
        'username': request.user.username if request.user.is_authenticated else None
    })

def select_user_type(request):
    return render(request, 'buyers_signup.html')

def signup(request):
    if request.method == 'POST':
        uname = request.POST['username']
        email = request.POST['email']
        pwd = request.POST['password']

        if User.objects.filter(username=uname).exists():
            return render(request, 'buyers_signin.html', {'error': 'Username already taken'})
        
        # create user with hashed password
        user = User.objects.create_user(username=uname, email=email, password=pwd)
        user.save()
        Buyer.objects.create(username=uname, email=email, password=pwd)

        # auto login after signup
        login(request, user)
        return redirect('home', username=uname)

    return render(request, 'buyers_signin.html')

def logins(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')

        user = authenticate(username=uname, password=pwd)

        if user is not None:
            login(request, user)
            return redirect('home', username=uname)
        else:
            # This handles invalid login
            return render(request, 'buyers_login.html', {'error': 'Invalid username or password'})

    # This handles GET requests
    return render(request, 'buyers_login.html')

def user_logout(request):
    logout(request)  # clears the session
    return redirect('login')  # redirect to homepage (or login page)
####################################################################################################################################################
def add_to_carts(request, uname, pid):
    buyer = Buyer.objects.get(username=uname)
    product = Product_vendor.objects.get(product_id=pid)
    Carts.objects.create(buyer_name=uname, buyer_id=buyer.id, product_name=product.product_name, product_id=pid)
    return render(request, 'buyers_success.html', {'username': uname})

def view_cart(request, uname):
    cart_items = Carts.objects.filter(buyer_name=uname)
    product_ids = cart_items.values_list('product_id', flat=True)
    products = Product_vendor.objects.filter(product_id__in=product_ids)
    return render(request, 'buyers_view.html', {'products': products, 'username': uname})

def delete_from_cart(request, uname, product_id):
    if request.method == 'POST':
        Carts.objects.filter(buyer_name=uname, product_id=product_id).delete()
    return redirect(f'/view_cart/{uname}/')
###################################################################################################################################################
def buy_now(request, username, product_id):
    # Get the product
    product = get_object_or_404(Product_add, product_id=product_id)

    # Get the actual user's email from the database
    user = get_object_or_404(User, username=username)  # or Buyer.objects.get(username=username)
    user_email = user.email  # this is the actual email

    # If order not confirmed, show confirmation page
    if "confirm" not in request.GET:
        return render(request, "buyers_conform.html", {"product": product, "username": username})

    # Send confirmation email to the actual email
    send_mail(
        "Order Confirmation",
        f"Hello {username}, your order for {product.product_name} is confirmed. "
        "Thank you for buying. You will get it in 7 days.",
        "allendarson27@gmail.com",  # sender email
        [user_email],  # actual user's email
        fail_silently=True
    )

    # Show order complete page
    return render(request, "buyers_complete.html", {"product": product, "username": username})

def contact_submit(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        service = request.POST.get('service')
        message_text = request.POST.get('message')

        # Email content
        subject = f"New Contact Request: {service}"
        message = f"Name: {name}\nEmail: {email}\nService: {service}\nMessage:\n{message_text}"
        from_email = 'allendarson27@gmail.com'   # Replace with your email
        recipient_list = [email]  # Replace with admin email(s)

        # Send email
        send_mail(subject, message, from_email, recipient_list)

        # Success message
        messages.success(request, "Your message has been successfully submitted. We’ll respond as soon as possible.")

        return redirect(buyers_contact)

###################################################################################################################################################
def buyers_about(request):
    return render(request,'buyers_about.html',{
        'username': request.user.username if request.user.is_authenticated else None
    })
def buyers_contact(request):
    return render(request,'buyers_contact.html',{
        'username': request.user.username if request.user.is_authenticated else None
    })
def buyers_allproducts(request):
    return render(request,'buyers_allproduct.html',{
        'username': request.user.username if request.user.is_authenticated else None
    })
def buyers_threadwalk(request):
    # Admin products
    admin_products = Product_vendor.objects.filter(category__in=["Threadmills", "Walkpads"])
    # Vendor products
    vendor_products = Product_vendor.objects.filter(category__in=["Threadmills", "Walkpads"])
    
    # Combine both
    # products = list(admin_products) + list(vendor_products)
    
    return render(request, 'buyers_threadmill.html', {
        'products': vendor_products,
        'username': request.user.username if request.user.is_authenticated else None
    })


def buyers_gymweights(request):
    admin_products = Product_vendor.objects.filter(category="Gym Weights")
    vendor_products = Product_vendor.objects.filter(category="Gym Weights")
    
    # products = list(admin_products) + list(vendor_products)
    
    return render(request, 'buyers_gymweights.html', {
        'products': vendor_products,
        'username': request.user.username if request.user.is_authenticated else None
    })


def buyers_personalgears(request):
    admin_products = Product_vendor.objects.filter(category="Personal Gears")
    vendor_products = Product_vendor.objects.filter(category="Personal Gears")
    
    # products = list(admin_products) + list(vendor_products)
    
    return render(request, 'buyers_personalgears.html', {
        'products': vendor_products,
        'username': request.user.username if request.user.is_authenticated else None
    })


def find_product(request):
    query = request.GET.get('query', '')  # get search input

    products = Product_vendor.objects.filter(
        Q(product_name__icontains=query) | 
        Q(product_brand__icontains=query)  # search by brand
    ) if query else Product_vendor.objects.none()  

    return render(request, 'buyers_search.html', {
        'products': products,
        'query': query,
        'username': request.user.username if request.user.is_authenticated else None
    })
###################################################################################################################################################
def vendors_home(request):
    return render(request, 'vendors.html')

def existing_vendors(request):
    all_vendors = Vendor.objects.all()
    return render(request, 'vendors_existing.html', {'vendors': all_vendors})

def vendor_signup(request):
    if request.method == 'POST':
        vname = request.POST['vendor_name']
        vid = request.POST['vendor_id']
        email = request.POST['email']
        product=request.POST['product']
        pwd = request.POST['vendor_password']

        # check if vendor_id exists
        if Vendor.objects.filter(vendor_id=vid).exists():
            return render(request, 'vendors_signup.html', {'error': 'Vendor ID already exists'})

        # create Vendor entry
        Vendor.objects.create(
            
            vendor_name=vname,
            vendor_id=vid,
            email=email,
            product_brought=product,
            vendor_password=pwd
        )

        # create linked Django User for authentication
        User.objects.create_user(username=vid, password=pwd, email=email,product_brought=product)

        return redirect(vendor_login)  # go to login after signup

    return render(request, 'vendors_signup.html')

def vendor_login(request):
    if request.method == 'POST':
        vid = request.POST['vendor_id']
        pwd = request.POST['vendor_password']

        # Authenticate using Django's built-in system
        user = authenticate(request, username=vid, password=pwd)
        if user:
            login(request, user)  # Django handles session automatically
            return redirect(vendor_dashboard)
        else:
            return render(request, 'vendor_login.html', {'error': 'Invalid ID or Password'})

    return render(request, 'vendors_login.html')

def vendor_dashboard(request):
    vendor = Vendor.objects.filter(vendor_id=request.user.username).first()
    products = Product_vendor.objects.filter(vendor_id=vendor.id)

    return render(request, 'vendor_dashboard.html', {
        'vendor_name': vendor.vendor_name,
        'products': products
    })


def vendor_logout(request):
    logout(request)
    return redirect(vendor_login)

def new_vendor(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        vendor_id = request.POST['vendor_id']
        product_category = request.POST['product_category']
        vendor_password = request.POST['vendor_password']
        Vendor.objects.create(vendor_name=name,email=email,vendor_id=vendor_id,product_brought=product_category,vendor_password=vendor_password)
        return redirect('/vendors/existing')
    return render(request, 'vendors_new.html')

def view_vendors(request):
    vendors = Vendor.objects.all()
    return render(request, "vendors_existing.html", {"vendors": vendors})

def delete_vendor(request, vendor_id):
    Vendor.objects.filter(vendor_id=vendor_id).delete()
    return redirect(view_vendors)

def add_product_by_Vendor(request):
    if request.method == 'POST':
        vendor = Vendor.objects.filter(vendor_id=request.user.username).first()
       
        vendor_id= vendor.id
        product_brand = request.POST.get('product_brand')
        name = request.POST.get('product_name')
        desc = request.POST.get('description')
        cat = request.POST.get('category')
        price = request.POST.get('price')
        mfg_date = request.POST.get('manufacturing_date')
        to_date = request.POST.get('expiry_date')
        image_file = request.FILES.get('image')
        print(product_brand)
        Product_vendor.objects.create(
            vendor_id=vendor_id,
            product_brand=product_brand,
            product_name=name,
            description=desc,
            category=cat,
            price=price,
            Manufacturing_date=mfg_date,   # ✅ match model field name
            expiry_date=to_date,
            image=image_file
        )
        return redirect(vendor_dashboard)  

    return render(request, 'vendors_add.html')


def getupdate(request, product_id):
    product = Product_vendor.objects.get(product_id=product_id)
    return render(request, 'vendors_update.html', {'product': product})

def update_vendor_products(request, product_id):
    if request.method == "POST":
        desc = request.POST.get('description')
        price = request.POST.get('price')
        mfg_date = request.POST.get('manufacturing_date')
        to_date = request.POST.get('expiry_date')

        Product_vendor.objects.filter(product_id=product_id).update(
            description=desc,
            price=price,
            Manufacturing_date=mfg_date,
            expiry_date=to_date,
        )
        return redirect(vendor_dashboard)
    
def delete_vendor_product(request, product_id):
    Product_vendor.objects.filter(product_id=product_id).delete()
    return redirect(vendor_dashboard)
####################################################################################################################################################
def staff_home(request):
    return render(request, 'staff_home.html')  # shows options

# Signup
def staff_signup(request):
    if request.method == 'POST':
        Staff.objects.create(
            staff_id=request.POST['staff_id'],
            name=request.POST['name'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        return redirect(staff_login)
    return render(request, 'staff_signup.html')

# Login
def staff_login(request):
    if request.method == 'POST':
        staff_id = request.POST['staff_id']
        password = request.POST['password']
        if Staff.objects.filter(staff_id=staff_id, password=password).exists():
            return redirect(staff_dashboard)
        return redirect(staff_login)  # reload login if invalid
    return render(request, 'staff_login.html')

# Dashboard
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

# List all staff
def current_staff(request):
    staff_list = Staff.objects.all()
    return render(request, 'staff_existing.html', {'staff_list': staff_list})

# Delete staff
def delete_staff(request, staff_id):
    Staff.objects.filter(staff_id=staff_id).delete()
    return redirect('/staff/list/')


def staff_admin_products(request):
    admin_products = Product_vendor.objects.filter(vendor_id="")  # use "" if empty string for admin products
    return render(request, 'staff_view.html', {
        'products': admin_products,
    })
    
def admin_product_update(request, product_id):
    product = Product_vendor.objects.get(product_id=product_id)  # simple get
    return render(request, 'staff_updateproduct.html', {'product': product})

def update_admin_product(request, product_id):
    if request.method == "POST":
        desc = request.POST.get('description')
        price = request.POST.get('price')
        mfg_date = request.POST.get('manufacturing_date')
        to_date = request.POST.get('expiry_date')

        Product_vendor.objects.filter(product_id=product_id).update(
            description=desc,
            price=price,
            Manufacturing_date=mfg_date,
            expiry_date=to_date,
        )
        return redirect(staff_admin_products)
    # return render(request, 'staff_updateproduct.html')

    
def delete_admin_product(request, product_id):
    product = Product_vendor.objects.get(product_id=product_id)
    product.delete()
    return redirect(staff_admin_products) 

def users_products(request):
    # Get all users and their purchased products
    user_orders = DefaultDict(list)
    for order in Order.objects.all():
        user_orders[order.username].append(order)
    return render(request, 'admin_userorders.html', {'user_orders_dict': user_orders})
###################################################################################################################################################
    
