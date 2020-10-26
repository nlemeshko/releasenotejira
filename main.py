import requests
import urllib, json
import re

commit = list()
result = 'Miraworks Admin \nRelease note:\n\n'

def deldup(x):
  return list(dict.fromkeys(x))

def telegram_bot_sendtext(bot_message):

    bot_token = ''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

url = 'https://gitlab'

res = requests.get(url,headers={'PRIVATE-TOKEN': ''})
response=res.json()

merge=response[0]['iid']

url2 = ('/api/v4/projects/137/merge_requests/'+str(merge)+'/commits')

res = requests.get(url2,headers={'PRIVATE-TOKEN': ''})
response=res.json()
for i in range(len(response)):
 if 'MIRA' in response[i]['title']:
  for match in re.finditer('MIRA', response[i]['title']):
    if match.start()>0:
        commit.append(response[i]['title'][match.start():match.end()+5])
  commit.append(response[i]['title'][:9])

commit=deldup(commit)

for i in range(len(commit)):
 query = {
   'jql': 'project = MIRA AND issue = '+str(commit[i])
 }

 url3 = 'https:///rest/api/2/search'
 headers = {'Accept': 'application/json','Content-Type': 'application/json','Authorization': 'Basic '}
 res = requests.get(url3, headers=headers, params=query)
 commit[i]=commit[i] + ' ' + json.dumps(json.loads(res.text)['issues'][0]['fields']['summary'], ensure_ascii=False, sort_keys=True, indent=4, separators=(",", ": "))

for i in range(len(commit)):
    result=result+commit[i]+'\n'

telegram_bot_sendtext(result)