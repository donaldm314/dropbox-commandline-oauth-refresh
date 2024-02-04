#!/bin/env python3

import os
import sys
import logging
from dotenv import find_dotenv, load_dotenv, set_key
from pathlib import Path
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox.exceptions import ApiError

script_name = os.path.basename(sys.argv[0])
logger = logging.getLogger(script_name)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

DOTENV_FILE = find_dotenv()
if not os.path.isfile(DOTENV_FILE):
    logger.critical("Did not find a .env file!")
    sys.exit("No .env file found!")
DOTENV_PATH = Path(DOTENV_FILE)
os.chmod(DOTENV_PATH, 0o600)
load_dotenv(DOTENV_FILE)
APP_KEY = os.getenv("DROPBOX_APP_KEY")
APP_SECRET = os.getenv("DROPBOX_APP_SECRET")
REFRESH_TOKEN = os.getenv("DROPBOX_REFRESH_TOKEN")


def start_oauth_flow():
    # No refresh was available, so start the OAuth flow. We request
    # offline, so we will receive a refresh token.
    logger.info("Initiating OAuth flow.")
    flow = DropboxOAuth2FlowNoRedirect(
        APP_KEY,
        APP_SECRET,
        token_access_type="offline"
    )

    authorize_url = flow.start()
    instructions = """
1. Go to: {}
2. Click 'Allow' (you might have to log into Dropbox first).
3. Copy the authorization code.
"""
    print(instructions.format(authorize_url))

    auth_code = input("Enter the authorization code here: ")

    try:
        oauth_result = flow.finish(auth_code)
        # Update .env file with new tokens
        set_key(
            dotenv_path=DOTENV_PATH,
            key_to_set='DROPBOX_REFRESH_TOKEN',
            value_to_set=oauth_result.refresh_token
        )
        logger.info("Stored new refresh token")
        return oauth_result.refresh_token
    except dropbox.exceptions.AuthError as e:
        logger.critical(e)
        sys.exit("Authorization error!")


def get_refresh_token():
    if REFRESH_TOKEN:
        logger.info("We've received a refresh token in the past")
        dbx = dropbox.Dropbox(
            app_key=APP_KEY,
            app_secret=APP_SECRET,
            oauth2_refresh_token=REFRESH_TOKEN
        )
        try:
            dbx.users_get_current_account()

            logger.info("Using our existing refresh token")
            return REFRESH_TOKEN
        except dropbox.exceptions.AuthError as e:
            logger.critical(e)
            sys.exit("Authorization error!")

    return start_oauth_flow()


def main():
    refresh_token = get_refresh_token()
    with dropbox.Dropbox(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        oauth2_refresh_token=refresh_token
    ) as dbx:
        try:
            account = dbx.users_get_current_account()
            print(f"Dropbox display name: {account.name.display_name}")
        except ApiError as e:
            logger.critical(e)
            sys.exit("Dropbox API error!")


if __name__ == '__main__':
    main()
