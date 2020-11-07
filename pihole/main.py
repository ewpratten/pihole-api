import requests
import time
import hashlib
import datetime as dt
from dateutil.relativedelta import relativedelta
import dateutil.parser as date_parser
from enum import Enum


class QueryActionType(Enum):
    GRAVITY = 1
    FORWARDED = 2
    CACHE = 3
    BLOCKED_WILDCARD = 4
    UNKNOWN = 5


class AuthRequired(Exception):
    pass


class QueryException(Exception):
    pass


def requires_auth(api_func):
    """Decorator to check auth_data is present for given api method."""

    def wrapper(self, *args, **kwargs):
        if not self.auth_data:
            raise AuthRequired('Authentication is required!')
        return api_func(self, *args, **kwargs)

    return wrapper


def inApiLink(ip, endpoint):
    return "http://"+ str(ip) +"/admin/scripts/pi-hole/php/"+ str(endpoint) +".php"


class Auth(object):
    def __init__(self, password):
        # PiHole's web token is just a double sha256 hash of the utf8 encoded password
        self.token = hashlib.sha256(hashlib.sha256(str(password).encode()).hexdigest().encode()).hexdigest()
        self.auth_timestamp = time.time()


class PiHole(object):

    known_time_ranges = {
        "today": (dt.datetime.combine(dt.datetime.utcnow().date(), dt.datetime.min.time()), dt.datetime.utcnow()),
        "yesterday": (dt.datetime.combine(dt.datetime.utcnow().date()-dt.timedelta(days=1), dt.datetime.min.time()),
                      dt.datetime.combine(dt.datetime.utcnow().date()-dt.timedelta(days=1), dt.datetime.max.time())),
        "last_7_days": (dt.datetime.combine(dt.datetime.utcnow().date()-dt.timedelta(days=6), dt.datetime.min.time()),
                        dt.datetime.utcnow()),
        "last_30_days": (dt.datetime.combine(dt.datetime.utcnow().date()-dt.timedelta(days=29), dt.datetime.min.time()),
                         dt.datetime.utcnow()),
        "this_month": (dt.datetime.combine(dt.date(dt.datetime.utcnow().date().year,dt.datetime.utcnow().date().month,1),
                                           dt.datetime.min.time()),
                       dt.datetime.utcnow()),
        "last_month": [dt.datetime.combine(dt.date(dt.datetime.utcnow().date().year,dt.datetime.utcnow().date().month,1)-relativedelta(months=1),
                                           dt.datetime.min.time()),
                       dt.datetime.combine(dt.date(dt.datetime.utcnow().date().year,dt.datetime.utcnow().date().month,1)-dt.timedelta(days=1),
                                           dt.datetime.max.time())],
        "this_year": (dt.datetime.combine(dt.date(dt.datetime.utcnow().date().year,1,1), dt.datetime.min.time()),
                      dt.datetime.utcnow()),
        "all_time": (0, dt.datetime.utcnow())
    }

    # Takes in an ip address of a pihole server
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.auth_data = None
        self.refresh()
        self.pw = None

    def refresh(self):
        rawdata = requests.get("http://" + self.ip_address + "/admin/api.php?summary").json()

        if self.auth_data:
            topdevicedata = requests.get("http://" + self.ip_address + "/admin/api.php?getQuerySources=25&auth=" + self.auth_data.token).json()
            self.top_devices = topdevicedata["top_sources"]
            self.forward_destinations = requests.get("http://" + self.ip_address + "/admin/api.php?getForwardDestinations&auth=" + self.auth_data.token).json()
            self.query_types = requests.get("http://" + self.ip_address + "/admin/api.php?getQueryTypes&auth=" + self.auth_data.token).json()["querytypes"]

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
        rawdata = requests.get("http://" + self.ip_address + "/admin/api.php?topItems="+ str(count) +"&auth=" + self.auth_data.token).json()
        self.top_queries = rawdata["top_queries"]
        self.top_ads = rawdata["top_ads"]

    def getGraphData(self):
        rawdata = requests.get("http://" + self.ip_address + "/admin/api.php?overTimeData10mins").json()
        return {"domains":rawdata["domains_over_time"], "ads":rawdata["ads_over_time"]}

    def authenticate(self, password):
        self.auth_data = Auth(password)
        self.pw = password
        # print(self.auth_data.token)

    @requires_auth
    def getAllQueries(self, client=None, domain=None, date_from=None, date_to=None, return_type='raw'):
        """
        This function allows querying the pihole DB. It can take client, domain or dates.
        dates can come in one of the following formats:
            ISO formatted string
            an instance of datetime
            one of the shorthand strings listed above under 'known_time_ranges'

        The return type can be either returned as is (default) or formatted (return_type=array_dict) in order to make
        using the data easier
        """
        if self.auth_data == None:
            print("Unable to get queries. Please authenticate")
            exit(1)

        url = "http://" + self.ip_address + "/admin/api_db.php?getAllQueries&auth=" + self.auth_data.token

        if client and domain:
            print("Cannot search for both client AND domain")
            exit(1)

        start = None
        until = None
        if isinstance(date_from, str):
            try:
                start = date_parser.isoparse(date_from)
            except Exception:
                if date_from in self.known_time_ranges and date_to is None:
                    start, until = self.known_time_ranges[date_from]
        elif isinstance(date_from, dt.datetime):
            start = date_from

        if isinstance(date_to, str):
            try:
                until = date_parser.isoparse(date_to)
            except Exception:
                pass
        elif isinstance(date_from, dt.datetime):
            until = date_to

        if start is not None:
            url +="&from=" + str(start.timestamp())

        if until is not None:
            url +="&until=" + str(until.timestamp())

        if client:
            url += "&client=" + client

        if domain:
            url += "&domain=" + domain

        result = requests.get(url).json()
        if 'data' not in result:
            raise QueryException("Empty results returned: something is wrong with your query")

        if return_type == 'array_dict':
            data = [{
                'datetime': dt.datetime.fromtimestamp(item[0]),
                'type': item[1],
                'requested_domain': item[2],
                'client': item[3],
                'status': QueryActionType(item[4])
            } for item in result['data']]
        else:
            data = result['data']

        return data

    @requires_auth
    def enable(self):
        requests.get("http://" + self.ip_address + "/admin/api.php?enable&auth=" + self.auth_data.token)

    @requires_auth
    def disable(self, seconds):
        requests.get("http://" + self.ip_address + "/admin/api.php?disable="+ str(seconds) +"&auth=" + self.auth_data.token)

    def getVersion(self):
        return requests.get("http://" + self.ip_address + "/admin/api.php?versions").json()

    @requires_auth
    def getDBfilesize(self):
        return float(requests.get("http://" + self.ip_address + "/admin/api_db.php?getDBfilesize&auth=" + self.auth_data.token).json()["filesize"])

    def getList(self, list):
        return requests.get(
            "http://" + str(self.ip_address) + "/admin/api.php?list=" + list).json()

    @requires_auth
    def add(self, list, domain):
        requests.get(
            "http://" + str(self.ip_address) + "/admin/api.php?list=" + list + "&add=" + domain + "&auth=" +
            self.auth_data.token)

    @requires_auth
    def sub(self, list, domain):
        with requests.session() as s:
            s.get("http://"+ str(self.ip_address) +"/admin/scripts/pi-hole/php/sub.php")
            requests.post("http://"+ str(self.ip_address) +"/admin/scripts/pi-hole/php/sub.php", data={"list":list, "domain":domain, "pw":self.pw}).text
