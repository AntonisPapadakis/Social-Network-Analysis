import json
import time
from datetime import datetime

import click
import requests
import twitter


@click.command()
@click.argument('accounts', type=click.Path(exists=True))
@click.argument('credentials', type=click.Path(exists=True))
@click.option('--dest', default='', help='where the edges file will be stored')
def main(accounts, credentials, dest):
    """
    A tool that downloads the ids of followers of twitter accounts and stores them
    in a csv file in the form of graph edges. Provide 2 files:

    CREDENTIALS: JSON file with twitter API credentials ("consumer_key", "consumer_secret", "access_token_key", "access_token_secret")

    ACCOUNTS: txt file with the usernames of all the accounts whose followers you want to download. 
    Each username should be in a seperate line
    """

    api = auth(credentials)
    accounts_list = read(accounts)

    date = datetime.now()
    file_name = str(date.year) + date.strftime('%b') + '.edges'

    for account in accounts_list:
        followers = download(account, api)
        with open(dest+file_name, mode='a') as f:
            for follower in followers:
                f.write(f"{follower},{account}\n")
        print(account)

    print('All done')


def auth(credentials):
    with open(credentials, "r") as file:
        creds = json.load(file)
    api = twitter.Api(consumer_key=creds["consumer_key"],
                      consumer_secret=creds["consumer_secret"],
                      access_token_key=creds["access_token_key"],
                      access_token_secret=creds["access_token_secret"],
                      sleep_on_rate_limit=True)
    try:
        api.VerifyCredentials()
        return api
    except twitter.error.TwitterError as e:
        print('Authentication failed:', e)
        exit(-1)


def read(file):
    with open(file, mode='r') as f:
        accounts_list = [x for x in f.read().splitlines()]
    return accounts_list


def download(account, api):
    while True:
        try:
            followers = api.GetFollowerIDs(screen_name=account)
        except (requests.exceptions.ConnectionError):
            print(f'error occured at {account}')
            time.sleep(600)
        else:
            break
    return followers


if __name__ == '__main__':
    main()