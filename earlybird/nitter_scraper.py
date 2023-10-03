import requests
from bs4 import BeautifulSoup
import time 


url = 'https://nitter.hyperreal.coffee/friendtech'

response = requests.get(url)
start_time = time.time()
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')    
    joined_element = soup.select_one('div.icon-container span.icon-calendar')
    if joined_element:
        joined_date = joined_element.find_next_sibling(string=True)
        if joined_date:
            print("Joined Date:", joined_date.strip())
        else:
            print("Joined date not found on the page.")
    else:
        print("Joined date not found on the page.")
    tweet_count_element = soup.select_one('ul li span.profile-stat-header:-soup-contains("Tweets") + span.profile-stat-num')
    if tweet_count_element:
        tweet_count = tweet_count_element.text.strip()
        print("Tweet Count:", tweet_count)
    else:
        print("Tweet count not found on the page.")

    tweet_count_element = soup.select_one('ul li span.profile-stat-header:-soup-contains("Following") + span.profile-stat-num')
    
    if tweet_count_element:
        tweet_count = tweet_count_element.text.strip()
        print("Following Count:", tweet_count)
    else:
        print("Following count not found on the page.")

    tweet_count_element = soup.select_one('ul li span.profile-stat-header:-soup-contains("Followers") + span.profile-stat-num')
    
    if tweet_count_element:
        tweet_count = tweet_count_element.text.strip()
        print("Followers Count:", tweet_count)
    else:
        print("Followers count not found on the page.")

    tweet_count_element = soup.select_one('ul li span.profile-stat-header:-soup-contains("Likes") + span.profile-stat-num')
    if tweet_count_element:
        tweet_count = tweet_count_element.text.strip()
        print("Likes Count:", tweet_count)
    else:
        print("Likes count not found on the page.")

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time} seconds")


