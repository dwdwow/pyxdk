from enum import Enum
import getpass

import requests
import eas
from object.fields import Field
from object.tweet import Tweet


base_url = "https://api.x.com/2"

class Client:
    def __init__(self, bearer_token: str):
        self.__bearer_token__ = bearer_token

    def __init__(self, file_path: str, password: str):
        token = eas.decrypt_from_file(file_path, password.encode())
        self.__bearer_token__ = token
        
    def __init__(self, file_path: str, input_password: bool):
        if input_password:
            password = getpass.getpass("Enter password: ")
        token = eas.decrypt_from_file(file_path, password.encode())
        self.__bearer_token__ = token
        
    def __headers__(self):
        return {
            "Authorization": f"Bearer {self.__bearer_token__}"
        }

    def __get__(self, path: str, ids: list[str] = None, fields: dict[Field, list[Enum]] = None, expansions: list[Enum] = None, other_params: dict = None) -> any:
        url = f"{base_url}/{path.strip('/')}"
        queries: list[str] = []
        if ids:
            queries.append(f"ids={','.join(ids)}")
        if fields:
            for key, value in fields.items():
                if not value:
                    continue
                queries.append(f"{key.value}={','.join([v.value for v in value])}")
        if expansions:
            queries.append(f"expansions={','.join([e.value for e in expansions])}")
        if other_params:
            for key, value in other_params.items():
                if not value:
                    continue
                k: str = None
                if isinstance(key, Enum):
                    k = key.value
                else:
                    k = key
                if isinstance(value, list):
                    if isinstance(value[0], Enum):
                        queries.append(f"{k}={','.join([v.value for v in value])}")
                    else:
                        queries.append(f"{k}={','.join(value)}")
                else:
                    if isinstance(value, Enum):
                        queries.append(f"{k}={value.value}")
                    else:
                        queries.append(f"{k}={value}")
        url += "?" + "&".join(queries)
        response = requests.get(url, headers=self.__headers__())
        return response.json()
    
    def lookup_tweets(self, ids: list[str], fields: dict[Field, list[Enum]], expansions: list[Enum]) -> Tweet:
        return self.__get__("tweets", ids, fields, expansions)


if __name__ == "__main__":
    pass
