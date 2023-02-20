import pytest

import twitter_creds
import tweepy
import time

@pytest.mark.parametrize("test_msg, expected_result",
[
    ("Test message 1", True),
    ("Here is a short message which is reasonably short", True),
    ("Here is a medium message which is 100 characters long 0123456789 Here is a medium message which is 160 characters long 0123456789 ABC", True),
    ("Here is a medium message which is 100 characters long 0123456789 Here is a medium message which is 274 characters long 0123456789 ABC Here is a medium message which is 100 characters long 0123456789 Here is a medium message which is 100 characters", True),
]
)
def test_tweepy(test_msg, expected_result):
    """

    :param msg:
    :param expected_result:
    :return:
    """
    #print tweepy.__version__
    msg = "unittest test"

    auth = tweepy.OAuthHandler(twitter_creds.CONSUMER_KEY, twitter_creds.CONSUMER_SECRET)
    auth.set_access_token(twitter_creds.ACCESS_KEY, twitter_creds.ACCESS_SECRET)
    api = tweepy.API(auth)

    now = time.time()
    msg = time.asctime(time.localtime(now)) + " : " + test_msg.__str__()
    print(msg)
    print(len(msg))
    #api.update_status(sys.argv[1],lat="51.6",long="43.6")
    result = api.update_status(msg,lat="51.6",int="0.1")
    #api.update_status(sys.argv[1],lat=GLEBE_LAT,long=GLEBE_LONG)
    print()
    assert result.id is not None



