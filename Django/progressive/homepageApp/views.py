from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import *
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
import requests
import random
from decimal import Decimal
from django.core.mail import EmailMultiAlternatives, get_connection
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from progressiveApp.models import *

def custom404(request, exception):
    return render(request, '404.html', {}, status=404)

def custom403(request, exception):
    return render(request, '404.html', {}, status=403)

def custom500(request):
    return render(request, '500.html', {}, status=500)


def homepage(request):

    key = 'CG-ijyB17U95TbbzxurdFzBKi6H'

    endpoint = 'https://api.coingecko.com/api/v3/coins/markets'
    
    ids = ['bitcoin', 'ethereum', 'litecoin', 'ripple', 'cardano', 'tether', 'polygon', 'solana', 'polkadot', 'dogecoin', 'chainlink', 'avalanche', 'uniswap', 'monero', 'tron', 'stellar', 'eos']

    params = {
        'vs_currency': 'usd',
        'ids': ','.join(ids),
        'order': 'market_cap_desc',
        'sparkline': 'false',
        'price_change_percentage': '24h',
        'key': key,
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
    else:
        data = []

    return render(request, 'index.html', {'coins_data':data})

def services(request):
    return render(request, 'services.html')

def error(request):
    return render(request, '404.html')

def  price(request):
    message = messages.get_messages(request)
    return render(request, 'price.html', {'messages': message})

def team(request):
    message = messages.get_messages(request)
    return render(request, 'team.html',{'messages': message})


def signin(request):
    if request.method == 'POST':
        request.session.setdefault('login_attempts', 0)
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember-me')


        captcha = request.POST.get('g-recaptcha-response')

        if not captcha:
            messages.error(request, 'reCAPTCHA verification token is missing', extra_tags='login')
            return render(request, 'signin.html')
        
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
           'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
           'response': captcha,
           'remoteip': request.META['REMOTE_ADDR']
        }
        try:
            call = requests.post(url, data=values)
            response = call.json()
        except requests.RequestException as e:
            messages.error(request, f'Error while verifying reCAPTCHA: {str(e)}', extra_tags='login')
            return render(request, 'signin.html')
        except ValueError as e:
            messages.error(request, f'Error parsing reCAPTCHA response: {str(e)}', extra_tags='login')
            return render(request, 'signin.html')

        if not response['success']:
            messages.error(request, 'reCAPTCHA verification failed. Please try again.', extra_tags='login')
            return render(request, 'signin.html')

        if not (email and password):
            request.session['login_attempts'] += 1
            messages.error(request, 'Please enter valid login details for authentication...', extra_tags='login')
            return render(request, 'signin.html')

        user = authenticate(request, email=email, password=password) 
        if user is not None:
            try:
                is_valid = is_verified.objects.get(email=email)
            except is_verified.DoesNotExist:
                is_valid = None
            if is_valid is not None and not is_valid.verified:
                messages.error(request, 'Access denied, It looks like your email is not yet verified or you just have to verify again. Please request a verification code to continue', extra_tags='email')
                request.session['email'] = email
                return redirect('verify_email')
            
            try:
                detail = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                detail = None
            if detail is not None and detail.can_login:
               status = 'yes'
               if remember == status:
                    cookie = HttpResponse("Cookie saved")
                    cookie.set_cookie('username', email, max_age=86400)
                    request.session['username'] = email
                    print('Cookie saved')
                    login(request, user)
                    messages.success(request, f'Authentication successful🤩, Welcome {user.first_name}!', extra_tags='signin')
                    return redirect('home')
               
               login(request, user)
               messages.success(request, f'Authentication successful🤩, Welcome {user.first_name}!', extra_tags='signin')
               return redirect('home')
            elif detail is not None and not detail.can_login:
               messages.error(request, 'Access denied, It looks like your account is disabled. Please contact support team for help.', extra_tags='login')
               return render(request, 'signin.html')
            elif detail is None:
                messages.error(request, 'Authentication failed 😥, Please check your email or password and try again. And make sure you\'re registered!', extra_tags='login')
                return render(request, 'signin.html')


        else:
            request.session['login_attempts'] += 1
            if request.session['login_attempts'] >= 3:
                user = CustomUser.objects.filter(email=email).exists()
                if user: 
                    username = CustomUser.objects.get(email=email).pk
                    try:                 
                        detail = UserProfile.objects.get(user=username)
                    except UserProfile.DoesNotExist:
                        detail = None
                    if detail is not None:
                        detail.can_login = False
                        detail.save()
                        request.session['login_attempts'] = 0
                        messages.error(request, 'Maximum number of login attempts exceeded, your account is now disabled, please contact support.', extra_tags='login')
                        return render(request, 'signin.html')
                    else:
                        messages.error(request, 'Authentication failed 😥, Please check your email or password and try again. And make sure you\'re registered!', extra_tags='login')
                        return render(request, 'signin.html')
                else:
                    messages.error(request, 'Authentication failed 😥, Please check your email or password and try again. And make sure you\'re registered!', extra_tags='login')
                    return render(request, 'signin.html')
                
            messages.error(request, 'Authentication failed 😥, Please check your email or password and try again. And make sure you\'re registered!', extra_tags='login')
            return render(request, 'signin.html')
        
        
    elif request.method == 'GET':
        email = request.COOKIES.get('username')
        session_email = request.session.get('email')
        if not session_email:
            email = email
        else:
            email = session_email
        if email == None:
            user = authenticate(request, email=email)
            if user is not None:
                user = user.pk
                try:
                    is_valid = is_verified.objects.get(user=user)
                except is_verified.DoesNotExist:
                    is_valid = None

                if is_valid is not None and not is_valid.verified:
                    messages.error(request, 'Access denied, It looks like your email is not yet verified or you just have to verify again. Please request a verification code to continue', extra_tags='email')
                    request.session['email'] = email
                    return redirect('verify_email')

                try:
                    detail = UserProfile.objects.get(user=user)
                except UserProfile.DoesNotExist:
                    detail = None
                if detail is not None and detail.can_login:
                    login(request, user)
                    messages.success(request, f'Authentication successful🤩, Welcome {user.first_name}!', extra_tags='signin')
                    return redirect('home')
        
        print('Email not found')
        return render(request, 'signin.html')




