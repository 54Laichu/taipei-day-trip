from fastapi import APIRouter, Body, Header, HTTPException
from fastapi.responses import JSONResponse
from models.User import UserAuth
from models.Order import Order
from models.Payment import Payment
from typing import Annotated
import requests
import os

router = APIRouter()

@router.post("/orders")
async def create(auth_header: Annotated[str, Header(alias="Authorization")], order_info: Annotated[dict, Body(...)]):
    try:
        user = UserAuth.check_jwt(auth_header)
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "Unauthorized User"})

        user_id = user['id']
        order = Order(**order_info['order'])
        order.user_id = user_id

        [order_id, order_number] = Order.create(order)
        if not order_id:
            return JSONResponse(status_code=400, content={"error": True, "message": "訂單建立失敗，請洽客服人員"})

        #POST TapPay
        tappay_data = {
            "prime": order_info['prime'],
            "partner_key": os.getenv('TAPPAY_PARTNER_KEY'),
            "merchant_id": os.getenv('TAPPAY_MERCHANT_ID'),
            "amount": order.price,
            "currency": "TWD",
            "details": f"Trip to {order.trip.attraction.name}",
            "cardholder": {
                "phone_number": order.contact.phone,
                "name": order.contact.name,
                "email": order.contact.email,
            },
            "order_number": order_number,
            "remember": True
        }

        tappay_url = os.getenv('TAPPAY_API_URL')
        headers = {
            "Content-Type": "application/json",
            "x-api-key": os.getenv('TAPPAY_PARTNER_KEY')
        }
        response = requests.post(tappay_url, json=tappay_data, headers=headers)
        tappay_result = response.json()


        #Create Payment
        payment = Payment(
            order_id=order_id,
            status=tappay_result['status'],
            transaction_time_millis=tappay_result['transaction_time_millis'],
            msg=tappay_result['msg'],
            amount=tappay_result['amount'],
            currency=tappay_result['currency'],
            rec_trade_id=tappay_result['rec_trade_id'],
            bank_transaction_id=tappay_result['bank_transaction_id'],
            last_four=int(tappay_result['card_info']['last_four'])
        )
        print(tappay_result)
        Payment.create(payment)

        if tappay_result['status'] == 0:
            Order.update_status(order_id, 'paid')
            return JSONResponse(status_code=200, content={
                "data": {
                    "number": tappay_result['order_number'],
                    "payment": {
                        "status": 0,
                        "message": "付款成功"
                    }
                }
            })
        else:
            return JSONResponse(status_code=400, content={
                "data": {
                    "number": tappay_result['order_number'],
                    "payment": {
                        "status": tappay_result['status'],
                        "message": "付款失敗"
                    }
                }
            })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})
