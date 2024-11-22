import os
from typing import List
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from app.db import get_db 
from app.db.models.stripe import StripePayment
from app.schemas.utility import PaymentListItem, PaymentRequest, PaymentStatusResponse
from app.api.stripe.controllers import create_payment_intent, get_payment_status
import logging

load_dotenv()

base_url = os.getenv("BASE_URL", "BASE_URL")


stripe = APIRouter()

@stripe.post("/create-payment-intent")
async def create_payment_intent_route(request: PaymentRequest, db: Session = Depends(get_db)):
    try:
        # Call the controller to create the payment intent and store it in the DB
        client_secret, payment_intent_id = create_payment_intent(
            amount=request.amount,
            currency=request.currency,
            payment_method=request.payment_method,
            db=db
        )
        return {"client_secret": client_secret, "payment_intent_id": payment_intent_id}
    except Exception as e:
        logging.error(f"Error creating payment intent: {str(e)}")
        raise HTTPException(status_code=400, detail="Error creating payment intent")


@stripe.get("/payment/confirmation")
async def payment_confirmation(request: Request, db: Session = Depends(get_db)):
    # Extract payment intent ID from the query parameters (Stripe appends this to the URL)
    payment_intent_id = request.query_params.get('payment_intent')
    
    # Retrieve payment intent from Stripe to check status
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        if payment_intent.status == 'succeeded':
            # Handle successful payment
            return {"message": "Payment successful!"}
        else:
            # Handle failed or pending payment
            return {"message": "Payment failed or pending."}
    except stripe.error.StripeError as e:
        # Handle error
        return {"error": f"Payment error: {e.user_message}"}


@stripe.get("/payment-status/{payment_intent_id}", response_model=PaymentStatusResponse)
async def payment_status_route(payment_intent_id: str, db: Session = Depends(get_db)):
    try:
        # Call the controller to retrieve the payment status from the DB
        status = get_payment_status(payment_intent_id, db)
        return {"status": status}
    except Exception as e:
        logging.error(f"Error retrieving payment status: {str(e)}")
        raise HTTPException(status_code=400, detail="Error retrieving payment status")


@stripe.get("/all-payments", response_model=List[PaymentListItem])
async def get_all_payments(db: Session = Depends(get_db)):
    try:
        # Query all payments from the database
        stripe_payments = db.query(StripePayment).all()

        if not stripe_payments:
            raise HTTPException(status_code=404, detail="No payments found")

        # Convert the list of payments into a response that includes `created_at_iso` as a string
        return [
            {
                "payment_intent_id": payment.payment_intent_id,
                "status": payment.status,
                "amount": payment.amount,
                "currency": payment.currency,
                "created_at": payment.created_at_iso,  # Use the ISO formatted string
            }
            for payment in stripe_payments
        ]

    except Exception as e:
        logging.error(f"Error retrieving all payments: {str(e)}")
        raise HTTPException(status_code=400, detail="Error retrieving payments")