def signup(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        nationality = request.POST.get('country')
        profile_picture = request.FILES.get('profile_picture')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        verification_code = random.randint(100000, 999999)
        consent = request.POST.get('consent')

        captcha = request.POST.get('g-recaptcha-response')

        if not captcha:
            messages.error(request, 'reCAPTCHA verification token is missing', extra_tags='secondary')
            return render(request, 'signup.html')
        
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
           'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
           'response': captcha,
           'remoteip': request.META['REMOTE_ADDR']
        }
        try:
            call = requests.post(url, data=values)
            response = call.json()
        except requests.RequestException as e:
            messages.error(request, f'Error while verifying reCAPTCHA: {str(e)}', 
            extra_tags='secondary')
            return render(request, 'signup.html')
        except ValueError as e:
            messages.error(request, f'Error parsing reCAPTCHA response: {str(e)}', extra_tags='secondary')
            return render(request, 'signup.html')

        if not response['success']:
            messages.error(request, 'reCAPTCHA verification failed. Please try again.', extra_tags='secondary')
            return render(request, 'signup.html')
        
        if not consent:
            messages.error(request, 'You forgot to consent to our terms of services and privacy policy.', extra_tags='secondary')
            return render(request, 'signup.html')
        else:
            consent = True

        if not (firstname and lastname and username and email and nationality and profile_picture and password1 and password2):
            messages.error(request, 'To get your Purse, Please fill all the form fields🙃.', extra_tags='secondary')
            return render(request, 'signup.html')
        
        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, f'Invalid email: {str(e)}', extra_tags='secondary')
            return render(request, 'signup.html')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Oops😥! Username is already taken. Do you want to Login instead?', extra_tags='secondary')
            return render(request, 'signup.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Oops😥! Email is already in use. Do you want to Login instead?', extra_tags='secondary')
            return render(request, 'signup.html')
        
        if password1 != password2:
            messages.error(request, 'Looks like there\'s a mismatch in your passwords.', extra_tags='secondary')
            return render(request, 'signup.html')

        user = CustomUser.objects.create_user(username=username, email=email, password=password1, first_name=firstname, last_name=lastname)
        user.save()
        UserProfile.objects.create(user=user, Profile_image=profile_picture, Nationality=nationality)
        current_time = timezone.now()
        is_verified.objects.create(user=user, email=email, verification_code=verification_code, creation_time=current_time, verified=False)
        request.session['email'] = email
        request.session['consent'] = consent

        subject = 'Please verify your email!'
        email_message = f'Hello {firstname} you just registered for a purse account with your Email address: {email}. please enter this code <h3><strong> {verification_code} </strong></h3> in the verification page to access your trading account.'
        from_email = 'alerts@myprofitpurse.com'
        recipient_list = [email]
        
        email_message = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
        email_message.content_subtype = 'html'
        email_message.send()

        subject = 'You have a new registered user!'
        email_message = f'A user named <h4>{firstname}</h4> Just registered on your website with the following details. Email address: {email}, Full name: <h4>{firstname} {lastname}</h4>, Nationality: <h4>{nationality}</h4>, & Username: <h4/>{username}</h4>. To see or manipulate user\'s full details, log into your administrator account.'
        from_email = 'alerts@myprofitpurse.com' 
        recipient_list = ['support@myprofitpurse.com']
        email = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
        email.content_subtype = 'html'
        email.attach_alternative(email_message, "text/html")
        email.send()
        return redirect('verify_email', )

    return render(request, 'signup.html')



