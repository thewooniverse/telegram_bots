import os
from datetime import datetime
import json





filters = {
    # contains the filter configuration and settings to check against
    # these can be manually maintained, or stored as configurations for each channel

    "Joined_Date": datetime(2023, 4, 1), # must be before April, which is around when FT itself launched.
    "Tweets_Count": 50, # user must have more than this many tweets
    "Followers_Count": 5000, # user must have over this amount of followers
    "Wallet_Balance": 0.05 # user must have over this amount in balance
    # as JSON {"Joined_Date": "2023-04-01 00:00:00", "Tweets_Count": 50, "Follower_Count": 5000, "Wallet_Balance": 0.05}
}

watchlist = [
    # watchlist contains a list of Twitter handles
    # these can be manually maintained, or stored as configurations for each channel
    # when adding to watchlist, all user handle strings should be str.lower() to keep case sensitivity
    "icunucmi", "elonmusk"
]





def check_filter(profile_data):
    """
    check_filter(json_payload) - returns True or False depending on whether the given profile's metadata passes the configured filters.
    """
    # unpack the json into a python dictionary
    if not isinstance(profile_data, str):
        raise ValueError("Expected a string type for JSON input")
    try:
        profile_data_dict = json.loads(profile_data)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format provided")
    
    # parse each key,value pair in the profile_data_dict into its correct datatypes - for now, hardcode
    profile_data_dict['Tweets_Count'] = int(profile_data_dict['Tweets_Count'].replace(',',''))
    profile_data_dict['Followers_Count'] = int(profile_data_dict['Followers_Count'].replace(',',''))
    profile_data_dict['Wallet_Balance'] = float(profile_data_dict['Wallet_Balance'].split(" ")[0])
    profile_data_dict['Joined_Date'] = parse_str_date(profile_data_dict['Joined_Date'])

    # first, check for whether the username is in the watchlist
    if profile_data_dict['Username'] in watchlist:
        return True
    
    # check against various other flags
    flags_to_check = filters.keys()

    for flag in flags_to_check:
        if flag == "Joined_Date":
            if profile_data_dict['Joined_Date'] > filters['Joined_Date']: # if the joined date is after the cutoff date
                print(flag)
                return False
        elif profile_data_dict[flag] < filters[flag]:
            print(flag)
            return False
    
    # if all the flags have passed, return True
    return True


def parse_str_date(str_date):
    """
    parse_str_date(str_date): takes "Joined March 2023" month-yy into mm-yy datetime
    """    
    month, year = str_date.split(" ")[1], str_date.split(" ")[2]
    month_num = datetime.strptime(month, '%B').month
    return datetime(int(year), month_num, 1)





# run tests
if __name__ == "__main__":
    test_json = {
    "Username": "woonomics",
    "Joined_Date": "Joined January 2023",
    "Account_Age_Months": 0,
    "Tweets_Count": "500",
    "Following_Count": "6600",
    "Followers_Count": "16000",
    "Likes_Count": "17",
    "Wallet_Balance": "0.052788 ETH"}
    test_json = json.dumps(test_json)
    print(check_filter(test_json))

