# Integrating Rapyd payments checkout in python.
Rapyd payment integration in a python application.

### What you need to start
* Rapyd Account (https://dashboard.rapyd.net/sign-up)
* Python (and pip) installed on your dev environment.
* Extras: to be able to register Webhooks with Rapyd and receive webhook event requests,
you will also be required to install [ngrok](https://ngrok.com/) and expose the port the python app is running on eg `ngrok http 5000`
then register the ngrok url to receive the request from Rapyd.

### Initial setup (Rapyd dashboard)
* Log in to your Rapyd account
* Make sure you are using the panel in "sandbox" mode (switch in the top right part of the panel)
* Go to the "Developers" tab. You will find your API keys there. Copy them and update the values in the utilities.py
* Go to the "Webhooks" tab and enter the URL where the application listens for events. By default it is "https://{YOUR_BASE_URL}/rapyd-webhooks" and mark which events should be reported to your app
* Proceed to the next steps to run the app in your dev environment.


### Getting started with testing the app:
* From within this apps folder, run `pip install -r requirements.txt` to install the dependencies (Flask) the app relies on.
* Then `python app.py` or `python3 app.py` to start the app @ `http://127.0.0.1:5000/`
* From this url, you can access the apps home page which contains the payment form, that when submitted, initiates the payment
workflow.

### Get support:
* [https://community.rapyd.net](https://community.rapyd.net)
* [https://support.rapyd.net](https://support.rapyd.net)
