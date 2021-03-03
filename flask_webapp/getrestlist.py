#importing the required packages
import requests
import asyncio
import aiohttp
import json

#running thr first crawl to get the number of listed restaurants
def urllist(lat, long):
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
             'accept-encoding': 'gzip, deflate, br',
             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
             'accept-language': 'en-US,en;q=0.9',
             'if-none-match': 'W/"18a70-2svTzwERwbNJVGpuh7Z+/vbtj8U"'}
    #lat = 12.8933808
    #long = 77.6609237
    r1= requests.get('https://www.swiggy.com/dapi/restaurants/list/v5?lat=' + str(lat) + '&lng=' + str(long) + '&offset=0&sortBy=RELEVANCE&pageType=SEE_ALL&page_type=DESKTOP_SEE_ALL_LISTING', headers= headers)
    r1_js = r1.json()
    url_list=[]
    tot_rest_cnt = r1_js['data']['totalSize']
    for off in range(0, tot_rest_cnt, 14):
        url_list.append('https://www.swiggy.com/dapi/restaurants/list/v5?lat=' + str(lat) + '&lng=' + str(long) + '&offset=' + str(off) +'&sortBy=RELEVANCE&pageType=SEE_ALL&page_type=DESKTOP_SEE_ALL_LISTING')
    return url_list

# First async function for requesting to the site
async def request_to_site(session, url):
    async with session.get(url) as resp:
        x=await resp.json()
        return x

#Function for extracing the fields from the response json
def extract_fields(r1_js):
    tot_rest_cnt = r1_js['data']['totalSize']
    columns=['name', 'rest_id', 'city', 'area', 'rating', 'cuisine', 'cost_for_two', 'del_time', 'max_del_time', 'min_del_time', 
             'loc', 'disc_meta', 'disc_type', 'disc_op_type', 'fee', 'menu_link', 'slug']
    rn = len(r1_js['data']['cards'])
    for i in range(rn):
        cardType = r1_js['data']['cards'][i]['cardType']
        if cardType == 'restaurant':    
            name = r1_js['data']['cards'][i]['data']['data']['name']
            rest_id = r1_js['data']['cards'][i]['data']['data']['id']
            city = r1_js['data']['cards'][i]['data']['data']['city']
            area = r1_js['data']['cards'][i]['data']['data']['area']
            rating = r1_js['data']['cards'][i]['data']['data']['avgRating']
            cuisine = r1_js['data']['cards'][i]['data']['data']['cuisines']
            cost_for_two = r1_js['data']['cards'][i]['data']['data']['costForTwo']/100
            del_time = r1_js['data']['cards'][i]['data']['data']['deliveryTime']
            min_del_time = r1_js['data']['cards'][i]['data']['data']['minDeliveryTime']
            max_del_time = r1_js['data']['cards'][i]['data']['data']['maxDeliveryTime']
            loc = r1_js['data']['cards'][i]['data']['data']['locality']
            #discount attributes
            try:
                disc_meta = r1_js['data']['cards'][i]['data']['data']['aggregatedDiscountInfo']['shortDescriptionList'][0]['meta']
                disc_type = r1_js['data']['cards'][i]['data']['data']['aggregatedDiscountInfo']['shortDescriptionList'][0]['discountType']
                disc_op_type = r1_js['data']['cards'][i]['data']['data']['aggregatedDiscountInfo']['shortDescriptionList'][0]['operationType']
            except:
                disc_meta = '' 
                disc_type = ''
                disc_op_type = '' 

            #fee details
            fee = r1_js['data']['cards'][i]['data']['data']['feeDetails']['totalFees']/100
            try:
                menu_link = r1_js['data']['cards'][i]['data']['data']['cta']['link']
            except:
                menu_link = ''
            slug = r1_js['data']['cards'][i]['data']['data']['slugs']['restaurant']

            l2= [name, rest_id, city, area, rating, cuisine, cost_for_two, del_time, max_del_time, min_del_time, loc, disc_meta,
                   disc_type, disc_op_type, fee, menu_link, slug]
            if dict(zip(columns, l2)) not in rest_json:
                rest_json.append(dict(zip(columns, l2)))

#Second async function for running the crawls
async def run_crawls(session, url):
    try:
        js=await request_to_site(session,url)
        extract_fields(js)
    except Exception as err:
        #print(err)
        pass

    
#final code to run
async def getrest(lat, long):
    url_list = urllist(lat, long)
    global rest_json
    rest_json=[]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[run_crawls(session, url) for url in url_list])
    return json.dumps(rest_json)
