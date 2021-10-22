from flask import Flask, render_template, request, redirect
import stripe
import sys
from decimal import Decimal

from stripe.api_resources import application_fee, payment_intent, transfer

stripe.api_key = "sk_test_51Jd5nnFr0Kn8j0AETLdTIDgTCt0thXU4b4ZsDMl6aXApNzbA0zjOcAtumLbsyeA2L3jYfGPnToFJTl1pCmIjHh4d00nkCNADzh"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/partners/signup", methods=['GET'])
def partners_signup():
    return render_template('seller_signup.html')

@app.route("/onboarding", methods=['POST'])
def onboard_start():
    # Generate signup URL;
    country=request.form.get('country')
    email=request.form.get('email')
    entity_type=request.form.get('entity_type')
    account = stripe.Account.create(
        type='express',
        country=country,
        email=email,
        business_type=entity_type
    )
    # Create account link and redirect user
    account_link = stripe.AccountLink.create(
        account=account.id,
        type='account_onboarding',
        refresh_url='http://localhost:5000/onboarding/failed',
        return_url='http://localhost:5000/onboarding/complete'
    )
    return redirect(account_link.url, code=302)

@app.route("/onboarding/complete")
def onboard_complete():
    return "<p>onboard completed</p>"

@app.route("/onboarding/failed")
def onboard_failed():
    return "<p>onboard failed!</p>"


# Customer flows
# Customer login
# Customer logout
# Add to cart
# Checkout
@app.route("/create-checkout-session", methods=['POST'])
def create_checkout_session():
    fee=Decimal(request.form.get('fees')) * 100
    account_id=request.form.get('account_id')
    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                'price':'price_1JdqcKFr0Kn8j0AEEhV1RaD0',
                'quantity':'1'
            }
        ],
        payment_method_types = [
            'card'
        ],
        mode='payment',
        success_url = 'http://localhost:5000/payment_success',
        cancel_url = 'http://localhost:5000/payment_cancel',
        payment_intent_data = {
            "application_fee_amount": fee,
            "description": "RWT Penfold Grange",
            "transfer_data": {
                "destination": account_id
            }
        }
    )
    return redirect(checkout_session.url, code=303)

@app.route('/payment_success')
def payment_success():
    return "Payment Success!"

@app.route('/payment_cancel')
def payment_cancel():
    return "Payment Cancelled!"

# @app.route("/checkout")
# def checkout