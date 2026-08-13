import requests
from django.conf import settings


ZARINPAL_REQUEST_URL = (
    "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
)

VERIFY_URL = (
    "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
)


def create_payment(amount, description, callback_url):

    data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": amount,
        "description": description,
        "callback_url": callback_url,
        "currency": "IRT",
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    response = requests.post(
        ZARINPAL_REQUEST_URL,
        json=data,
        headers=headers,
    )

    result = response.json()

    if (
        "data" in result
        and result["data"].get("code") == 100
    ):
        authority = result["data"]["authority"]

        return {
            "success": True,
            "url": (
                "https://sandbox.zarinpal.com/pg/StartPay/"
                f"{authority}"
            ),
            "authority": authority,
        }

    return {
        "success": False,
        "message": result,
    }


def verify_payment(amount, authority):

    data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": amount,
        "authority": authority,
        "currency": "IRT",
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    response = requests.post(
        VERIFY_URL,
        json=data,
        headers=headers,
    )

    return response.json()
