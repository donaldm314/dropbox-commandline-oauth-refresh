# Dropbox command-line OAuth with refresh in Python

Python Dropbox command-line example using OAuth with a refresh token.

[Dropbox SDK examples](https://github.com/dropbox/dropbox-sdk-python/tree/main/example/oauth) show how to handle the start of the OAuth flow, prompting the user to click a URL and authorize the app.

I was not able to find examples using the refresh token.

## Setup:

1. go to the [Dropbox App Console](https://www.dropbox.com/developers/apps/).
2. click 'create an app'
3. choose a scoped access API
4. choose the type of access you need: app folder or full dropbox
5. name your app

This results in two secrets:

- an app key
- an app secret

Store those in a .env file. Because they are secret, **do not add them to git**, keep them **read-write only for the user**.

## Running the example:

1. the first time you run the script, it will prompt you to seek an authorization code:

   > ./oauth2-with-refresh.py
   > oauth2-with-refresh.py - INFO - Initiating OAuth flow.
   >
   > 1. Go to: https://www.dropbox.com/oauth2/authorize?response_type=code&client_id=SOME_ID&token_access_type=offline
   > 2. Click 'Allow' (you might have to log into Dropbox first).
   > 3. Copy the authorization code.
   >
   > Enter the authorization code here:

2. After pasting the authorization code, the script connects to Dropbox and reads the display name of the account:

   > oauth2-with-refresh.py - INFO - Stored new refresh token
   >
   > Dropbox display name: Don Murray

3. The refresh token is now stored in .env, and can be used without re-authorizing:

   > ./oauth2-with-refresh.py
   >
   > oauth2-with-refresh.py - INFO - We've received a refresh token in the past
   >
   > oauth2-with-refresh.py - INFO - Using our existing refresh token
   >
   > Dropbox display name: Don Murray
