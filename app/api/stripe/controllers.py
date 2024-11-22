# # app\api\stripe\controllers.py

import os
from dotenv import load_dotenv
from requests import Session
import stripe
import logging
import stripe
from stripe.error import StripeError

from app.db.models.stripe import StripePayment

load_dotenv()

# Set your secret Stripe API key here
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Create Payment Intent and store it in the DB
def create_payment_intent(amount: int, currency: str, payment_method: str, db: Session):
    try:
        logging.debug(f"Received payment request: amount={amount}, currency={currency}, payment_method={payment_method}")
        
        # Create the PaymentIntent with Stripe
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            confirmation_method="manual",
            # confirm=False,  # Don't confirm yet, let the client do it later
            confirm=True, 
            return_url=os.getenv("RETURN_URL")
        )
        
        logging.debug(f"Payment Intent created: {payment_intent.id}")
        
        # Save the payment intent and status in the database (set status to 'pending' initially)
        stripe_payment = StripePayment(
            payment_intent_id=payment_intent.id,
            amount=amount,
            currency=currency,
            status="succeeded",  
        )
        db.add(stripe_payment)
        db.commit()

        return payment_intent.client_secret, payment_intent.id

    except StripeError as e:
        logging.error(f"Stripe error: {e.user_message}")
        raise e


# app/api/stripe/controllers.py

def confirm_payment(payment_intent_id: str, return_url: str, db: Session):
    try:
        # Retrieve the PaymentIntent from Stripe
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        # Confirm the payment intent
        payment_intent_confirmed = stripe.PaymentIntent.confirm(
            payment_intent.id,
            return_url=return_url  # For redirection-based payment methods
        )

        # Update the payment status in the database
        stripe_payment = db.query(StripePayment).filter(StripePayment.payment_intent_id == payment_intent.id).first()
        if stripe_payment:
            stripe_payment.status = payment_intent_confirmed.status  # Update status (e.g., succeeded, failed)
            db.commit()

        return payment_intent_confirmed.status, payment_intent_confirmed.id

    except StripeError as e:
        logging.error(f"Stripe error: {e.user_message}")
        raise e


# app/api/stripe/controllers.py

def get_payment_status(payment_intent_id: str, db: Session):
    try:
        # Query the StripePayment table to get the status
        stripe_payment = db.query(StripePayment).filter(StripePayment.payment_intent_id == payment_intent_id).first()
        
        if stripe_payment:
            logging.debug(f"Payment Intent status from DB: {stripe_payment.status}")
            return stripe_payment.status
        else:
            logging.error(f"Payment intent not found in database for ID: {payment_intent_id}")
            raise StripeError("Payment intent not found in database.")

    except StripeError as e:
        logging.error(f"Error retrieving payment status: {e.user_message}")
        raise e



def get_all_payments(db: Session):
    try:
        # Fetch all Stripe payment records from the database
        payments = db.query(StripePayment).all()
        return payments
    except Exception as e:
        logging.error(f"Error retrieving all payments: {str(e)}")
        raise e