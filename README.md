# Dropbox command-line OAuth with refresh in Python

Python Dropbox command-line example using OAuth with a refresh token.

[Dropbox SDK examples](https://github.com/dropbox/dropbox-sdk-python/tree/main/example/oauth) show how to handle the start of the OAuth flow, prompting the user to click a URL and authorize the app.

I was not able to find examples using the refresh token.

Steps:

1. go to the [Dropbox App Console](https://www.dropbox.com/developers/apps/).
2. click 'create an app'
3. choose a scoped access API
4. choose the type of access you need: app folder or full dropbox
5. name your app

This results in two secrets:

- an app key
- an app secret

Store those in a .env file. Because they are secret, **do not add them to git**, keep them **read-write only for the user**.
