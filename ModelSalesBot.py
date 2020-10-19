import requests
from typing import List, Union

def model_sales(cookie_list: List[str], model_id: int):
    r = requests.get(f'http://api.roblox.com/Marketplace/ProductInfo?assetId={model_id}')
    
    c =             1
    product_data =  None
    xcsrf =         None
    product_id =    None
    product_price = None

    print(r.json())
    print(r.headers)

    if r.status_code == 200:
        product_data = r.json()
        xcsrf = r.headers['x-csrf-token']
        product_id = product_data['ProductId']
        product_price = product_data['PriceInRobux']

    for cookie in cookie_list:
        
        url = f"https://economy.roblox.com/v1/purchases/products/{product_id}"

        r = requests.post(
            url=url,
            data={
                "expectedCurrency": 1,
                "expectedPrice": product_price,
                "expectedSellerId": 1
            },
            cookies={
                ".ROBLOSECURITY": cookie
            },
            headers={
                "X-CSRF-TOKEN": xcsrf,
                "Content-type": 'application/json; charset=utf-8'
            }
        )

        if r.status_code != 200:
            print(r.json())
            print(r.headers)
            print(r.status_code)
            return None

        print(f"Cookie {c} bought asset {model_id} successfully")
        c += 1
    
    print(f"{c}/{len(cookie_list)} cookies bought the model successfully")