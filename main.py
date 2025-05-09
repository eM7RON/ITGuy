import os
import requests
import time

BOT_TOKEN       = os.environ["BOT_TOKEN"]
SIGNING_SECRET  = os.environ["SIGNING_SECRET"]
WORKSPACE_ID    = os.environ["WORKSPACE_ID"]
CHANNEL_ID      = os.environ["CHANNEL_ID"]

def http_helper(url, method='post', query={}, body=''):
    headers = {"Authorization": f"Bearer {bot_token}"}
    return getattr(requests, method.lower())(url, headers=headers, params=query, data=body)

def paginate_helper(url, method='post', query={}, body='', paginate='', items=[]):
    response = http_helper(url, method, query, body)
    response_json = response.json()
    items.extend(response_json.get(paginate, []))
    if 'response_metadata' in response_json \
    and 'next_cursor' in response_json['response_metadata'] \
    and response_json['response_metadata']['next_cursor']:
        query['cursor'] = response_json['response_metadata']['next_cursor']
        time.sleep(1)
        items = paginate_helper(url, method, query, body, paginate, items)
    return items

def req(url, method='get', query={}, body='', paginate=''):
    if paginate:
        return paginate_helper(url, method, query, body, paginate)
    else:
        return http_helper(url, method, query, body).json()

def authping():
    "Check if the bot token is valid"
    return req('https://slack.com/api/auth.test')['ok']
     
def conv_members(CHANNEL_ID, cursor='', limit=100, paginate='members'):
    return req('https://slack.com/api/conversations.members', query={
        'channel': CHANNEL_ID, 'cursor': cursor, 'limit': limit}, paginate=paginate)

def conv_history(CHANNEL_ID, cursor='', limit=100, paginate='messages'):
    return req('https://slack.com/api/conversations.history', query={
        'channel': CHANNEL_ID, 'cursor': cursor, 'limit': limit}, paginate=paginate)

def conv_replies(CHANNEL_ID, timestamp, cursor='', limit=100, paginate='messages'):
    "Retrieve a thread of messages posted to a conversation"
    return req('https://slack.com/api/conversations.replies', 'get', query={
        'channel': CHANNEL_ID, 'ts': timestamp, 'cursor': cursor, 'limit': limit}, paginate=paginate)

def chat_post_message(CHANNEL_ID, query={}):
    req('https://slack.com/api/chat.postMessage', query={**query, 'channel': CHANNEL_ID})

def chat_me_message(CHANNEL_ID, text=''):
    req('https://slack.com/api/chat.meMessage', query={'channel': CHANNEL_ID, 'text': text})

def chat_post_ephemeral(CHANNEL_ID, user_id, query={}):
    req('https://slack.com/api/chat.postEphemeral', query={**query, 'channel': CHANNEL_ID, 'user': user_id})

def chat_delete(CHANNEL_ID, timestamp, query={}):
    req('https://slack.com/api/chat.delete', query={**query, 'channel': CHANNEL_ID, 'ts': timestamp})

def chat_get_permalink(CHANNEL_ID, timestamp, query={}):
    return req('https://slack.com/api/chat.getPermalink', query={**query, 'channel': CHANNEL_ID, 'message_ts': timestamp}).json()

def chat_update(CHANNEL_ID, timestamp, query={}):
    return req('https://slack.com/api/chat.update', query={**query, 'channel': CHANNEL_ID, 'ts': timestamp})

def users_info(user_id, query={}, method='get'):
    return req('https://slack.com/api/users.info', query={**query, 'user': user_id}, method=method)