# Forex Investment Broker PWA

## Overview
This is a Progressive Web App (PWA) for a Forex investment broker. It allows users to track Forex investments and manage their portfolios. The frontend is built with HTML, CSS, and JavaScript, while the backend is powered by Django.

## Features
- User authentication and authorization
- Portfolio management
- Real-time Forex data integration
- Responsive design for mobile and desktop

## Technologies Used
- Frontend:
  - HTML
  - CSS
  - JavaScript

- Backend:
  - Django
  - Django REST Framework

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/demigodhitr/django.git
   cd progressive


## Install Dependencies
1. pip install -r requirements.txt

## Run migrations
- python manage.py migrate
1.  if failed, check db config in #settings.py, then
-   python manage.py makemigrations
-   python manage.py migrate

## Start the development server
- python manage.py runserver
- access the application through the url on your command prompt / terminal.
  ## OR
  - python manage.py runserver 0.0.0.0:port (example python manage.py runserver 0.0.0.0:8080) to bind development to public network
    and make it discoverable by other device/machines on the same network.
  - for example, you can connect your smartphone device and computer to the same network and and access the deveopment server using your
    smartphone through the address =  ip_address:port
    # replace ip_address with your computer ip address. run the command ipconfig in a command prompt to confirm your computer's IP.
    # replace port with the actual port number used. 8080 in this case or any port used when starting the server.
    - example 192.168.0.231:8080
    - you typically enter the address in your browser url search bar.

  
## Email and API Configuration

This application requires email functionality for certain features, such as user registration, password reset, and notifications. It also utilizes the Google reCAPTCHA service for form submissions, the IP stack API for geolocation features, and the CoinGecko API for fetching cryptocurrency data. Before running the application, you'll need to configure the email backend, Google reCAPTCHA key, IP stack API key, and CoinGecko API key in the Django settings.

### Email Configuration

To configure the email backend:

1. Open the `settings.py` file in your Django project.
2. Locate the email settings section.
3. Replace the placeholder values with your SMTP server settings or use a third-party email service provider.
4. Save the changes and restart the Django server.

For more information on configuring the email backend, refer to the [Django documentation](https://docs.djangoproject.com/en/stable/topics/email/).

### Google reCAPTCHA Configuration

To configure the Google reCAPTCHA key:

1. Obtain a reCAPTCHA site key and secret key from the [reCAPTCHA admin console](https://www.google.com/recaptcha/admin).
2. Open the relevant HTML template files where the reCAPTCHA widget is used (e.g., user registration, contact form).
3. Replace the placeholder values with your reCAPTCHA site key.

For more information on integrating reCAPTCHA with your Django application, refer to the [reCAPTCHA documentation](https://developers.google.com/recaptcha/intro).

### IP stack API Configuration

To configure the IP stack API key:

1. Sign up for an account on [IP stack](https://ipstack.com/) to obtain an API key.
2. Open the relevant Django settings file where the IP stack API key is used.
3. Replace the placeholder value with your IP stack API key.

For more information on using the IP stack API, refer to the [IP stack documentation](https://ipstack.com/documentation).

### CoinGecko API Configuration

To configure the CoinGecko API key:

1. Sign up for an account on [CoinGecko](https://www.coingecko.com/) to obtain an API key.
2. Open the relevant Django settings file where the CoinGecko API key is used.
3. Replace the placeholder value with your CoinGecko API key.

For more information on using the CoinGecko API, refer to the [CoinGecko API documentation](https://www.coingecko.com/api/documentation).

### Google Analytics Tags

If you wish to track website traffic using Google Analytics, replace the Google Analytics tags (`<script>` tags with your tracking ID) on each template, placed immediately after `<head>` opening tag  with your own Google Analytics tags. You can obtain your tracking ID from the Google Analytics admin console.



## THIS PROJECT IS LICENSED UNDER THE MIT LICENSE, THIS MEANS THAT YOU CAN READ, WRITE, MODIFY AS DESIRED.

FEEL FREE TO MODIFY IT TO SUIT YOUR PROJECTS'S SPECIFIC NEEDS AND ADD ANY ADDITIONAL INFORMATION
YOU THINK WOULD BE HELPFUL FOR USERS. 
