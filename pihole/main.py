import requests
import time
import hashlib


class AuthRequired(Exception):
    pass


def requires_auth(api_func):
    """Decorator to check auth_data is present for given api method."""

    def wrapper(self, *args, **kwargs):
        if not self.auth_data:
            raise AuthRequired('Authentication is required!')
        return api_func(self, *args, **kwargs)

    return wrapper


class Auth(object):
    def __init__(self, password):
        # PiHole's web token is just a double sha256 hash of the utf8 encoded password
        self.token = hashlib.sha256(hashlib.sha256(str(password).encode()).hexdigest().encode()).hexdigest()
        self.auth_timestamp = time.time()


class PiHole(object):
    # Takes in an ip address of a pihole server
    def __init__(self, host, port = 80):
        self.host = host
        self.auth_data = None
        self.pw = None
        self.protocol = "http://"
        self.port = str(port)
        if self.port == "443":
            self.protocol = "https://"
        self.refresh()

    def inApiLink(self,ip, endpoint):
        return self.protocol+ str(ip) + ":"+self.port+"/admin/scripts/pi-hole/php/"+ str(endpoint) +".php"

    def refresh(self):
        rawdata = requests.get(self.protocol + self.host + ":"+self.port + "/admin/api.php?summary").json()
        # Debugging Purposes print(self.protocol + self.host + ":"+self.port + "/admin/api.php?summary")

        if self.auth_data:
            topdevicedata = requests.get(self.protocol + self.host + ":"+self.port + "/admin/api.php?getQuerySources=25&auth=" + self.auth_data.token).json()
            self.top_devices = topdevicedata["top_sources"]
            self.forward_destinations = requests.get(self.protocol + self.host + ":"+self.port + "/admin/api.php?getForwardDestinations&auth=" + self.auth_data.token).json()
            self.query_types = requests.get(self.protocol + self.host + ":"+self.port + "/admin/api.php?getQueryTypes&auth=" + self.auth_data.token).json()["querytypes"]

        # Data that is returned is now parsed into vars
        self.status = rawdata["status"]
        self.domain_count = rawdata["domains_being_blocked"]
        self.queries = rawdata["dns_queries_today"]
        self.blocked = rawdata["ads_blocked_today"]
        self.ads_percentage = rawdata["ads_percentage_today"]
        self.unique_domains = rawdata["unique_domains"]
        self.forwarded = rawdata["queries_forwarded"]
        self.cached = rawdata["queries_cached"]
        self.total_clients = rawdata["clients_ever_seen"]
        self.unique_clients = rawdata["unique_clients"]
        self.total_queries = rawdata["dns_queries_all_types"]
        self.gravity_last_updated = rawdata["gravity_last_updated"]

    @requires_auth
    def refreshTop(self, count):
        rawdata = requests.get(self.protocol + self.host + ":"+self.port + "/admin/api.php?topItems="+ str(count) +"&auth=" + self.auth_data.token).json()
        self.top_queries = rawdata["top_queries"]
        self.top_ads = rawdata["top_ads"]


    def getGraphData(self):
        rawdata = requests.get(self.protocol + self.host + ":"+self.port + "/admin/api.php?overTimeData10mins").json()
        return {"domains":rawdata["domains_over_time"], "ads":rawdata["ads_over_time"]}

    def authenticate(self, password):
        self.auth_data = Auth(password)
        self.pw = password
        # print(self.auth_data.token)

    @requires_auth
    def getAllQueries(self):
        if self.auth_data == None:
            print("Unable to get queries. Please authenticate")
            exit(1)
        return requests.get(self.protocol + self.host + ":"+self.port + "/admin/api.php?getAllQueries&auth=" + self.auth_data.token).json()["data"]

    @requires_auth
    def enable(self):
        requests.get(self.protocol + self.host + ":"+self.port + "/admin/api.php?enable&auth=" + self.auth_data.token)

    @requires_auth
    def disable(self, seconds):
        requests.get(self.protocol + self.host + ":"+self.port + "/admin/api.php?disable="+ str(seconds) +"&auth=" + self.auth_data.token)

    def getVersion(self):
        return requests.get(self.protocol + self.host + ":"+self.port + "/admin/api.php?versions").json()

    @requires_auth
    def getDBfilesize(self):
        return float(requests.get(self.protocol + self.host + ":"+self.port + "/admin/api_db.php?getDBfilesize&auth=" + self.auth_data.token).json()["filesize"])

    def getList(self, list):
        return requests.get(self.inApiLink(self.host, "get") + "?list="+str(list)).json()

    @requires_auth
    def add(self, list, domain):
        with requests.session() as s:
            s.get(self.protocol+ str(self.host) + ":"+self.port + "/admin/scripts/pi-hole/php/add.php")
            requests.post(self.protocol+ str(self.host) + ":"+self.port + "/admin/scripts/pi-hole/php/add.php", data={"list":list, "domain":domain, "pw":self.pw}).text

    @requires_auth
    def sub(self, list, domain):
        with requests.session() as s:
            s.get(self.protocol+ str(self.host) +":"+self.port+"/admin/scripts/pi-hole/php/sub.php")
            requests.post(self.protocol+ str(self.host) +":"+self.port+"/admin/scripts/pi-hole/php/sub.php", data={"list":list, "domain":domain, "pw":self.pw}).text
