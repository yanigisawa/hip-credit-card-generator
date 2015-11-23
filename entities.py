import re 
import json
from datetime import datetime

class HipChatUser(object):
    def __init__(self, id = None, name = None, created = None,
            email = None, group = None, is_deleted = None, is_group_admin = None,
            is_guest = None, last_active = None, links = None, mention_name = None,
            photo_url = None, presence = None, timezone = None, title = None, 
            version = None, xmpp_jid = None):
        self.id = id
        self.name = name

class HipChatFromUser(object):
    def __init__(self, from_user):
        self.id = from_user["id"]
        self.name = from_user["name"]

class HipChatMessage(object):
    def __init__(self, jsonDict):
        self.user_from = HipChatFromUser(jsonDict["from"])
        self.message = jsonDict['message'] 

class HipChatRoom(object):
    def __init__(self, roomDict):
        self.room_id = roomDict["id"]
        self.links = roomDict["links"]

class HipChatMessageItem(object):
    def __init__(self, message = None, room = None):
        self.message = HipChatMessage(message)
        self.room = HipChatRoom(room)

class HipChatRoomMessage(object):
    def __init__(self, event = None, item = None, oauth_client_id = None, webhook_id = None):
        self.event = event
        self.item = HipChatMessageItem(**item)
        self.oauth_client_id = oauth_client_id
        self.webhook_id = webhook_id



