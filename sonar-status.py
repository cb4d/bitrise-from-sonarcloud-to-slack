import sys
import json
import requests
from types import SimpleNamespace

projectKey = sys.argv[1]
sonarToken = sys.argv[2]
slackWebhookUrl = sys.argv[3]

url = 'https://sonarcloud.io/api/qualitygates/project_status'
query = {'projectKey': projectKey, 'branch': 'develop'}
r = requests.get(url, params=query, auth=(str(sonarToken), ''))

# throw if bad status
r.raise_for_status()

# json-to-object from https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
# if you want to see what's in the json just print(r.text)
projectStatus = json.loads(r.text, object_hook=lambda d: SimpleNamespace(**d)).projectStatus

failingConditions = list(filter(lambda x: x.status != 'OK', projectStatus.conditions))

slack_data = {
  'attachments' : [
    {
      'pretext' : 'Latest quality gate status for <https://sonarcloud.io/dashboard?id={}|{}>: {}'.format(projectKey, projectKey, projectStatus.status),
      'color' : 'warning',
      'fields' : list(map(lambda cond:
        {
          'title' : cond.metricKey,
          'value': '{} (threshold is {})'.format(cond.actualValue, cond.errorThreshold)
        },
      failingConditions))
    }
  ]
}

r = requests.post(slackWebhookUrl, data=json.dumps(slack_data))

# throw if bad status
r.raise_for_status()