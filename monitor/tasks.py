from celery import shared_task
from amadeus import Client, ResponseError
from datetime import date, timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Route, PriceHistory
import os


def send_alert(route, price):
    """Send an email alert for an error fare."""
    message = f"Error fare for {route}: {price}"
    from_email = settings.EMAIL_HOST_USER or "noreply@example.com"
    recipient = [route.user.email] if route.user.email else []
    if recipient:
        send_mail("Error Fare Detected", message, from_email, recipient)
    else:
        print("No email for user, skipping alert.")


@shared_task
def monitor_prices():
    """Monitor flight prices for all routes and save the lowest price to history."""
    amadeus = Client(
        client_id=os.getenv('AMADEUS_CLIENT_ID'),
        client_secret=os.getenv('AMADEUS_CLIENT_SECRET')
    )

    routes = Route.objects.all()
    for route in routes:
        try:
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=route.origin,
                destinationLocationCode=route.destination,
                airlineCodes=route.airline,
                departureDate=(date.today() + timedelta(days=30)).strftime('%Y-%m-%d'),
                adults=1,
                currencyCode='JPY'
            )
            offers = response.data
            if offers:
                prices = [float(offer['price']['total']) for offer in offers]
                min_price = min(prices)
            else:
                min_price = None
        except ResponseError as error:
            print(f"Amadeus API error for route {route}: {error}")
            continue  # 次ルートへ

        if min_price is not None:
            PriceHistory.objects.create(route=route, price=min_price)
            if min_price <= route.baseline_price * route.threshold:
                print("Error fare detected")
                send_alert(route, min_price)
