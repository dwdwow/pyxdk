import getpass
import eas


class Client:
    def __init__(self, bearer_token: str):
        self.__bearer_token = bearer_token

    def __init__(self, file_path: str, password: str):
        token = eas.decrypt_from_file(file_path, password.encode())
        self.__bearer_token = token
        
    def __init__(self, file_path: str, input_password: bool):
        if input_password:
            password = getpass.getpass("Enter password: ")
        token = eas.decrypt_from_file(file_path, password.encode())
        self.__bearer_token = token
