from enum import Enum
import getpass

import requests
import eas
from objects.expansions import ArgExpansions
from objects.fields import ArgFields
from objects.resp_data import ResponseData
from objects.tweet import Tweet


base_url = "https://api.x.com/2"

class Client:
    def __init__(self, bearer_token: str):
        self.__bearer_token__ = bearer_token

    def __init__(self, file_path: str, password: str):
        token = eas.decrypt_from_file(file_path, bytes.fromhex(password))
        self.__bearer_token__ = token
        
    def __init__(self, file_path: str, input_password: bool):
        if input_password:
            password = getpass.getpass("Enter password: ")
        token = eas.decrypt_from_file(file_path, bytes.fromhex(password))
        self.__bearer_token__ = token
        
    def __headers__(self):
        return {
            "Authorization": f"Bearer {self.__bearer_token__}"
        }

    def get[D](self, path: str, ids: list[str] = None, fields: ArgFields = None, expansions: ArgExpansions = None, other_params: dict = None) -> ResponseData[D]:
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
        status_code = response.status_code
        if status_code == 200:
            return ResponseData[D].from_dict(response.json())
        elif status_code == 304:
            # Not Modified
            # There was no new data to return.
            return ResponseData[D](data=None, includes=None, meta=None, errors=None)  # No new data
        elif status_code == 400:
            raise ValueError(f"{status_code} - Bad Request - Invalid parameters")
        elif status_code == 401:
            raise ValueError(f"{status_code} - Unauthorized - Authentication failed") 
        elif status_code == 403:
            raise ValueError(f"{status_code} - Forbidden - Access not allowed")
        elif status_code == 404:
            raise ValueError(f"{status_code} - Not Found - Invalid URI or resource does not exist")
        elif status_code == 406:
            raise ValueError(f"{status_code} - Not Acceptable - Invalid format specified")
        elif status_code == 409:
            raise ValueError(f"{status_code} - Connection Exception - No rules defined for filtered stream")
        elif status_code == 410:
            raise ValueError(f"{status_code} - Gone - API endpoint has been turned off")
        elif status_code == 422:
            raise ValueError(f"{status_code} - Unprocessable Entity - Invalid data format")
        elif status_code == 429:
            raise ValueError(f"{status_code} - Too Many Requests - Rate limit exceeded")
        elif status_code == 500:
            raise ValueError(f"{status_code} - Internal Server Error")
        elif status_code == 502:
            raise ValueError(f"{status_code} - Bad Gateway - Twitter is down or being upgraded")
        elif status_code == 503:
            raise ValueError(f"{status_code} - Service Unavailable - Server overloaded")
        elif status_code == 504:
            raise ValueError(f"{status_code} - Gateway Timeout - Request timed out")
        else:
            raise ValueError(f"{status_code} - Unknown error occurred")
    
    def lookup_tweets(self, ids: list[str], fields: ArgFields=None, expansions: ArgExpansions=None) -> ResponseData[list[Tweet]]:
        return self.get("tweets", ids, fields, expansions)


if __name__ == "__main__":
    import os
    home_dir = os.path.expanduser("~")
    token_path = os.path.join(home_dir, "pyxdk_test",  "bearer_token.pvt")
    res = Client(token_path, True).lookup_tweets(
        ids=["1460323737035677698",
        "1519781379172495360",
        "1519781381693353984"],
    )
    print(res)