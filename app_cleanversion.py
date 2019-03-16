import requests
import json
import re
import sys
from loguru import logger


def get_token(user,pwd): 
    """
    Get Full Access Token with Username and Password
    """
    return json.loads(requests.get("https://api.facebook.com/restserver.php?api_key=3e7c78e35a76a9299309885393b02d97&email={0}&format=JSON&generate_machine_id=1&generate_session_cookies=1&locale=en_US&method=auth.login&password={1}&return_ssl_resources=0&v=1.0&sig=0a51bddba3a4152ab92ec4b8cdf8a730".format(user, pwd)).text)['access_token']

def get_friends_list(token): 
    """
    Get all friendlist and return json files that has name and id of your friends
    """
    return json.loads(requests.get('https://graph.facebook.com/me?fields=friends&access_token='+token).text)['friends']['data']

def get_last_active(friendid,token): 
    """
    return last created status (in year)
    """
    return json.loads(requests.get('https://graph.facebook.com/%s/feed?access_token=%s&limit=1'%(friendid,token)).text)['data'][0]

def unfriend(friendid,token): 
    """
    Unfriending friend by ID
    """
    return requests.delete('https://graph.facebook.com/me/friends?uid={0}&access_token={1}'.format(friendid,token)).text


if __name__ == "__main__":
    # Get Token
    token = get_token(input('Masukan Username Facebook: '),input('Masukan Password Facebook: '))
    minyear = int(input('Minimum Year: '))

    # Set Initial Amount for Tracking
    num,unfriended = 1,0

    # Iterate for each friend
    for account in get_friends_list(token):
        try:
            # Get Last Active
            last = get_last_active(account['id'],token)['created_time'].split('-')[0]
            logger.info('[%s][%s] Last Update: %s'%(num,account['name'],last))

            # If Last Active below Min year
            if int(last) < minyear:
                # Unfriend the friend
                # If it return true
                if unfriend(account['id'],token) == "true":
                    logger.success('[%s] Unfriended'%(account['name']))
                    unfriended += 1
            num += 1
        except:
            continue
    logger.success('%s unfriended'%(unfriended))