def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('fullName')
        email = request.POST.get('email')
        message = request.POST.get('message')

        captcha = request.POST.get('g-recaptcha-response')

        if not captcha:
            attempts, created = Attempts.objects.get_or_create(pk=1)
            attempts.failed_attempts += 1
            attempts.save()
            messages.error(request, 'reCAPTCHA verification token is missing, please verify that you\'re not a robot', extra_tags='contact')
            return render(request, 'contact.html')
        
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
           'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
           'response': captcha,
           'remoteip': request.META['REMOTE_ADDR']
        }
        try:
            call = requests.post(url, data=values)
            response = call.json()
        except requests.RequestException as e:
            messages.error(request, f'Error while verifying reCAPTCHA: {str(e)}', extra_tags='contact')
            return render(request, 'contact.html')
        except ValueError as e:
            messages.error(request, f'Error parsing reCAPTCHA response: {str(e)}', extra_tags='contact')
            return render(request, 'contact.html')

        if not response['success']:
            attempts, created = Attempts.objects.get_or_create(pk=1)
            attempts.failed_attempts += 1
            attempts.save()
            messages.error(request, 'reCAPTCHA verification failed. Please try again.', extra_tags='contact')
            return render(request, 'contact.html')
        
        if not (name and email and message):
            messages.error(request, 'To send us a message, Please fill all the form fields🙃.', extra_tags='contact')
            return render(request, 'contact.html')
        if len(message) < 20 or len(name) < 5:
            messages.error(request, 'Either your message is too short or you didn\'t enter your full name. ', extra_tags='contact')
            return render(request, 'contact.html')
        
        Messages.objects.create(name=name, email=email, message=message)
        
        subject = f'New message from {name}'
        email_message = f'Hello admin, <h4>"{name}" </h4> just sent you a message: <em>"{message}". </em> Send response to this email address: <a href="mailto:{email}"><em>{email}</em></a>'
        from_email = 'alerts@myprofitpurse.com'
        recipient_list = ['support@myprofitpurse.com']
        email = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
        email.content_subtype = 'html'
        email.attach_alternative(email_message, "text/html")
        email.send()
        messages.success(request, 'your message has been sent, We will reach you through the provided email address', extra_tags='contact')
        return render(request, 'contact.html')
    return render(request, 'contact.html')


