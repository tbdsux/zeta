import base64
import json

# base64 data hasher and decoder
class Hasher:
    @staticmethod
    def hash(dict_data):
        # convert dict to string and hash to base64
        data = base64.b64encode(str(dict_data).encode("ascii"))
        encoded = data.decode("ascii")

        return encoded

    @staticmethod
    def decode(hashed_dict):
        # convert hashed to string dict
        string_data = base64.b64decode(hashed_dict.encode("ascii"))
        decoded = string_data.decode("ascii")

        # convert string dict to dict
        return json.loads(decoded.replace("'", '"'))
