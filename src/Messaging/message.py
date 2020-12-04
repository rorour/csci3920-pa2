import json


class Message:

    next_id = 0

    def __init__(self, msg: str, sender_username: str, recipient_username: str):
        self.__msg = msg
        self.__sender = sender_username
        self.__recipient = recipient_username
        self.__msg_id = Message.next_id
        Message.next_id += 1

    @property
    def msg(self):
        return self.__msg

    @property
    def sender_username(self):
        return self.__sender

    @property
    def recipient(self):
        return self.__recipient

    @property
    def id(self):
        return self.__msg_id

    def __str__(self):
        return f'{self.sender_username}|{self.id}|{self.msg}'
