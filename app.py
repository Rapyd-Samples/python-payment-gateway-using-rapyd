from flask import Flask, request, redirect
import utilities

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def app_home():
    # payment form submissions (payment-form name) in html below.
    if request.method == 'POST' and request.form['amount']:
        amount = int(request.form['amount'])
        body = {
            'amount': amount,
            'complete_checkout_url': 'http://example.com/complete',
            'country': 'US',
            'currency': 'USD',
            'cancel_checkout_url': 'http://example.com/cancel',
            'language': 'en',
        }

        try:
            # Generate checkout with this payment object
            req = utilities.make_request('post', '/v1/checkout', body)
            print('++++++ payment created +++++')
            print(req['data']['redirect_url'])
            print('++++++ payment created +++++')

            # Redirect to checkout.
            return redirect(req['data']['redirect_url'])

        except Exception as ex:
            print(ex)

    # Checkout html
    checkout_markup = "<div> <h1>Welcome to my Website!</h1> <hr>" \
                      "<h1> Checkout my upcoming event</h1> " \
                      "<section><h3>Consuming 3rd party apis (online)</h3> " \
                      "<p>Introduction to Postman Collections and api examples</p>" \
                      "<bold>$100</bold> <p></p>" \
                      "<form name=payment-form method=POST> " \
                      "<input type=hidden name=amount value=100>" \
                      " <input type=submit value=\"Reserve your slot \" name=submit>" \
                      "</form>" \
                      "</section><hr>" \
                      "</div>"
    return checkout_markup


@app.route('/rapyd-webhooks', methods=['POST'])
def rapyd_webhooks():
    print(request)

app.run(debug=True)
