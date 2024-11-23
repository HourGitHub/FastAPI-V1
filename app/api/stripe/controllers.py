# # app\api\stripe\controllers.py

import os
from app.utility.telegramAlert import send_telegram_message
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


def create_response(status: str, message: str, data: dict = None) -> dict:
    return {
        "status": status,
        "message": message,
        "data": data if data else {}
    }

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
            confirm=True,  # Don't confirm yet, let the client do it later
            return_url=os.getenv("RETURN_URL")
        )
        
        logging.debug(f"Payment Intent created: {payment_intent.id}")
        
        # Save the payment intent and status in the database (set status to 'pending' initially)
        stripe_payment = StripePayment(
            payment_intent_id=payment_intent.id,
            amount=amount,
            currency=currency,
            status="succeeded",  # Set the status to 'succeeded' initially
        )
        db.add(stripe_payment)
        db.commit()

        # Send success message to Telegram
        send_telegram_message(f"✅ Payment Intent created successfully: ID={payment_intent.id}, Amount={amount}, Currency={currency}")

        return payment_intent.client_secret, payment_intent.id

    except Exception as e:
        # Send failure message to Telegram on error
        send_telegram_message(f"❌ Error occurred while creating payment intent: {str(e)}")
        return create_response(status="error", message=f"Error: {str(e)}")




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

            send_telegram_message(f"✅ Payment confirmed successfully: ID={payment_intent.id}, Status={payment_intent_confirmed.status}")

        return payment_intent_confirmed.status, payment_intent_confirmed.id

    except StripeError as e:
        logging.error(f"Stripe error: {e.user_message}")
        send_telegram_message(f"❌ Stripe error occurred while confirming payment: {e.user_message}")
        return create_response(status="error", message=f"Stripe error: {e.user_message}")

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        send_telegram_message(f"❌ Unexpected error while confirming payment: {str(e)}")
        return create_response(status="error", message=f"Unexpected error: {str(e)}")



# app/api/stripe/controllers.py

def get_payment_status(payment_intent_id: str, db: Session):
    try:
        # Query the StripePayment table to get the status
        stripe_payment = db.query(StripePayment).filter(StripePayment.payment_intent_id == payment_intent_id).first()
        
        if stripe_payment:
            logging.debug(f"Payment Intent status from DB: {stripe_payment.status}")
            send_telegram_message(f"✅ Payment status retrieved: ID={payment_intent_id}, Status={stripe_payment.status}")
            return stripe_payment.status
        else:
            logging.error(f"Payment intent not found in database for ID: {payment_intent_id}")
            send_telegram_message(f"❌ Payment intent not found in database for ID={payment_intent_id}")
            raise StripeError("Payment intent not found in database.")

    except StripeError as e:
        logging.error(f"Error retrieving payment status: {e.user_message}")
        send_telegram_message(f"❌ Stripe error occurred while retrieving payment status: {e.user_message}")
        raise e
    
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        send_telegram_message(f"❌ Unexpected error while retrieving payment status: {str(e)}")
        return create_response(status="error", message=f"Unexpected error: {str(e)}")


def get_all_payments(db: Session):
    try:
        # Fetch all Stripe payment records from the database
        payments = db.query(StripePayment).all()
        if payments:
            send_telegram_message(f"✅ Retrieved all payments from the database: Total Payments={len(payments)}")
            return create_response(
                status="success", 
                message="All payments retrieved successfully", 
                data={"payments": [payment.to_dict() for payment in payments]}
            )
        else:
            send_telegram_message("❌ No payments found in the database.")
            return create_response(status="error", message="No payments found in database.")
    except Exception as e:
        logging.error(f"Error retrieving all payments: {str(e)}")
        send_telegram_message(f"❌ Unexpected error while retrieving all payments: {str(e)}")
        return create_response(status="error", message=f"Unexpected error: {str(e)}")