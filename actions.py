#
# Here are the definitions of actions to perform, where an events ocurrs
# Every function below, has three parameters, 'repo', 'branch', and 'payload'
#     repo: this is the name of the repository whom triggered the event
#     branch: this is the name of the branch related to event. It may be None
#     payload: the whole payload given by github
# 

def push(repo, branch, payload):
    print "push action"

def pull_request(repo, branch, payload):
    print "pull request"
