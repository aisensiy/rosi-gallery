import json


class Config(object):
    def __init__(self, path="config.json"):
        data = json.loads(file(path, 'r').read())
        for k, v in data.items():
            self.__dict__[k] = v

if __name__ == '__main__':
    c = Config()
    print c.base_dir
