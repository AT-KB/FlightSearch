import streamlit as st
import pandas as pd
from api_utils import get_amadeus_client, search_cheapest_dates, parallel_search_offers
from calc_utils import calculate_miles, calculate_lsp, calculate_lsp_unit_price, is_international

st.title("JAL国際線 LSP検索ツール")

origin = st.text_input("出発地 (例: NRT)", "NRT")
destinations_str = st.text_input("到着地 (カンマ区切り, 例: JFK,LHR,SYD)", "JFK")
destinations = [d.strip() for d in destinations_str.split(",") if d.strip()]
departure_range = st.text_input("出発日範囲 (例: 2025-09-01,2025-09-30)", "2025-09-01,2025-09-30")
return_date = st.text_input("帰り日 (往復の場合、例: 2025-10-01。片道は空欄)", "")
classes = st.multiselect("クラス (複数選択可)", ["ECONOMY", "PREMIUM_ECONOMY", "BUSINESS", "FIRST"], default=["ECONOMY"])
min_unit_price = st.number_input("最小LSP単価閾値 (これ未満のみ表示、0で全て)", min_value=0.0, value=0.0)

if st.button("検索開始"):
    client = get_amadeus_client()
    results = []

    dep_dates = {}
    for dest in destinations:
        cheapest = search_cheapest_dates(client, origin, dest, departure_range)
        if cheapest and cheapest.data:
            dep_dates[dest] = cheapest.data[0]['departureDate']

    for dest in destinations:
        dep_date = dep_dates.get(dest)
        if dep_date:
            offers_data = parallel_search_offers(client, origin, [dest], classes, dep_date, return_date if return_date else None)
            for offer in offers_data:
                if is_international(offer):
                    miles = calculate_miles(offer)
                    lsp = calculate_lsp(miles)
                    price = float(offer['price']['total'])
                    unit_price = calculate_lsp_unit_price(price, lsp)
                    if min_unit_price == 0.0 or unit_price <= min_unit_price:
                        results.append({
                            '出発地': origin,
                            '到着地': dest,
                            '日付': dep_date,
                            'クラス': offer.get('travelerPricings', [{}])[0].get('fareDetailsBySegment', [{}])[0].get('classOfService', '不明'),
                            'マイル': round(miles, 1),
                            'LSP': round(lsp, 2),
                            '値段 (USD)': price,
                            'LSP単価': round(unit_price, 2)
                        })

    if results:
        df = pd.DataFrame(results)
        df = df.sort_values(by='LSP単価')
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="CSVダウンロード", data=csv, file_name="jal_lsp_results.csv", mime='text/csv')
    else:
        st.warning("結果なし。条件を調整してください。")
