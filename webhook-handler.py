
import hmac
from json import loads, dumps
from flask import Flask, request, abort
from hashlib import sha1


application = Flask(__name__)


@application.route('/github', methods=['POST'])
def handle_web_hook():
    
    # Only SHA1 is supported
    header_signature = request.headers.get('X-Hub-Signature')
    if header_signature is None:
        abort(403)
                                                                  
    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        abort(501)
                                                                  
    # HMAC requires the key to be bytes, but data is string
    secret = "JB7Cb5XB+luPPDwvaL68lQ=="
    mac = hmac.new(str(secret), msg=request.data, digestmod=sha1)

    if not str(mac.hexdigest()) == str(signature):
        abort(403)

    # Handle ping event
    event = request.headers.get('X-GitHub-Event', 'ping')
    if event == 'ping':
        return dumps({'msg': 'pong'})

    # Gather data
    try:
        payload = loads(request.data)
    except ValueError:
        abort(400)

    try:
        # Case 1: a ref_type indicates the type of ref.
        # This true for create and delete events.
        if 'ref_type' in payload:
            if payload['ref_type'] == 'branch':
                branch = payload['ref']
        # Case 2: a pull_request object is involved. This is pull_request and
        # pull_request_review_comment events.
        elif 'pull_request' in payload:
            # This is the TARGET branch for the pull-request, not the source
            # branch
            branch = payload['pull_request']['base']['ref']
        elif event in ['push']:
            # Push events provide a full Git ref in 'ref' and not a 'ref_type'.
            branch = payload['ref'].split('/')[2]
    except KeyError:
        # If the payload structure isn't what we expect, we'll live without
        # the branch name
        branch = None

    # All current events have a repository, but some legacy events do not,
    # so let's be safe
    try:
        name = payload['repository']['name']
    except KeyError:
        name = None

    print "some random string"
    return dumps(payload, indent=4)

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
