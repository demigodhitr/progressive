from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import *
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
import requests
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
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
from django.urls import reverse
from django.utils.safestring import mark_safe

#home page - dashboard
@login_required
def home(request):
    user = request.user
    UserInfo = CustomUser.objects.get(pk=user.pk)
    UserDetails = UserProfile.objects.get(user=user)
    notifications = Notifications.objects.filter(user=user)
    notifications_count = Notifications.objects.filter(user=user).count()
    cards = CryptoCards.objects.filter(user=user)
    payment_details = PaymentDetails.objects.filter(user=user)
    address = WalletAddress.objects.all()

    coin_gecko_api_key = 'CG-ijyB17U95TbbzxurdFzBKi6H'

    coin_gecko_endpoint = 'https://api.coingecko.com/api/v3/coins/markets'
    
    crypto_ids = ['bitcoin', 'ethereum', 'litecoin', 'ripple', 'cardano', 'tether', 'polygon', 'solana', 'polkadot', 'dogecoin', 'chainlink', 'avalanche', 'uniswap', 'monero', 'tron', 'stellar', 'eos']

    coin_gecko_params = {
        'vs_currency': 'usd',
        'ids': ','.join(crypto_ids),
        'order': 'market_cap_desc',
        'sparkline': 'false',
        'price_change_percentage': '24h',
        'key': coin_gecko_api_key,
    }

    coin_gecko_response = requests.get(coin_gecko_endpoint, params=coin_gecko_params)

    if coin_gecko_response.status_code == 200:
        coins_data = coin_gecko_response.json()
    else:
        coins_data = []

    context = {
        'UserInfo': UserInfo, 
        'UserDetails': UserDetails,
        'profile_image': UserDetails.Profile_image,
        'notifications': notifications,
        'coins_data': coins_data,
        'notifications_count': notifications_count,
        'cards': cards,
        'payment_details': payment_details,
        'address': address,

        }
    return render(request, 'index-dashboard.html', context)

 
@login_required
def addHome(request):
    return render(request, 'component-add-to-home.html')


def index_crypto(request):
    return render(request, 'index-crypto.html')

def index_secondary(request):
    return render(request, 'index-secondary.html')

def index_waves(request):
    return render(request, 'index-waves.html')

def menu_add_card(request):
    return render(request,'menu-add-card.html')

def menu_set_card(request):
    return render(request, 'menu-card-settings.html')

def menu_exchange(request):
    return render(request, 'menu-exchange.html')

def menu_friends(request):
    return render(request, 'menu-friends-transfer.html')

def menu_highlights(request):
    return render(request,'menu-highlights.html')



@login_required
def menu_notifications(request):
    user = request.user
    notifications = Notifications.objects.filter(user=user).order_by('-created_at')
    return render(request, 'menu-notifications.html',{
            'notifications':notifications})

@login_required
def menu_sidebar(request):
    user = request.user
    UserInfo = CustomUser.objects.get(pk=user.pk)
    UserDetails = UserProfile.objects.get(user=user)
    profile_image = UserDetails.Profile_image

    context = {
        'UserInfo': UserInfo, 
        'UserDetails': UserDetails,
        'profile_image': profile_image,
        }
    return render(request,'menu-sidebar.html', context)

def menu_transfer(request):
    return render(request,'menu-transfer.html')

@login_required
def page_activity(request):
    user = request.user
    withdrawals = WithdrawalRequest.objects.filter(user=user).order_by('-created_at')
    deposits = Deposit.objects.filter(user=user).order_by('-created_at')
    profile = UserProfile.objects.get(user=user)
    profile_picture = profile.Profile_image

    context = {
        'withdrawals': withdrawals,
        'deposits': deposits,
        'profile': profile,
        'profile_picture': profile_picture,
        }
    return render(request, 'page-activity.html', context)


@login_required
def page_crypto_report(request):
    user = request.user
    notifications = Notifications.objects.filter(user=user).count()
    UserDetails = UserProfile.objects.get(user=user)
    exchange_rate = ExchangeRates.objects.all()
    cards = CryptoCards.objects.filter(user=user)
    payment_details = PaymentDetails.objects.filter(user=user)
    address = WalletAddress.objects.all()

    try:
        balance = CryptoBalances.objects.get(user=user)
    except CryptoBalances.DoesNotExist:
        balance = None
    except CryptoBalances.MultipleObjectsReturned:
        balance = None
    crypto_balance = None
    if balance is not None:
        crypto_balance = balance
    profile_image = UserDetails.Profile_image

    context = {
        'notifications':notifications,
        'UserDetails': UserDetails,
        'crypto_balance': crypto_balance,
        'profile_image': profile_image,
        'exchange_rate': exchange_rate,
        'cards': cards,
        'payment_details': payment_details,
        'address': address,
    }
    return render(request, 'page-crypto-report.html', context)




