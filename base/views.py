from django.shortcuts import render
from datetime import timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.shortcuts import render, get_object_or_404
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# from .tokens import account_activation_token  
from django.contrib.auth.models import User  


import os
from PIL import Image
from django.http import HttpResponse
import zipfile

# =====================Functions Used In Logic ===========================#

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        niche = request.POST.get('niche')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')

        username_exists = User.objects.filter(username=username).exists()
        email_exists = User.objects.filter(email=email).exists()
        selected_niche = get_object_or_404(Niche, niche_name=niche)
        
        if username_exists:
            niche = Niche.objects.all()
            return render(request, 'register.html', {'error':'Username Already Exists, select other username','niche': niche} )
        elif email_exists:
            niche = Niche.objects.all()
            return render(request, 'register.html', {'error':'Email Already Exists, Please Signin in using that email','niche': niche} )
        
        elif User.objects.filter(Q(username=username) & Q(email=email)).exists():
            profile = get_object_or_404(Profile, email=email)
            return render(request, 'signin.html', {'profile':profile})
        else:
            if password==c_password:
                user = User.objects.create_user(username, email, password)
                # user.is_active = False
                user.save()
                profile = Profile.objects.create(name=name, username=username,email=email, joining_date=timezone.now(), fee_paid=False, user_subscription_record = False, niche=selected_niche, p1=True)
                profile.save()

                re_open_profile = get_object_or_404(Profile, email=email)
                id = re_open_profile.id
                return redirect( 'pay-now', id=id)
            else:
                niche = Niche.objects.all()
                return render(request, 'register.html', {'error':'Password does not matched','niche': niche} )
    niche = Niche.objects.all()
    return render(request, 'register.html', {'niche': niche})

