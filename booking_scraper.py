from playwright.sync_api import sync_playwright
import pandas as pd


def main():
    with sync_playwright() as p:
        checkin_date = '2024-05-10'
        checkout_date = '2024-05-11'

        page_url = f'https://www.booking.com/searchresults.html?ss=Gothenburg&ssne=Gothenburg&ssne_untouched=Gothenburg&sid=7e855e08f05774dc6779945105c32d02&aid=355028&lang=en-us&sb=1&src_elem=sb&src=index&dest_id=-2482986&dest_type=city&checkin={checkin_date}&checkout={checkout_date}&group_adults=2&no_rooms=1&group_children=0'

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)

        hotels = page.locator('//div[@data-testid="property-card"]').all()
        print(f'There are: {len(hotels)} hotels.')

        hotels_list = []
        for hotel in hotels: 
            hotel_dict = {}
            hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
            hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
            hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
            hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
            hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text()


            hotels_list.append(hotel_dict) 

        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list.xlsx', index=False)
        df.to_csv('hotels_list.csv', index=False)



        browser.close()



if __name__ == '__main__':
    main()