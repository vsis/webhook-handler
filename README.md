# GitHub WebHook Handler

This is a flask-based webserver, that performs defines "actions" when it recieves GitHub Webhooks.

## What's a webhook

It is a POST HTTP request, sended by Github, when some events happen.
Read more here: https://developer.github.com/webhooks/

## Requirements

You need some python packages before to run.

```
pip install -r requirements.txt
```

## Setup

You need to take some steps before run webhook-hander.

### Edit settings

Edit `settings.py`, and modify these variables acording to your jenkins setup.

```
jenkins_URL = ""
jenkins_user = ""
jenkins_token = ""
```

Then set a secret for your github repository. Read more here: https://developer.github.com/webhooks/securing/
You should set `Payload URL` to `${your_server}/github`, and Content Type to `application/json`

The same secret should be set in `setting.py`:

```
secret = ""
check_signature = True
```

I *strongly* recomend to set `check_signature` to `True`. Set it to `False` only for testing/develptment purposes.

### Setup actions

Now edit `actions.py`. You will find two functions: `push` and `pull_request`. You can set what things Webhook-Handler will do.
Also, you can define more GitHub events. But, you need to declare them in `defined_actions` variable at `webhook-handler.py`.

### Execute it

Then, you can run: `python webhook-handler.py -h 0.0.0.0`.
