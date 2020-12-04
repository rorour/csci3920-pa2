class User:
    def __init__(self, username: str, password: str, display_name: str):
        self.__username = username
        self.__password = password
        self.__display_name = display_name

    @property
    def username(self):
        return self.__username

    @property
    def display_name(self):
        return self.__display_name

    @property
    def password(self):
        return self.__password

    def __str__(self):
        return f'{self.username}|{self.display_name}'
