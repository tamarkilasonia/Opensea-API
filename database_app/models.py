from .base_model import Model

class Collection(Model):
    collection: str
    name: str
    description: str
    image_url: str
    owner: str
    twitter_username: str
    contracts: dict

# to test things
class Cars(Model):
    name: str
    description: str