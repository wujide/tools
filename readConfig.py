import os
import codecs
import configparser

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")


class ReadConfig:
    def __init__(self):
        with open(configPath) as fd:
            data = fd.read()
            #  remove BOM
            if data[:3] == codecs.BOM_UTF8:
                data = data[3:]
                with codecs.open(configPath, "w") as file:
                    file.write(data)
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)

    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    def get_redis(self, name):
        value = self.cf.get("REDIS", name)
        return value


if __name__ == '__main__':
    rf = ReadConfig()
    ci = rf.get_headers('clientid')
    print(ci)
    rf.set_headers('clientid', str(int(ci) + 100))
    cii = rf.get_headers('clientid')
    print(cii)
