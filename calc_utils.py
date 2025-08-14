KM_TO_MILE = 0.621371

def calculate_miles(offer):
    total_km = sum(seg['distance'] for itin in offer['itineraries'] for seg in itin['segments'])
    return total_km * KM_TO_MILE

def calculate_lsp(miles):
    return miles / 400  # 400マイル = 1 LSP

def calculate_lsp_unit_price(price, lsp):
    return price / lsp if lsp > 0 else float('inf')

def is_international(offer):
    # 簡易フィルタ: origin国 != destination国 (改善: Airport Search APIで正確国コード取得)
    origin_code = offer['itineraries'][0]['segments'][0]['departure']['iataCode']
    dest_code = offer['itineraries'][0]['segments'][-1]['arrival']['iataCode']
    # 仮: 国コードとして先頭2文字使用 (例: TYO=JP, NYC=US) – 不正確、実際は別API推奨
    return origin_code[:2] != dest_code[:2]
