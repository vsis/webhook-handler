import settings
import actions
import hmac
from json import loads, dumps, dump
from flask import Flask, request, abort
from hashlib import sha1


application = Flask(__name__)


@application.route('/github', methods=['POST'])
def handle_web_hook():
    # Only SHA1 is supported
    header_signature = request.headers.get('X-Hub-Signature')
    if header_signature is None:
        print "No github signature found!"
        abort(403)
    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        abort(501)
    # HMAC requires the key to be bytes, but data is string
    mac = hmac.new(str(settings.secret), msg=request.data, digestmod=sha1)
    if not str(mac.hexdigest()) == str(signature):
        print "Invalid github signature"
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
    # Get repository name and branch
    name, branch = get_branch_parameters(payload, event)
    # Dump payload, if necessary
    if settings.dump_payload:
	write_payload(payload)
    # Make a response. It is not really important
    response = {
        "name": name,
        "branch": branch,
        "event": event,
    }
    return dumps(response)

# Given a payload and an event, it returns a tuple with repository name and branch
def get_branch_parameters(payload, event):
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
        else:
            branch = None
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
    return (name,branch)

# It will write a payload in a file.
# The file path is given in settings.dump_payload_file
def write_payload(payload):
    with open(settings.dump_payload_file, 'a') as json_file:
        dump(payload, json_file, indent=2)

# Perform an action, according to event type
def execute_action(event, name, branch, payload):
    defined_actions = {
        "push": actions.push,
        "pull_request": actions.pull_request,
    }
    try:
        action = defined_actions[event]
    except KeyError:
        print "Action for '%s' event is not defined" % event
        abort(501)
    action(name, branch, payload)

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
