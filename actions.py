#
# Here are the definitions of actions to perform, where an events ocurrs
# Every function below, has three parameters, 'repo', 'branch', and 'payload'
#     repo: this is the name of the repository whom triggered the event
#     branch: this is the name of the branch related to event. It may be None
#     payload: the whole payload given by github
#
import settings
import requests

def push(repo, branch, payload):
    crumb = get_jenkins_crumb()
    job_request = requests.post(
        "%s/job/pep8/build" % settings.jenkins_URL,
        headers=crumb
    )
    print job_request.text

def pull_request(repo, branch, payload):
    print "pull request"

def get_jenkins_crumb():
    crumb_request = requests.get(
        "%s/crumbIssuer/api/xml" % settings.jenkins_URL,
        auth=requests.auth.HTTPBasicAuth(settings.jenkins_user, settings.jenkins_token),
        params={"xpath": 'concat(//crumbRequestField,":",//crumb)'}
    )
    try:
        response = crumb_request.json()
    except ValueError:
        print "Warning: couldn't decode crumb request."
        response = None
    return response