def register_business(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        niche = request.POST.get('niche')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')

        username_exists = User.objects.filter(username=username).exists()
        email_exists = User.objects.filter(email=email).exists()
        selected_niche = get_object_or_404(Niche, niche_name=niche)
        if username_exists:
            niche = Niche.objects.all()
            return render(request, 'register_business.html', {'error':'Username Already Exists, select other username','niche': niche} )
        elif email_exists:
            niche = Niche.objects.all()
            return render(request, 'register_business.html', {'error':'Email Already Exists, Please Signin in using that email','niche': niche} )
        
        elif User.objects.filter(Q(username=username) & Q(email=email)).exists():
            profile = get_object_or_404(Profile, email=email)
            return render(request, 'signin.html', {'profile':profile})
        else:
            if password==c_password:
                user = User.objects.create_user(username, email, password)
                # user.is_active = False
                user.save()
                profile = Profile.objects.create(name=name, username=username,email=email, joining_date=timezone.now(), fee_paid=False, user_subscription_record = False, niche=selected_niche, p2=True)
                profile.save()

                re_open_profile = get_object_or_404(Profile, email=email)
                id = re_open_profile.id
                return redirect( 'pay-now-business', id=id)
            else:
                niche = Niche.objects.all()
                return render(request, 'register_business.html', {'error':'Password does not matched','niche': niche} )
    niche = Niche.objects.all()
    return render(request, 'register_business.html', {'niche': niche})

def pay_now(request,id):
    key = settings.STRIPE_PUBLIC_KEY
    profile = get_object_or_404(Profile, id=id)

    if request.method == 'POST':
        try:
            success_url = request.build_absolute_uri('/success/') + f'{id}'
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': 'price_1Pay9BL8ALOno4dNLzBHiZgR',  # Replace with your actual price ID
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=success_url,
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:

        return render(request, 'pay_now.html', {'key': key, 'profile':profile})   

def pay_now_business(request,id):
    key = settings.STRIPE_PUBLIC_KEY
    profile = get_object_or_404(Profile, id=id)

    if request.method == 'POST':
        try:
            success_url = request.build_absolute_uri('/success/') + f'{id}'
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': 'price_1OV7z0L8ALOno4dNe9ElVnA8',  # Replace with your actual price ID
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=success_url,
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:

        return render(request, 'pay_now.html', {'key': key, 'profile':profile})   

def success(request,id):
    profile = get_object_or_404(Profile, id=id)
    profile.fee_paid=True
    profile.user_subscription_record = True
    profile.save()
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            profile = get_object_or_404(Profile, username = username )
            # IF USER IS A REGITSTERED AND UnSUBSCRIBED MEMEBER THEN WE HAVE TO SIGN HIM IN
            # profile.fee_paid=True
            # profile.save()
            login(request, user)
            return redirect('dashboard')
            
        else:
            return redirect('home')
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')

def signin(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            profile = get_object_or_404(Profile, username = username )
            # IF USER IS A REGITSTERED AND UnSUBSCRIBED MEMEBER THEN WE HAVE TO SIGN HIM IN
            if profile.fee_paid:
                login(request, user)
                return redirect('dashboard')
            else:
                key = settings.STRIPE_PUBLIC_KEY
                id = profile.id
                return redirect('pay-now', id = id)
        else:
            return render(request, 'signin.html', {'message':'username or password is incorrect - make sure you are a registered user and paid membership fee also'})
    return render(request, 'signin.html')

def dashboard(request):
    user = request.user
    if user.is_authenticated:
        profile = get_object_or_404(Profile, email=user.email)
        # Get today's date
        today = timezone.now().date()
        
        # Calculate the most recent Monday
        last_monday = today - timedelta(days=today.weekday())
        
        # Filter products added from the last Monday onwards
        products = Products.objects.filter(date_added__date__gte=last_monday)
        shortlisted_products = []
        for p in products:
            if p.niche == profile.niche:
                shortlisted_products.append(p)
            
        return render(request, 'dashboard.html', {'products': shortlisted_products,'profile':profile})
    else:
        return redirect('home')

def signout(request):
    logout(request)
    return redirect('home')

def contactus(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        data = Contact.objects.create(name=name, email=email, message=message, date=timezone.now())
        data.save()
        return render(request,  'contactus.html', {'success':'Message Sent!'})
    return render(request, 'contactus.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def hireus(request):
    if request.method == "POST":
        email = request.POST.get('email')
        service = request.POST.get('service')
        message = request.POST.get('message')

        data = Service_Offer_Request.objects.create(email=email,service=service,message=message)
        data.save()
        success='Request Sent! We will contact you soon'
        return render(request, 'home.html', {'success':success})
    return render(request, 'hire_us.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')

def faqs(request):
    return render(request, 'faqs.html')

def no_link(request):
    user = request.user
    if user.is_authenticated:
        profile = get_object_or_404(Profile, email=user.email)
        return render(request, 'no_link.html', {'profile': profile})
    else:
        return redirect('home')


# ADMIN PANEL VIEWS STARTS FROM HERE

def add_products(request):
    niche = Niche.objects.all()
    if request.method == 'POST':
            title = request.POST['title']
            product_image = request.FILES['product_image']
            description = request.POST['description']
            niche_name = request.POST['niche']
            purchase_cost = request.POST['purchase_cost']
            selling_cost = request.POST['selling_cost']
            profit = request.POST['profit']
            aliexpress_link = request.POST.get('aliexpress_link', '')
            alibab_link = request.POST.get('alibab_link', '')
            country = request.POST['country']
            gender = request.POST['gender']
            age_range = request.POST['age_range']
            audience = request.POST['audience']
            interests = request.POST['interests']
            approximate_CPA = request.POST['approximate_CPA']
            saturation = request.POST['saturation']
            fb_ads = request.POST.get('fb_ads', '')
            videos = request.POST.get('videos', '')
            stores_selling_it = request.POST.get('stores_selling_it', '')

            niche = get_object_or_404(Niche, niche_name=niche_name)
        
            # Create and save the new product
            product = Products.objects.create(
                title=title,
                product_image=product_image,
                description = description,
                niche = niche,
                purchase_cost=purchase_cost,
                selling_cost=selling_cost,
                profit=profit,
                aliexpress_link=aliexpress_link,
                alibab_link=alibab_link,
                country=country,
                gender=gender,
                age_range=age_range,
                audiance=audience,
                intrests=interests,
                approximate_CPA=approximate_CPA,
                saturation=saturation,
                fb_ads=fb_ads,
                videos=videos,
                stores_selling_it=stores_selling_it,
                date_added = timezone.now()
            )
            product.save()
            return redirect('dashboard')  # Redirect to a success page
    return render(request, 'add_products.html', {'niche':niche})

def all_products(request):
    products = Products.objects.all().order_by('-date_added')
    niche = Niche.objects.all()
    if request.method == "POST":
        niche = Niche.objects.all()
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        niche1 = request.POST['niche']
        my_niche = get_object_or_404(Niche, niche_name = niche1 )
        products_in_date_range = Products.objects.filter(
            Q(date_added__gte=start_date) & Q(date_added__lte=end_date),
            niche=my_niche
        )
        
        products = products_in_date_range
        return render(request, 'all_products.html', {'products':products, 'niche':niche})

    return render(request, 'all_products.html', {'products':products, 'niche':niche})

def confirm_delete(request,id):
    product = get_object_or_404(Products, id=id)
    if product:
        product.delete()
        return redirect('all_products')
    else:
        return render(request, 'all_products.html',{'message':'NO PRODUCTS FOUND'})
    
def edit_products(request,id):
    product = get_object_or_404(Products, id=id)
    niche = Niche.objects.all()
    if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            niche_name = request.POST['niche']
            purchase_cost = int(request.POST['purchase_cost'])
            selling_cost = int(request.POST['selling_cost'])
            profit = int(request.POST['profit'])
            aliexpress_link = request.POST.get('aliexpress_link', '')
            alibab_link = request.POST.get('alibab_link', '')
            country = request.POST['country']
            gender = request.POST['gender']
            age_range = request.POST['age_range']
            audience = request.POST['audience']
            interests = request.POST['interests']
            approximate_CPA = request.POST['approximate_CPA']
            saturation = request.POST['saturation']
            fb_ads = request.POST.get('fb_ads', '')
            videos = request.POST.get('videos', '')
            stores_selling_it = request.POST.get('stores_selling_it', '')

            niche = get_object_or_404(Niche, niche_name=niche_name)

            try:
                product_image = request.FILES['product_image']
                product.description=description
                product.title=title
                product.product_image=product_image
                niche = niche
                product.purchase_cost=purchase_cost
                product.selling_cost=selling_cost
                product.profit=profit
                product.aliexpress_link=aliexpress_link
                product.alibab_link=alibab_link
                product.country=country
                product.gender=gender
                product.age_range=age_range
                product.audiance=audience
                product.intrests=interests
                product.approximate_CPA=approximate_CPA
                product.saturation=saturation
                product.fb_ads=fb_ads
                product.videos=videos
                stores_selling_it=stores_selling_it
                product.date_added = timezone.now()
                
                product.save()
                return redirect('all_products')  # Redirect to a success page
            except:
                # Create and save the new product
            
                product.product_image = product.product_image
                product.title=title
                product.description=description
                niche = niche
                product.purchase_cost=purchase_cost
                product.selling_cost=selling_cost
                product.profit=profit
                product.aliexpress_link=aliexpress_link
                product.alibab_link=alibab_link
                product.country=country
                product.gender=gender
                product.age_range=age_range
                product.audiance=audience
                product.intrests=interests
                product.approximate_CPA=approximate_CPA
                product.saturation=saturation
                product.fb_ads=fb_ads
                product.videos=videos
                stores_selling_it=stores_selling_it
                product.date_added = timezone.now()
                
                product.save()
                return redirect('all_products')  # Redirect to a success page
    return render(request, 'edit_products.html',{'product':product,'niche':niche})

def redistered_users(request):
    non_staff_users = User.objects.filter(is_staff=False)
    registered_profiles = []
    for users in non_staff_users:
        profile = Profile.objects.filter(username = users.username)
        for p in profile:
            if not p.fee_paid:
                registered_profiles.append(p)
    return render(request, 'view_registered_users.html', {'registered_profiles':registered_profiles})

def subscribers(request):
    niche = Niche.objects.all()
    non_staff_users = User.objects.filter(is_staff=False).order_by('-date_joined')
    subscribed_profiles = []
    for users in non_staff_users:
        profile = Profile.objects.filter(username = users.username)
        for p in profile:
            if p.fee_paid:
                subscribed_profiles.append(p)

    if request.method == "POST":
        niche = Niche.objects.all()
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        niche1 = request.POST['niche']
        print("------NICHE IS-----",niche1)
        if niche1 == 'Nil':
            profiles_in_date_range = Profile.objects.filter(
                Q(joining_date__gte=start_date) & Q(joining_date__lte=end_date)
            )
            
            subscribed_profiles = profiles_in_date_range
            return render(request, 'view_subscribers.html', {'subscribed_profiles':subscribed_profiles, 'niche':niche})
    
        my_niche = get_object_or_404(Niche, niche_name = niche1 )
        profiles_in_date_range = Profile.objects.filter(
            Q(joining_date__gte=start_date) & Q(joining_date__lte=end_date),
            niche=my_niche
        )
        
        subscribed_profiles = profiles_in_date_range
        return render(request, 'view_subscribers.html', {'subscribed_profiles':subscribed_profiles, 'niche':niche})
    
    return render(request, 'view_subscribers.html', {'subscribed_profiles':subscribed_profiles, 'niche':niche})

def old_subscribers(request):
    non_staff_users = User.objects.filter(is_staff=False)
    past_subscribed_profiles = []
    for users in non_staff_users:
        profile = Profile.objects.filter(username = users.username)
        for p in profile:
            if p.user_subscription_record and not p.fee_paid:
                past_subscribed_profiles.append(p)
    return render(request, 'view_old_subscribers.html', {'past_subscribed_profiles':past_subscribed_profiles})


# USERS VIEWS STARTS

def prodcut_details(request,id):
    user = request.user
    if user.is_authenticated:
        profile = get_object_or_404(Profile, email=user.email)
        product = get_object_or_404(Products, id=id)

        return render(request, 'product_details.html', {'profile': profile, 'p':product})
    else:
        return redirect('home')

def past_two_weeks_products(request):
    user = request.user
    if user.is_authenticated:
        profile = get_object_or_404(Profile, email=user.email)
        
        # Get today's date
        today = timezone.now().date()
        
        # Calculate the start of the previous week (Monday)
        start_of_previous_week = today - timedelta(days=today.weekday() + 7)
        
        # Filter products added during the past two weeks
        products = Products.objects.filter(date_added__date__range=[start_of_previous_week, today])
        shortlisted_products = []
        for p in products:
            if p.niche.niche_name == profile.niche.niche_name:
                shortlisted_products.append(p)
        return render(request, 'past_week.html', {'products': shortlisted_products, 'profile': profile})
    else:
        return redirect('home')

def past_three_weeks_products(request):
    user = request.user
    if user.is_authenticated:
        profile = get_object_or_404(Profile, email=user.email)
        
        # Get today's date
        today = timezone.now().date()
        
        # Calculate the start of three weeks ago (Monday)
        start_of_three_weeks_ago = today - timedelta(days=today.weekday() + 14)
        
        # Filter products added during the past three weeks
        products = Products.objects.filter(date_added__date__range=[start_of_three_weeks_ago, today])
        shortlisted_products = []
        for p in products:
            if p.niche.niche_name == profile.niche.niche_name:
                shortlisted_products.append(p)
        return render(request, 'past3_weeks.html', {'products': shortlisted_products, 'profile': profile})
    else:
        return redirect('home')
    
def past_four_weeks_products(request):
    user = request.user
    if user.is_authenticated:
        profile = get_object_or_404(Profile, email=user.email)
        
        # Get today's date
        today = timezone.now().date()
        
        # Calculate the start of three weeks ago (Monday)
        start_of_three_weeks_ago = today - timedelta(days=today.weekday() + 21)
        
        # Filter products added during the past three weeks
        products = Products.objects.filter(date_added__date__range=[start_of_three_weeks_ago, today])
        shortlisted_products = []
        for p in products:
            if p.niche.niche_name == profile.niche.niche_name:
                shortlisted_products.append(p)
        return render(request, 'past4_weeks.html', {'products': shortlisted_products, 'profile': profile})
    else:
        return redirect('home')



# FREE TOOLS IN OUR WEBSITE


def convert_to_webp_and_download(input_files):
    try:
        # Create a temporary directory to store the converted WebP images
        temp_dir = 'temp_webp_images'
        os.makedirs(temp_dir, exist_ok=True)

        # Convert each input image to WebP format and save it in the temporary directory
        for input_file in input_files:
            with Image.open(input_file) as img:
                webp_image = img.convert("RGB")
                temp_filename = os.path.join(temp_dir, os.path.splitext(input_file.name)[0] + ".webp")
                webp_image.save(temp_filename, "WEBP")

        # Create a zip folder and add the WebP images to it
        zip_filename = 'webp_images.zip'
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for temp_file in os.listdir(temp_dir):
                temp_file_path = os.path.join(temp_dir, temp_file)
                zipf.write(temp_file_path, os.path.basename(temp_file_path))

        # Prepare the response to download the zip folder
        with open(zip_filename, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

        # Delete the temporary directory and zip folder after sending it for download
        for temp_file in os.listdir(temp_dir):
            temp_file_path = os.path.join(temp_dir, temp_file)
            os.remove(temp_file_path)
        os.rmdir(temp_dir)
        os.remove(zip_filename)
        print("--------I FIRED 2")

        return response

    except Exception as e:
        print(f"An error occurred while converting the images: {e}")
        return HttpResponse(status=500)

def image_conversion(request):
    user = request.user
    if user.is_authenticated:
        profile = get_object_or_404(Profile, email=user.email)
    if request.method == 'POST' and 'file' in request.FILES:
        print("--------I FIRED 1")
        input_images = request.FILES.getlist('file')  # Get the list of uploaded images using the correct key ('file')
        print("-----INPUT IMAGES - ----", input_images)
        return convert_to_webp_and_download(input_images)
    return render(request, 'image_conversion.html', {'profile':profile})

def guide(request):
    return render(request, 'guide.html')

def privacy_policy_generator(request):
    return render(request, 'privacy_policy_generator.html')

def refund_policy_generator(request):
    return render(request, 'refund_policy_generator.html')

def return_policy_generator(request):
    return render(request, 'return_policy_generator.html')

def shipping_policy_generator(request):
    return render(request, 'shipping_policy_generator.html')

def terms_and_conditions_generator(request):
    return render(request, 'terms_and_conditions_generator.html')

def profit_calculator(request):
    return render(request, 'profit_calculator.html')