from amadeus import Client, ResponseError
import concurrent.futures
import time
from config import API_KEY, API_SECRET

def get_amadeus_client():
    return Client(client_id=API_KEY, client_secret=API_SECRET)

def search_cheapest_dates(client, origin, destination, departure_range, retries=1):
    for attempt in range(retries + 1):
        try:
            return client.shopping.flight_dates.get(
                origin=origin, destination=destination, departureDate=departure_range
            )
        except ResponseError as error:
            if attempt < retries:
                time.sleep(2)  # リトライ前に待機
                continue
            raise error

def search_flight_offers(client, origin, destination, departure_date, return_date=None,
                         travel_class='ECONOMY', airline='JL', adults=1):
    params = {
        'originLocationCode': origin,
        'destinationLocationCode': destination,
        'departureDate': departure_date,
        'adults': adults,
        'includedAirlineCodes': airline,
        'travelClass': travel_class,
        'currencyCode': 'USD',
        'max': 50
    }
    if return_date:
        params['returnDate'] = return_date
    try:
        time.sleep(1)  # レートリミット回避
        return client.shopping.flight_offers_search.get(**params)
    except ResponseError as error:
        raise error

def parallel_search_offers(client, origin, destinations, classes, departure_date,
                           return_date=None, adults=1):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for dest in destinations:
            for cls in classes:
                futures.append(
                    executor.submit(
                        search_flight_offers, client, origin, dest, departure_date,
                        return_date, cls, 'JL', adults
                    )
                )
        for future in concurrent.futures.as_completed(futures):
            try:
                offers = future.result()
                if offers:
                    results.extend(offers.data)
            except Exception as e:
                print(f"Error in parallel search: {e}")
    return results
