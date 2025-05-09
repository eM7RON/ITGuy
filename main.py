import os
import requests
import time

BOT_TOKEN       = os.environ["BOT_TOKEN"]
SIGNING_SECRET  = os.environ["SIGNING_SECRET"]
WORKSPACE_ID    = os.environ["workspace_id"]
CHANNEL_ID      = os.environ["channel_id"]

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
     
def conv_members(channel_id, cursor='', limit=100, paginate='members'):
    return req('https://slack.com/api/conversations.members', query={
        'channel': channel_id, 'cursor': cursor, 'limit': limit}, paginate=paginate)

def conv_history(channel_id, cursor='', limit=100, paginate='messages'):
    return req('https://slack.com/api/conversations.history', query={
        'channel': channel_id, 'cursor': cursor, 'limit': limit}, paginate=paginate)

def conv_replies(channel_id, timestamp, cursor='', limit=100, paginate='messages'):
    "Retrieve a thread of messages posted to a conversation"
    return req('https://slack.com/api/conversations.replies', 'get', query={
        'channel': channel_id, 'ts': timestamp, 'cursor': cursor, 'limit': limit}, paginate=paginate)

def chat_post_message(channel_id, query={}):
    req('https://slack.com/api/chat.postMessage', query={**query, 'channel': channel_id})

def chat_me_message(channel_id, text=''):
    req('https://slack.com/api/chat.meMessage', query={'channel': channel_id, 'text': text})

def chat_post_ephemeral(channel_id, user_id, query={}):
    req('https://slack.com/api/chat.postEphemeral', query={**query, 'channel': channel_id, 'user': user_id})

def chat_delete(channel_id, timestamp, query={}):
    req('https://slack.com/api/chat.delete', query={**query, 'channel': channel_id, 'ts': timestamp})

def chat_get_permalink(channel_id, timestamp, query={}):
    return req('https://slack.com/api/chat.getPermalink', query={**query, 'channel': channel_id, 'message_ts': timestamp}).json()

def chat_update(channel_id, timestamp, query={}):
    return req('https://slack.com/api/chat.update', query={**query, 'channel': channel_id, 'ts': timestamp})

def users_info(user_id, query={}, method='get'):
    return req('https://slack.com/api/users.info', query={**query, 'user': user_id}, method=method)