from celery import shared_task
from amadeus import Client, ResponseError
from datetime import date, timedelta
from .models import Route, PriceHistory
import os

# Amadeus クライアントを環境変数から初期化
amadeus = Client(
    client_id=os.getenv("AMADEUS_CLIENT_ID"),
    client_secret=os.getenv("AMADEUS_CLIENT_SECRET"),
)

@shared_task
def monitor_prices():
    """各ルートの最安価格を取得して保存するタスク"""
    routes = Route.objects.all()
    for route in routes:
        try:
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=route.origin,
                destinationLocationCode=route.destination,
                airlineCodes=route.airline,
                departureDate=(date.today() + timedelta(days=30)).strftime("%Y-%m-%d"),
                adults=1,
                currencyCode="JPY",
            )
            offers = response.data or []
            prices = [float(o["price"]["total"]) for o in offers]
            if prices:
                min_price = min(prices)
                PriceHistory.objects.create(route=route, price=min_price)
        except ResponseError as error:
            # エラー発生時は次のルートへ
            print(error)
            continue