def is_subscribed(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            messages.error(request, 'Please enter a valid email address.', extra_tags='newsletter')
            return redirect('homepage/team')

        messages.success(request, f'Thank you for subscribing to our newsletter, You are subscibed as "{email}".  We will periodically send you you mail notifications about our upcoming events and general updates.', extra_tags='newsletter')

        return redirect('homepage/team')
    
    return redirect('homepage/team')



def request_verification(request): 
    email = request.session.get('email')
    request.session.setdefault('trials', 0)
    request.session['trials'] += 1
    request.session.set_expiry(timedelta(minutes=15))
    if request.session['trials'] >= 3:
        is_visible = False
        messages.error(request, 'Oops! Something went wrong or you\'re just too fast. ', extra_tags='email')
        return render(request, 'email_verify.html', {
            'email': email, 
            'is_visible': is_visible
            })
    try:
        is_valid = is_verified.objects.get(email=email)
    except is_verified.DoesNotExist:
       is_valid = None
    if is_valid is not None:
        user = is_valid.user
        verification_code = random.randint(100000, 999999)
        new_object = is_verified.objects.get(user=user)
        
        new_object.email = email
        new_object.verification_code = verification_code
        new_object.creation_time = timezone.now()
        new_object.save()
        
        subject = 'Please verify your email!'
        body = f'You just requested for a purse account email verification code to your Email address: {email}. please enter this code <h3><strong> {verification_code} </strong></h3> in the verification page to access your trading account.'
        from_email = 'alerts@myprofitpurse.com'
        recipient_list = [email]

        
        email_message = EmailMultiAlternatives(subject, body, from_email, recipient_list)
        email_message.content_subtype = 'html'
        email_message.send()
        is_valid = True
        messages.success(request, f'Verification Code sent successfully to {email}', extra_tags='email')
        return render(request, 'email_verify.html', {'email': email, 'is_valid': is_valid})

    else:
        messages.error(request, 'Oops! Something went wrong. Please try again.', extra_tags='email')
        return render(request, 'email_verify.html', {'email': email, 'is_valid': is_valid})



def verify_email(request):

    # Store a data to be used for manipulating the state of the page, like what the user sees.
    is_valid = True
    # extract messages stored in request
    message = messages.get_messages(request)

    # set a key for tracking user attempts and prevent brute force attacks
    request.session.setdefault('verification_trials', 0)

    # extract email stored in request session
    email = request.session.get('email')

    # if email is not on the request session, give the user a form to enter it
    if email is None:
        return redirect('homepage/signin')
    
    # get data from form submitted by user and validate. but first check if the user actually submitted a form.
    if request.method == 'POST':

        #  increment user attempts counter for every request
        request.session['verification_trials'] += 1

        # prevent further requests from the user after a certain number of requests
        if request.session['verification_trials'] == 5:
            messages.error(request, 'Something went wrong, please try again later', extra_tags='email')
            return render(request, 'email_verify.html', {'email': email, 'is_valid': True, 'message':message})
        # Get the code from the the form the user submitted
        code = request.POST.get('code')

        #  try to get an email from the form and replace with what was received from the server earlier
        form_email = request.POST.get('email')

        # if email is not submitted, use the email received from the server earlier
        if not form_email:
            email = email 
        else:
            email = form_email

        # if code is not submitted and the user submitted a form, take them back 🥴 lmao.
        if not code:
            messages.error(request, 'Please enter a six digit code sent to your email. ', extra_tags='email')
            return render(request, 'email_verify.html', {'email': email, 'is_valid':is_valid})

        # if code is submitted, code continues running >>>.

        # attempt to validate the email and code submitted by the user
        try:
            verified_object = is_verified.objects.get(verification_code=code, email=email)
        # if there is nothing like what was submitted,  then it is considered invalid
        except is_verified.DoesNotExist:
            messages.error(request, 'Invalid verification code or Something isn\'t just right with your verification. Please try again.', extra_tags='email')
            return render(request, 'email_verify.html', {'email': email, 'messages': message, 'is_valid':False})

        # if the code is  valid, check if the code has expired, and if so, return the request accordingly with some additional informations important to the user.
        currentTime = timezone.now()
        timeoutDuration = timedelta(minutes=15)
        if currentTime - verified_object.creation_time > timeoutDuration:
            messages.error(request, 'Looks like the code is no longer valid. Please request a new one', extra_tags='email')
            return render(request, 'email_verify.html', {'email': email, 'messages': message, 'is_valid':False})
        
        # if we manage to bypass all the checkpoints defined above, then we're good to go.

        # verify the user's email.
        verified_object.verified = True
        # reset the verification code of the user
        verified_object.verification_code = 0
        verified_object.save()

        messages.success(request, 'Your email address has been verified. trying to reach myPurse app....', extra_tags='email')
        request.session['email'] = ''
        # login the user.
        user = verified_object.user
        login(request, user)
        # redirect the user to the home page or anywhere.
        return redirect('home')
    
    
    # all of that works only when the user submitted a form. if the user did not submit a form, then the user is requesting the form.  give the user the form.
    return render(request, 'email_verify.html', {'email': email, 'messages': message, 'is_valid': is_valid})