import platform
import socket
import os
import json

MGO_PATH = os.path.expanduser("~") + '/Mari/mGo'
ASSETS_PATH = MGO_PATH + '/Assets'
APP_CONFIG = MGO_PATH + '/mgo_config.txt'


class MgoUtils(object):
    def __init__(self):
        """
        It would be useful to have a class of methods/utilities which could be shared between Mari and other
        applications. For eg. networking code, or code for reading/writing files, shouldn't need to be doubled up
        between Maya and Mari.

        For now, I've included this module in both the Mari examples folder, as well as the Maya scripts folder. We can
        sort this out later on
        """

        print "mgo utils: ver.1"

    # if mgo_config.txt not found, a new config file is initialised here
    def init_app_config(self):
        print "initialising mgo config..."
        data = {'mari hosts': {}, '_current host': {}, 'mari projects': {}, '_current project': {}, 'assets paths': {}}
        data['mari hosts']['localhost'] = '127.0.0.1'

        self.json_write(data, APP_CONFIG)

    # retrives the config data for the application UI
    def get_config(self):
        if not os.path.exists(APP_CONFIG):
            self.init_app_config()

        data = self.json_read(APP_CONFIG)
        return data

    # convenience functions for reading/writing json files
    def json_write(self, data, path):
        base_path = path.rsplit('/', 1)[0]
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        with open(path, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
        return path

    def json_read(self, path):
        if os.path.isfile(path):
            with open(path, 'r') as infile:
                data = json.load(infile)
            return data

    # function to open/close port 6010 for an specific network address
    def get_ip_list(self):
        import platform
        ip_list = []
        wired_ip = '127.0.0.1'

        def get_ip():
            _ip = '127.0.0.1'
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # doesn't even have to be reachable
                s.connect(('10.255.255.255', 0))
                _ip = s.getsockname()[0]
                s.close()
                return _ip
            except:
                pass

        # Machines could have multiple IPs - Wifi, Wired etc... (Prioritize WIRED)
        platform = str(platform.system())

        if platform == "Windows":
            try:
                wired_ip = str(socket.gethostbyname(socket.gethostname()))
            except:
                wired_ip = get_ip()

            ip_list = [wired_ip, get_ip()]

        else:
            # Linux Only
            try:
                co = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)
                # read the ifconfig file
                ifconfig = co.stdout.read()

                i = 0
                _ips = []
                # look for the IP number that comes right after the inet string.
                ifconfig_spaceless = ifconfig.split(" ")
                for ifconfig_strings in ifconfig_spaceless:
                    if ifconfig_strings == "inet":
                        if ifconfig_spaceless[i + 1] != "127.0.0.1":
                            _ips.append(ifconfig_spaceless[i + 1])
                    i += 1

                wired_ip = ext_ip = get_ip()
                for _ip in _ips:
                    if _ip != ext_ip:
                        wired_ip = _ip
            except:
                wired_ip = get_ip()
            ip_list = [wired_ip, get_ip()]

        return ip_list


