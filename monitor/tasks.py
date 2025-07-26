from celery import shared_task
from amadeus import Client, ResponseError
from datetime import date, timedelta
from .models import Route, PriceHistory
import os

# Initialize the Amadeus client using environment variables
client = Client(
    client_id=os.getenv('AMADEUS_CLIENT_ID'),
    client_secret=os.getenv('AMADEUS_CLIENT_SECRET')
)

@shared_task
def monitor_prices():
    """Check flight prices and store the lowest result."""
    routes = Route.objects.all()
    for route in routes:
        try:
            response = client.shopping.flight_offers_search.get(
                originLocationCode=route.origin,
                destinationLocationCode=route.destination,
                airlineCodes=route.airline,
                departureDate=(date.today() + timedelta(days=30)).strftime('%Y-%m-%d'),
                adults=1,
                currencyCode='JPY'
            )
            data = response.data
            if data:
                prices = [float(offer['price']['total']) for offer in data]
                min_price = min(prices)
            else:
                min_price = None
        except ResponseError as error:
            # Print the error and continue with the next route
            print(error)
            continue

        if min_price is not None:
            PriceHistory.objects.create(route=route, price=min_price)
