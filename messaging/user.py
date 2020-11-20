class User:
    def __init__(self, username: str, password: str, display_name: str, phone_number: str):
        self.__username = username
        self.__password = password
        self.__display_name = display_name
        self.__phone_number = phone_number

    @property
    def username(self):
        return self.__username

    @property
    def display_name(self):
        return self.__display_name

    @property
    def phone_number(self):
        return self.__phone_number

    @property
    def password(self):
        return self.__password
