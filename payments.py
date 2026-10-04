from fastapi import APIRouter, Request
import razorpay
import os

router = APIRouter(prefix="/api/payments")

razorpay_client = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET")))

@router.post("/create-order")
async def create_order(amount: int, user_id: str, request: Request):
    supabase = request.app.state.supabase
    
    # Razorpay paisa paise me leta hai (₹10 = 1000 paise)
    order_amount = amount * 100
    order_currency = "INR"
    
    order = razorpay_client.order.create(dict(amount=order_amount, currency=order_currency))
    
    # Order pending status me DB me save karo
    supabase.table('transactions').insert({
        "user_id": user_id,
        "amount": amount,
        "type": "CREDIT",
        "description": "Wallet Recharge",
        "razorpay_order_id": order['id'],
        "status": "PENDING"
    }).execute()
    
    return {"order_id": order['id'], "amount": order_amount}

@router.post("/webhook")
async def verify_payment(request: Request):
    # Yahan Razorpay webhook event bhejega success hone par
    payload = await request.json()
    supabase = request.app.state.supabase
    
    if payload['event'] == 'payment.captured':
        payment_entity = payload['payload']['payment']['entity']
        order_id = payment_entity['order_id']
        
        # DB update karna: Transaction Success + Wallet Balance Badhana
        txn = supabase.table('transactions').update({"status": "SUCCESS"}).eq("razorpay_order_id", order_id).execute()
        user_id = txn.data[0]['user_id']
        amount = txn.data[0]['amount']
        
        # (Actual app me yahan RPC function use karna chahiye atomicity ke liye)
        user = supabase.table('users').select('wallet_balance').eq('id', user_id).execute()
        new_balance = user.data[0]['wallet_balance'] + amount
        supabase.table('users').update({"wallet_balance": new_balance}).eq('id', user_id).execute()
        
    return {"status": "ok"}