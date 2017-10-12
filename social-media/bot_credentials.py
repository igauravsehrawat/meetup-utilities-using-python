
__all__ = ["provide_key"]

def provide_key(key_name):
    all_keys = {
        "consumer_key": "your secret stuff",
        "consumer_secret": "your secret stuff",
        "access_token": "your secret stuff",
        "access_token_secret": "your secret stuffk"
    }
    try:
        return all_keys[key_name]
    except:
        print("Invalid key name")
