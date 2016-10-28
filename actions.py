#
# Here are the definitions of actions to perform, where an events ocurrs
# Every function below, has three parameters, 'repo', 'branch', and 'payload'
#     repo: this is the name of the repository whom triggered the event
#     branch: this is the name of the branch related to event. It may be None
#     payload: the whole payload given by github
#
import settings
import jenkins

_server = jenkins.Jenkins(
    settings.jenkins_URL,
    username=settings.jenkins_user,
    password=settings.jenkins_token
)


def push(repo, branch, payload):
    if branch == "master" or branch == "develop":
        _server.build_job("pep8", {"branch": branch})
    else:
        print "Ignoring push event for branch: '%s'" % branch


def pull_request(repo, branch, payload):
    try:
        action = payload["action"]
        issue_url = payload["pull_request"]["issue_url"]
    except KeyError:
        print "Can't parse payload."
        return None
    if action in ["opened", "synchronize"]:
        print "Pull request action: '%s'." % action
        _server.build_job("pep8", {
            "branch": branch,
            "issue_url": issue_url
        })
    else:
        print "Ignoring pull request action: '%s'" % action