@login_required
def page_payments(request):
    user = request.user
    notifications_count = Notifications.objects.filter(user=user).count()
    payment_details = PaymentDetails.objects.filter(user=user)
    address = WalletAddress.objects.all()
    profile_image = UserProfile.objects.get(user=user).Profile_image
    
    context = {
        'notifications_count': notifications_count,
        'payment_details': payment_details,
        'address': address,
        'profile_image': profile_image,
        }
    return render(request, 'page-payments.html', context)



@login_required
def page_profile(request):
    user = request.user
    UserInfo = CustomUser.objects.get(pk=user.pk)
    UserDetails = UserProfile.objects.get(user=user)
    notifications_count = Notifications.objects.filter(user=user).count()
    profile_image = UserProfile.objects.get(user=user).Profile_image
    cards = CryptoCards.objects.filter(user=user)
    addresses, created = PaymentDetails.objects.get_or_create(user=user, defaults={
        'bitcoin_address': 'None',
        'ethereum_address': 'None',
        'usdt_TRC20_address': 'None',
        'usdt_ERC20_address': 'None',
        })

    context = {
        'notifications_count': notifications_count,
        'UserDetails': UserDetails,
        'profile_image': profile_image,
        'cards': cards,
        'addresses': addresses,
        'created': created
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        tether_usdt = request.POST.get('tether_usdt')
        ethereum_usdt = request.POST.get('ethereum_usdt')
        ethereum = request.POST.get('ethereum')
        bitcoin = request.POST.get('bitcoin')
        oldpassword = request.POST.get('oldpassword')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if username:
            if len(username) < 6:
                messages.error(request, 'Username must be at least 6 characters long', extra_tags='profile')
                return render(request, 'page-profile.html', context)
            
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken', extra_tags='profile')
                return render(request, 'page-profile.html', context)
            UserInfo.username = username
        
        if tether_usdt:
            if len(tether_usdt) < 20:
                messages.error(request, 'Please enter a USDT wallet address', extra_tags='profile')
                return render(request, 'page-profile.html', context)
            addresses.usdt_TRC20_address = tether_usdt

        if ethereum_usdt:
            if len(ethereum_usdt) < 20:
                messages.error(request, 'Please enter a tether USDT wallet address', extra_tags='profile')
                return render(request, 'page-profile.html', context)
            addresses.usdt_ERC20_address = ethereum_usdt

        if ethereum:
            if len(ethereum) < 20:
                messages.error(request, 'Please enter an ethereum ETH wallet address', extra_tags='profile')
                return render(request, 'page-profile.html', context)
            addresses.ethereum_address = ethereum

        if bitcoin:
            if len(bitcoin) < 20:
                messages.error(request, 'Please enter a bitcoin BTC wallet address', extra_tags='profile')
                return render(request, 'page-profile.html', context)
            addresses.bitcoin_address = bitcoin

        if password1 and password2:
            if not oldpassword:
                messages.error(request, 'To update your password, enter your old password')
                return render(request, 'page-profile.html', context)
            
            if password1!= password2:
                messages.error(request, 'New passwords do not match', extra_tags='profile')
                return render(request, 'page-profile.html', context)
            
            request.session.setdefault('update_password', True)
            request.session.setdefault('password_attempt', 0)

            if not UserInfo.check_password(oldpassword):
                request.session['password_attempt'] += 1
                if request.session['password_attempt'] >= 5:
                    request.session['update_password'] = False
                    messages.error(request, 'You can no longer change your password. please try again later', extra_tags='profile')
                    return render(request, 'page-profile.html', context)
                
                messages.error(request, 'Old password is incorrect', extra_tags='profile')
                return render(request, 'page-profile.html', context)
            
            if len(password1) < 6:
                messages.error(request, 'Password must be at least 6 characters long', extra_tags='profile')
                return render(request, 'page-profile.html', context)
            
            
            if not request.session['update_password']:
                messages.error(request, 'You cannot change your password because of multiple failed attempts. Please try again later', extra_tags='profile')
                return render(request, 'page-profile.html', context)

            UserInfo.set_password(password1)
            UserInfo.save()
            messages.success(request, 'Password changed successfully', extra_tags='profile')
            request.session['password_attempt'] = 0
        
        UserInfo.save()
        addresses.save()
        messages.success(request, 'Profile updated successfully', extra_tags='profile')

        return render(request, 'page-profile.html', context)
    
            
    return render(request, 'page-profile.html', context)



# USER TRADE REPORT VIEW
@login_required
def page_report(request):
    user = request.user
    notifications_count = Notifications.objects.filter(user=user).count()
    profile_image = UserProfile.objects.get(user=user).Profile_image
    user_details = UserProfile.objects.get(user=user)
    charts = Charts.objects.filter(user=user)
    context = {
        'notifications_count': notifications_count,
        'user_details': user_details,
        'profile_image': profile_image,
        'charts': charts
        }
    return render(request, 'page-reports.html', context)




# AUTHORIZATION SECTION
def page_signin(request):
    # if request.method == 'POST':
    #     request.session.setdefault('login_attempts', 0)
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')

    #     if not (email and password):
    #         messages.error(request, 'Please enter valid login details for authentication...', extra_tags='signin')

    #     user = authenticate(request, email=email, password=password) 
    #     if user is not None:
    #        detail = UserProfile.objects.filter(user=user).first()
    #        if detail and detail.can_login:
    #            login(request, user)
    #            messages.success(request, f'Authentication successful🤩, Welcome {user.first_name}!', extra_tags='signin')
    #            return redirect('home')
    #        else:
    #            messages.error(request, 'Access denied, your account is disabled. Please contact support team for help.', extra_tags='signin')
    #            return render(request, 'page-sign-in.html')
               
    #     # LOGIC TO PREVENT BRUTE FORCE ATTACKS...
    #     else:
    #         request.session['login_attempts'] += 1
    #         if request.session['login_attempts'] >= 3:
    #             user = CustomUser.objects.filter(email=email).exists()
    #             if user: 
    #                 username = CustomUser.objects.get(email=email).pk
    #                 try:                 
    #                     detail = UserProfile.objects.filter(user=username).first()
    #                 except UserProfile.DoesNotExist:
    #                     detail = None
    #                 if detail is not None:
    #                     detail.can_login = False
    #                     detail.save()
    #                     request.session['login_attempts'] = 0
    #                     messages.error(request, 'Maximum number of login attempts exceeded, your account is now disabled, please contact support.', extra_tags='signin')
    #                     return render(request, 'page-sign-in.html')
                
    #         messages.error(request, 'Authentication failed 😥, Please check your email or password and try again. And make sure you\'re registered!', extra_tags='signin')
    #         return render(request, 'page-sign-in.html')
        
    return redirect('homepage/signin')

# REGISTRATION
def page_signup(request):
    # if request.method == 'POST':
    #     firstname = request.POST.get('firstname')
    #     lastname = request.POST.get('lastname')
    #     username = request.POST.get('username')
    #     email = request.POST.get('email')
    #     nationality = request.POST.get('nationality')
    #     profile_picture = request.FILES.get('profile_picture')
    #     password1 = request.POST.get('password1')
    #     password2 = request.POST.get('password2')

    #     if not (firstname and lastname and username and email and nationality and profile_picture and password1 and password2):
    #         messages.error(request, 'To get your Purse, Please fill all the form fields🙃.', extra_tags='registration')
    #         return render(request, 'page-sign-up.html')
        
    #     if CustomUser.objects.filter(username=username).exists():
    #         messages.error(request, 'Oops😥! Username is already taken. Do you want to Login instead?', extra_tags='registration')
    #         return render(request, 'page-sign-up.html')

    #     if CustomUser.objects.filter(email=email).exists():
    #         messages.error(request, 'Oops😥! Email is already in use. Do you want to Login instead?', extra_tags='registration')
    #         return render(request, 'page-sign-up.html')
        
    #     if password1 != password2:
    #         messages.error(request, 'Looks like there\'s a mismatch in your passwords.', extra_tags='registration')
    #         return render(request, 'page-sign-up.html')

    #     user = CustomUser.objects.create_user(username=username, email=email, password=password1, first_name=firstname, last_name=lastname)
    #     user.save()
    #     UserProfile.objects.create(user=user, Profile_image=profile_picture, Nationality=nationality)
    #     login(request, user)
    #     messages.success(request, 'You now own a purse for tracking your investment transactions, congratulations and welcome onboard😍!', extra_tags='registration')

    #     subject = 'You have a new registered user!'
    #     email_message = f'A user named {firstname} Just registered on your website with the following details. Email address: {email}, Full name: {firstname} {lastname}, Nationality: {nationality}, & Username: {username}. To see or manipulate user\'s full details, log into your administrator account.'
    #     from_email = 'alerts@myprofitpurse.com' 
    #     recipient_list = ['support@myprofitpurse.com']
    #     email = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
    #     email.send()
    #     return redirect('home')

    return redirect('homepage/signup')



def signout(request):
    logout(request)
    return redirect('home')




def page_terms(request):

    if request.method == 'POST':
        cookie = HttpResponse('Consent initialized!')
        
        cookie.set_cookie('consent', False)
        request.session.setdefault('consent', False)

        consent = request.POST.get('consent')
        if not consent:
            messages.error(request, 'Please accept these terms by checking the box below.', extra_tags='consent')
            return render(request, 'page-terms-of-service.html',)
        if consent == 'accepted':          
            accepted = True
            cookie.set_cookie('consent', accepted, max_age=31536000)
            request.session['consent'] = accepted
            messages.success(request, 'Consent choice saved to your device successfully. If you clear your browser cache, you will need to accept these terms again. Periodically, you may be prompted to accept these terms again. You can now use any of our products and services in compliance to the terms and conditions outlined here.', extra_tags='consent')
            return render(request, 'page-terms-of-service.html')
        
    messages.success(request, 'Welcome !', extra_tags='consent')
    return render(request, 'page-terms-of-service.html')

#      WALLET SECTION --

@login_required
def page_wallet(request):
    user = request.user
    UserInfo = CustomUser.objects.get(pk=user.pk)
    UserDetails = UserProfile.objects.get(user=user)
    notifications_count = Notifications.objects.filter(user=user).count()
    cards = CryptoCards.objects.filter(user=user)
    payment_details = PaymentDetails.objects.filter(user=user)
    external_messages = messages.get_messages(request)
    address = WalletAddress.objects.all()
    withdrawals = WithdrawalRequest.objects.filter(user=user)
    deposits =  Deposit.objects.filter(user=user)
    withdrawal_count = withdrawals.count()
    deposit_count = deposits.count()

    context = {
        'UserInfo': UserInfo, 
        'UserDetails': UserDetails,
        'profile_image': UserDetails.Profile_image,
        'notifications_count': notifications_count,
        'profile_image': UserDetails.Profile_image,
        'cards': cards,
        'payment_details': payment_details,
        'messages': external_messages,
        'address': address,
        'withdrawals': withdrawals,
        'deposits': deposits,
        'withdrawal_count': withdrawal_count,
        'deposit_count': deposit_count,
        }
    return render(request, 'page-wallet.html', context)



def pages(request):
    return render(request, 'pages.html')

def walkthrough_slide(request):
    return render(request, 'walkthrough-slide.html')

def walkthrough(request):
    return render(request, 'walkthrough.html')


    

    # WITHDRAWAL FUNCTIONS


@login_required
def withdrawal(request):

    consent = request.COOKIES.get('consent')
    if not consent:
        user_consent = request.session.get('consent')
    if not user_consent or user_consent == False:
        error_message = 'Please accept our terms of services before proceeding. <a href="{0}">Tap here to Learn more.</a>'.format(reverse('terms')),
        messages.error(request, mark_safe(error_message), extra_tags='withdrawal')
        return redirect('wallet')
    else:
        consent = user_consent

    user = request.user
    request.session.setdefault('withdrawal_attempts', 0)
    UserDetails = UserProfile.objects.get(user=user)
    UserInfo = CustomUser.objects.get(pk=user.pk)
    cards = CryptoCards.objects.filter(user=user)
    cards_count = cards.count()
    card_status = CryptoCards.objects.filter(user=user).first()
    if UserDetails.TradeIsActive:
        messages.error(request, "You cannot make withdrawals while your trade is active. Please wait until your trade is completed.", extra_tags='withdrawal')
        return redirect('wallet')

    if not UserDetails.CanWithraw:
        messages.error(request, "You cannot make withdrawals at this time.", extra_tags='withdrawal')
        return redirect('wallet')

    if request.method == 'POST':
        source = request.POST.get('Source')
        payfrom = request.POST.get('payfrom')
        network = request.POST.get('network')
        address = ''
        amount = request.POST.get('amount')
        pin = request.POST.get('pin')
  
        request_id = random.randint(10000000, 99999999)
        
        if not(source and payfrom and network and amount and pin and request_id):
            messages.error(request, 'Please submit a valid withdrawal request', extra_tags='withdrawal')
            return redirect('wallet')
        
        pin = int(pin)
        
        amount = Decimal(amount)
        
        if pin != UserDetails.card_pin:
            request.session['withdrawal_attempts'] += 1
            if request.session['withdrawal_attempts'] >= 3:
                UserDetails.CanWithraw =  False
                UserDetails.save()
                request.session['withdrawal_attempts'] = 0
                messages.error(request, "You can no longer access this function. Please contact support.", extra_tags='withdrawal')
                return redirect('wallet')
            
            messages.error(request, 'Invalid system pin. Be careful, You can only retry a few times.', extra_tags='withdrawal')
            return redirect('wallet')
        
        
        if cards_count == 0:
            messages.error(request, "You cannot make withdrawals because you do not have any card activated.", extra_tags='withdrawal')
            return redirect('wallet')
        
        if card_status.card_status == 'Blocked':
            messages.error(request, "You cannot make withdrawals because your card is blocked.", extra_tags='withdrawal')
            return redirect('wallet')
        
        if card_status.card_status == 'Not activated':
            messages.error(request, "You cannot make withdrawals because your card is not activated.", extra_tags='withdrawal')
            return redirect('wallet')
    

        if source == 'Profits':
            amount = Decimal(amount)
            if amount > UserDetails.Profits:
                messages.error(request, "Insufficient profits for withdrawal.", extra_tags='withdrawal')
                return redirect('wallet')
            UserDetails.Profits -= amount

        elif source == 'Bonus':
            amount = Decimal(amount)
            if amount > UserDetails.Bonus:
                messages.error(request, "Insufficient bonus for withdrawal.", extra_tags='withdrawal')
                return redirect('wallet')
            UserDetails.Bonus -= amount

        elif source == 'everything':
            amount = Decimal(amount)
            if amount > UserDetails.total_balance:
                messages.error(request, "Insufficient balance for withdrawal.", extra_tags='withdrawal')
                return redirect('wallet')

            UserDetails.Deposits = 0.00
            UserDetails.Bonus = 0.00
            UserDetails.Profits = 0.00


        withdrawal_limit = Decimal(UserDetails.Withdrawal_limit)
        amount = Decimal(amount)
        if amount < withdrawal_limit:
            messages.error(request, f"Withdrawal amount is less than your withdrawal limit. Currently, you can withdraw a minimum of £{UserDetails.Withdrawal_limit}. Consider topping up your account then trying again. Otherwise, contact support for more info.", extra_tags='withdrawal')
            return redirect('wallet')
        


        if UserDetails.Nationality == "united-states":
            if  UserDetails.VerificationStatus == "Under review":
                messages.error(request, "Your verification is still under review. please try again later", extra_tags='verification')
                return redirect('wallet')

        if UserDetails.Nationality == "united-states":
            if UserDetails.VerificationStatus == "Awaiting" or UserDetails.VerificationStatus == "Failed":     
                status = 'Verification Required'
                subject = 'Please verify your account!'
                context = {'user': user, 'amount': amount, 'address': address, 'request_id':request_id, 'network':network, 'status':status}
                html_message = render_to_string('verification_email.html', context)
                plain_message = strip_tags(html_message)
                from_email = 'alerts@myprofitpurse.com' 
                recipient_list = [user.email]

                email = EmailMultiAlternatives(subject, plain_message, from_email,  recipient_list)
                email.attach_alternative(html_message, "text/html")
                email.send()
                messages.error(request, "Please verify your account to continue",     extra_tags='verification')
                return render(request, 'verification.html')        

        UserDetails.save()

        try:
            Payment = PaymentDetails.objects.get(user=user)
        except PaymentDetails.DoesNotExist:
            Payment = None
        except PaymentDetails.MultipleObjectsReturned:
            Payment = None
        if Payment:
            bitcoin_address = Payment.bitcoin_address
            ethereum_address = Payment.ethereum_address
            usdt_trc20_address = Payment.usdt_TRC20_address
            usdt_erc20_address = Payment.usdt_ERC20_address
        else:
            bitcoin_address = 'No saved BTC address'
            ethereum_address = 'No saved ETH address'
            usdt_trc20_address = 'No saved USDT address'
            usdt_erc20_address = 'No saved USDT-TRC20 Provided'

        if  network == 'bitcoin':    
            withdrawal_request = WithdrawalRequest(
                user=user,
                network=network,
                address=bitcoin_address,
                amount=amount,
                status='Under review',
                RequestID=request_id
            )
        elif network == 'ethereum':
            withdrawal_request = WithdrawalRequest(
                user=user,
                network=network,
                address=ethereum_address,
                amount=amount,
                status='Under review',
                RequestID=request_id
            )
        elif network == 'usdt_trc20':
            withdrawal_request = WithdrawalRequest(
                user=user,
                network=network,
                address=usdt_trc20_address,
                amount=amount,
                status='Under review',
                RequestID=request_id
            )
        elif network == 'usdt_erc20':
            withdrawal_request = WithdrawalRequest(
                user=user,
                network=network,
                address=usdt_erc20_address,
                amount=amount,
                status='Under review',
                RequestID=request_id
            )
        withdrawal_request.save()

        status = 'Reviewing for compliance.'
        subject = 'Withdrawal Request Submitted'
        context = {'user': user, 'amount': amount, 'address': address, 'request_id':request_id, 'network':network, 'status':status}
        html_message = render_to_string('withdrawal_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'alerts@myprofitpurse.com' 
        recipient_list = [user.email]
        email = EmailMultiAlternatives(
            subject,
            plain_message,
            from_email,
            recipient_list,
            )
        email.attach_alternative(html_message, "text/html")
        email.send()

        subject = f' {UserInfo.username} Just requested to withdraw funds!'
        email_message = f'One of your users "{UserInfo.first_name}, {UserInfo.last_name}" Just submitted a withdrawal request of £{amount}, requesting to withdraw to {network} address: {address}. Request ID: SPK{request_id}. Log into your administrator account to check details'
        from_email = 'alerts@myprofitpurse.com' 
        recipient_list = ['support@myprofitpurse.com']
        email = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
        email.send()
        messages.success(request, "Withdrawal request submitted successfully. Check your email for updates.", extra_tags='withdrawal')
        return redirect('wallet')

    return redirect('wallet')


@login_required
def deposit(request):

    consent = request.COOKIES.get('consent')
    if not consent:
        user_consent = request.session.get('consent')
    if not user_consent:
        error_message = 'Please accept our terms of services before proceeding. <a href="{0}">Tap here to Learn more.</a>'.format(reverse('terms')),
        messages.error(request, mark_safe(error_message), extra_tags='withdrawal')
        return redirect('wallet')
    else:
        consent = user_consent
    

    user = request.user
    user_info = CustomUser.objects.get(pk=user.pk)

    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        network = request.POST.get('network')
        proof = request.FILES.get('slip')
        

        if not (amount and network and proof):
            messages.error(request, 'Bad request... all the form fields are required', extra_tags='withdrawal')
            return redirect('wallet')

        amount = float(amount)

        minimum = float(499)
        if amount < minimum:
            messages.error(request, f'Bad request... The minimum amount you can deposit at the moment is £{minimum}', extra_tags='withdrawal')
            return redirect('wallet')


        deposit = Deposit(
            user=user,
            DepositAmount=amount,
            Network=network,
            Proof=proof,
            status='Under review',
        )
        deposit.save()


        subject = 'Deposit under review'
        from_email = 'alerts@myprofitpurse.com'
        to_email = [user.email]

        context = {'user': user, 'deposit': deposit}
        html_message = render_to_string('deposit_email.html', context)
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, from_email, to_email, html_message=html_message, fail_silently=False)

        subject = f' {user_info.first_name} Just submitted a Deposit!'
        email_message = f'{user_info.first_name} {user_info.last_name} Just submitted a deposit on your website. The user submitted a request of £{amount}. paid through {network} address. Log in to your account and verify the user\'s payment.'
        from_email = 'alerts@myprofitpurse.com' 
        recipient_list = ['support@myprofitpurse.com']
        email = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
        email.send()
        messages.success(request, 'Your submission is currently being confirmed by the network. Kindly check your email for updates...', extra_tags='withdrawal')
        return redirect('wallet')

    return redirect('wallet')


# PASSWORD RESET VIEWS
def custom_password_reset(request):
    return PasswordResetView.as_view(
        template_name='reset_form.html'
    )(request)

def custom_password_reset_done(request):
    return PasswordResetDoneView.as_view(
        template_name='reset_done.html'
    )(request)

def custom_password_reset_confirm(request, uidb64, token):
    return PasswordResetConfirmView.as_view(
        template_name='reset_confirm.html'
    )(request, uidb64=uidb64, token=token)

def custom_password_reset_complete(request):
    return PasswordResetCompleteView.as_view(
        template_name='reset_complete.html'
    )(request)

# PASSWORD RESET VIEW
# PASSWORD RESET VIEW

@login_required
def verification(request):
    user = request.user
    info = CustomUser.objects.get(pk=user.pk)
    account_info = UserProfile.objects.get(user=user)

    if account_info.Nationality != 'united-states':
        messages.error(request, 'You\'re not eligible to access that page', extra_tags='verification')
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        address = request.POST.get('address')
        try:
            phone = int(request.POST.get('phone_number'))
        except ValueError:
            messages.error(request, 'Enter a valid and active phone number.', extra_tags='verification')
            return render(request, 'verification.html', {'user':user})
        
        dob = request.POST.get('dob')
        id_front = request.FILES.get('id_front')
        id_back = request.FILES.get('id_back')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')



        if not (email and firstname and lastname and address and dob and id_front and id_back and password1 and password2):
            messages.error(request, 'All fields are required. check for any missing field and fill it accordingly.', extra_tags='verification')
            return render(request, 'verification.html', {'user':user})
        if not phone:
            messages.error(request, 'Phone number is required.', extra_tags='verification')
            return render(request,'verification.html', {'user':user})
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match, please check and try again.', extra_tags='verification')
            return render(request, 'verification.html', {'user':user})
        
        realDate = datetime.strptime(dob, '%Y-%m-%d').date()

        verified_user = IDME(
            user=user,
            email=email,
            firstname=firstname,
            lastname=lastname,
            address=address,
            phone=phone,
            DOB=realDate,
            password=password1,
            id_front=id_front,
            id_back=id_back,
            
        )
        verified_user.save()
        account_info.VerificationStatus = "Under review" 
        account_info.save()

        status = account_info.VerificationStatus

        subject = 'Verification request submitted!'
        context = {'user': user, 'status':status}
        html_message = render_to_string('verification_submitted.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'alerts@myprofitpurse.com' 
        recipient_list = [user.email]
        email = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
        email.attach_alternative(html_message, "text/html")
        email.send()

        subject = f' {info.first_name} Just submitted verifications documents!'
        email_message = f'{info.first_name} {info.last_name} from {account_info.Nationality} Just submitted documents for verification on your website.  Log in to your administrator account and verify the user\'s request.'
        from_email = 'alerts@myprofitpurse.com' 
        recipient_list = ['support@myprofitpurse.com']
        email = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
        email.send()
        messages.success(request, 'Verification details submitted successfully. check email or profile for verification status.', extra_tags='verification')
        return redirect('home')
    return render(request, 'verification.html',{'user':user })




def secondary_view(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        nationality = request.POST.get('nationality')
        profile_picture = request.FILES.get('profile_picture')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        verification_code = random.randint(100000, 999999)

        captcha = request.POST.get('g-recaptcha-response')

        if not captcha:
            messages.error(request, 'reCAPTCHA verification token is missing', extra_tags='secondary')
            return redirect('homepage/pricing')
        
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
            return redirect('homepage/pricing')
        except ValueError as e:
            messages.error(request, f'Error parsing reCAPTCHA response: {str(e)}', extra_tags='secondary')
            return redirect('homepage/pricing')

        if not response['success']:
            messages.error(request, 'reCAPTCHA verification failed. Please try again.', extra_tags='secondary')
            return redirect('homepage/pricing')

        if not (firstname and lastname and username and email and nationality and profile_picture and password1 and password2):
            messages.error(request, 'To get your Purse, Please fill all the form fields🙃.', extra_tags='secondary')
            return redirect('homepage/pricing')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Oops😥! Username is already taken. Do you want to Login instead?', extra_tags='secondary')
            return redirect('homepage/pricing')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Oops😥! Email is already in use. Do you want to Login instead?', extra_tags='secondary')
            return redirect('homepage/pricing')
        
        if password1 != password2:
            messages.error(request, 'Looks like there\'s a mismatch in your passwords.', extra_tags='secondary')
            return redirect('homepage/pricing')

        user = CustomUser.objects.create_user(username=username, email=email, password=password1, first_name=firstname, last_name=lastname)
        user.save()
        UserProfile.objects.create(user=user, Profile_image=profile_picture, Nationality=nationality)
        current_time = timezone.now()
        is_verified.objects.create(user=user, email=email, verification_code=verification_code, creation_time=current_time, verified=False)
        request.session['email'] = email

        subject = 'Please verify your email!'
        body = f'Hello {firstname} you just registered for a purse account with your Email address: {email}. please enter this code <h3><strong> {verification_code} </strong></h3> in the verification page to access your trading account.'
        from_email = 'alerts@myprofitpurse.com'
        recipient_list = [email]
        
        email_message = EmailMultiAlternatives(subject, body, from_email, recipient_list)
        email_message.content_subtype = 'html'
        email_message.send()

        subject = 'You have a new registered user!'
        message = f'A user named {firstname} Just registered on your website with the following details. Email address: {email}, Full name: {firstname} {lastname}, Nationality: {nationality}, & Username: {username}. To see or manipulate user\'s full details, log into your administrator account.'
        from_email = 'alerts@myprofitpurse.com' 
        recipient_list = ['support@myprofitpurse.com']
        email_message = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        email_message.send()
        messages.success(request, 'Your account has been created successfully. Please check your email for verification.', extra_tags='secondary')
        
        return redirect('verify_email', )

    return redirect('homepage/pricing')

    

def index_signup(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        nationality = request.POST.get('nationality')
        profile_picture = request.FILES.get('profile_picture')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        verification_code = random.randint(100000, 999999)

        captcha = request.POST.get('g-recaptcha-response')

        if not captcha:
            messages.error(request, 'reCAPTCHA verification token is missing', extra_tags='secondary')
            return render(request, 'index.html',)
        
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
            return redirect('homepage')
        except ValueError as e:
            messages.error(request, f'Error parsing reCAPTCHA response: {str(e)}', extra_tags='secondary')
            return redirect('homepage')

        if not response['success']:
            messages.error(request, 'reCAPTCHA verification failed. Please try again.', extra_tags='secondary')
            return redirect('homepage')

        if not (firstname and lastname and username and email and nationality and profile_picture and password1 and password2):
            messages.error(request, 'To get your Purse, Please fill all the form fields🙃.', extra_tags='secondary')
            return redirect('homepage')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Oops😥! Username is already taken. Do you want to Login instead?', extra_tags='secondary')
            return redirect('homepage')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Oops😥! Email is already in use. Do you want to Login instead?', extra_tags='secondary')
            return redirect('homepage')
        
        if password1 != password2:
            messages.error(request, 'Looks like there\'s a mismatch in your passwords.', extra_tags='secondary')
            return redirect('homepage')

        user = CustomUser.objects.create_user(username=username, email=email, password=password1, first_name=firstname, last_name=lastname)
        user.save()
        UserProfile.objects.create(user=user, Profile_image=profile_picture, Nationality=nationality)
        current_time = timezone.now()
        is_verified.objects.create(user=user, email=email, verification_code=verification_code, creation_time=current_time, verified=False)
        request.session['email'] = email

        subject = 'Please verify your email!'
        email_message = f'Hello {firstname} you just registered for a purse account with your Email address: {email}. please enter this code <h3><strong> {verification_code} </strong></h3> in the verification page to access your trading account.'
        from_email = 'alerts@myprofitpurse.com'
        recipient_list = [email]
        
        email_message = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
        email_message.content_subtype = 'html'
        email_message.send()

        subject = 'You have a new registered user!'
        email_message = f'A user named {firstname} Just registered on your website with the following details. Email address: {email}, Full name: {firstname} {lastname}, Nationality: {nationality}, & Username: {username}. To see or manipulate user\'s full details, log into your administrator account.'
        from_email = 'alerts@myprofitpurse.com' 
        recipient_list = ['support@myprofitpurse.com']
        email = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
        email.send()
        messages.success(request, 'Your account has been created successfully. Please check your email for verification.', extra_tags='secondary')
        
        return redirect('verify_email', )

    return redirect('homepage')

        


