[![PyPI version](https://badge.fury.io/py/PiHole-api.svg)](https://badge.fury.io/py/PiHole-api)
# PiHole-api
A python3 wrapper for the pihole api that aims to eventually be a full replacement for the [AdminLTE](https://github.com/pi-hole/AdminLTE) web panel

## Installing
To install the package from pip, first run:
```bash
python3 -m pip install --no-cache-dir PiHole-api
```

Due to naming issues, inside python, the package is named `pihole` **not** `PiHole-api`. Keeping this in mind, let's import it.
```python3
import pihole as ph
```

## Usage
This library has many features that can be broken down in to two simple sections. Stats, and Controls. In order to use any of the functions, you must first import the library, then create a PiHole object.

```python3
# Import the library
import pihole as ph

# Create an object
pihole = ph.PiHole("<ip address of server>")
```
Throuought this README, I will assume that you are using the name `pihole` for your object

### Stats
Checking the current version data can be done using:
```python3
pihole.getVersion()
```
It will return a json object that will look like:
```json
{'core_update': False, 'web_update': False, 'FTL_update': False, 'core_current': 'v4.0', 'web_current': 'v4.0', 'FTL_current': 'v4.0', 'core_latest': 'v4.0', 'web_latest': 'v4.0', 'FTL_latest': 'v4.0', 'core_branch': 'master', 'web_branch': 'master', 'FTL_branch': ''}
```

To refresh all stat-related data:
```python3
pihole.refresh()
```

To access the fetched data, use these self-descriptive variables:
```python3
pihole.status
pihole.domain_count
pihole.queries
pihole.blocked
pihole.ads_percentage
pihole.unique_domains
pihole.forwarded
pihole.cached
pihole.total_clients
pihole.unique_clients
pihole.total_queries
```

If you have already [authenticated](#Controls), the `refresh()` function will also return data about the top devices, forward destinations, and query types. These can be accessed using:
```python3
# Top devices
pihole.top_devices

# Forward destinations
pihole.forward_destinations

# Query types
pihole.query_types
```

To get data about the last gravity update, use:
```python3
pihole.gravity_last_updated
```

It will return a json object that looks like:
```json
{'file_exists': True, 'absolute': 1534793121, 'relative': {'days': '0', 'hours': '00', 'minutes': '42'}}
```

You can also get the graph data using:
```python3
pihole.getGraphData()
```

The data it returns looks like this:
```json
{'domains': {'1534712100': 3, '1534712700': 87, '1534713300': 41, '1534713900': 45, '1534714500': 1, '1534715100': 28, '1534715700': 26, '1534716300': 0, '1534716900': 0, '1534717500': 0, '1534718100': 0, '1534718700': 0, '1534719300': 0, '1534719900': 0, '1534720500': 0, '1534721100': 0, '1534721700': 0, '1534722300': 0, '1534722900': 22, '1534723500': 5, '1534724100': 6, '1534724700': 2, '1534725300': 0, '1534725900': 3, '1534726500': 15, '1534727100': 1, '1534727700': 0, '1534728300': 0, '1534728900': 10, '1534729500': 8, '1534730100': 5, '1534730700': 0, '1534731300': 0, '1534731900': 0, '1534732500': 0, '1534733100': 0, '1534733700': 0, '1534734300': 0, '1534734900': 0, '1534735500': 0, '1534736100': 0, '1534736700': 0, '1534737300': 0, '1534737900': 0, '1534738500': 0, '1534739100': 0, '1534739700': 0, '1534740300': 0, '1534740900': 0, '1534741500': 0, '1534742100': 0, '1534742700': 0, '1534743300': 0, '1534743900': 0, '1534744500': 0, '1534745100': 0, '1534745700': 0, '1534746300': 0, '1534746900': 0, '1534747500': 0, '1534748100': 0, '1534748700': 0, '1534749300': 0, '1534749900': 0, '1534750500': 0, '1534751100': 0, '1534751700': 0, '1534752300': 0, '1534752900': 0, '1534753500': 0, '1534754100': 0, '1534754700': 0, '1534755300': 0, '1534755900': 0, '1534756500': 0, '1534757100': 0, '1534757700': 0, '1534758300': 0, '1534758900': 0, '1534759500': 0, '1534760100': 0, '1534760700': 0, '1534761300': 0, '1534761900': 0, '1534762500': 0, '1534763100': 0, '1534763700': 0, '1534764300': 0, '1534764900': 0, '1534765500': 0, '1534766100': 0, '1534766700': 0, '1534767300': 0, '1534767900': 0, '1534768500': 0, '1534769100': 0, '1534769700': 0, '1534770300': 0, '1534770900': 0, '1534771500': 0, '1534772100': 0, '1534772700': 0, '1534773300': 0, '1534773900': 0, '1534774500': 0, '1534775100': 0, '1534775700': 71, '1534776300': 61, '1534776900': 53, '1534777500': 27, '1534778100': 101, '1534778700': 118, '1534779300': 24, '1534779900': 6, '1534780500': 7, '1534781100': 37, '1534781700': 106, '1534782300': 142, '1534782900': 54, '1534783500': 79, '1534784100': 90, '1534784700': 71, '1534785300': 77, '1534785900': 90, '1534786500': 86, '1534787100': 72, '1534787700': 95, '1534788300': 98, '1534788900': 35, '1534789500': 31, '1534790100': 17, '1534790700': 32, '1534791300': 49, '1534791900': 43, '1534792500': 66, '1534793100': 131, '1534793700': 68, '1534794300': 48, '1534794900': 43, '1534795500': 45, '1534796100': 46, '1534796700': 26}, 'ads': {'1534712100': 0, '1534712700': 6, '1534713300': 0, '1534713900': 0, '1534714500': 0, '1534715100': 0, '1534715700': 0, '1534716300': 0, '1534716900': 0, '1534717500': 0, '1534718100': 0, '1534718700': 0, '1534719300': 0, '1534719900': 0, '1534720500': 0, '1534721100': 0, '1534721700': 0, '1534722300': 0, '1534722900': 0, '1534723500': 0, '1534724100': 0, '1534724700': 0, '1534725300': 0, '1534725900': 0, '1534726500': 0, '1534727100': 0, '1534727700': 0, '1534728300': 0, '1534728900': 0, '1534729500': 0, '1534730100': 0, '1534730700': 0, '1534731300': 0, '1534731900': 0, '1534732500': 0, '1534733100': 0, '1534733700': 0, '1534734300': 0, '1534734900': 0, '1534735500': 0, '1534736100': 0, '1534736700': 0, '1534737300': 0, '1534737900': 0, '1534738500': 0, '1534739100': 0, '1534739700': 0, '1534740300': 0, '1534740900': 0, '1534741500': 0, '1534742100': 0, '1534742700': 0, '1534743300': 0, '1534743900': 0, '1534744500': 0, '1534745100': 0, '1534745700': 0, '1534746300': 0, '1534746900': 0, '1534747500': 0, '1534748100': 0, '1534748700': 0, '1534749300': 0, '1534749900': 0, '1534750500': 0, '1534751100': 0, '1534751700': 0, '1534752300': 0, '1534752900': 0, '1534753500': 0, '1534754100': 0, '1534754700': 0, '1534755300': 0, '1534755900': 0, '1534756500': 0, '1534757100': 0, '1534757700': 0, '1534758300': 0, '1534758900': 0, '1534759500': 0, '1534760100': 0, '1534760700': 0, '1534761300': 0, '1534761900': 0, '1534762500': 0, '1534763100': 0, '1534763700': 0, '1534764300': 0, '1534764900': 0, '1534765500': 0, '1534766100': 0, '1534766700': 0, '1534767300': 0, '1534767900': 0, '1534768500': 0, '1534769100': 0, '1534769700': 0, '1534770300': 0, '1534770900': 0, '1534771500': 0, '1534772100': 0, '1534772700': 0, '1534773300': 0, '1534773900': 0, '1534774500': 0, '1534775100': 0, '1534775700': 3, '1534776300': 19, '1534776900': 21, '1534777500': 12, '1534778100': 23, '1534778700': 40, '1534779300': 12, '1534779900': 3, '1534780500': 5, '1534781100': 9, '1534781700': 11, '1534782300': 39, '1534782900': 13, '1534783500': 13, '1534784100': 18, '1534784700': 12, '1534785300': 6, '1534785900': 19, '1534786500': 14, '1534787100': 7, '1534787700': 17, '1534788300': 26, '1534788900': 18, '1534789500': 10, '1534790100': 9, '1534790700': 10, '1534791300': 24, '1534791900': 13, '1534792500': 19, '1534793100': 21, '1534793700': 8, '1534794300': 7, '1534794900': 4, '1534795500': 7, '1534796100': 6, '1534796700': 4}}
```

You can grab just the domain data by using:
```python3
pihole.getGraphData()["domains"]
```

And just the ads data by using:
```python3
pihole.getGraphData()["ads"]
```

To refresh the top data, first [authenticate](#Controls), then use:
```python3
pihole.refreshTop(10)
```
Replace the `10` with how many results you want back.

The top data can then be fetched using:
```python3
pihole.top_queries # returns all top queries

# Or

pihole.top_ads # returns all top ads
```

To view all queries, use:
```python3
pihole.getAllQueries()
```

This returns a list of lists containing data about all queries. Fore more info, see the getAllQueries section of: https://discourse.pi-hole.net/t/pi-hole-api/1863

To get the filesize of the database file, use:
```python3
pihole.getDBfilesize()
```

To get the contents of your white/black list, use:
```python3
pihole.getList("black")
```
"black" can be replaced with "white" to get your whitelist



### <div id="Controls"> Controls </div>
First, you must log in. Use the password you set or where given by the installer (the same one you use on the web control panel)
```python3
pihole.authenticate(password)
```

To enable pihole, authenticate, then use:
```python3
pihole.enable()
```

To disable pihole, authenticate, then use:
```python3
pihole.disable(10)
```
replace `10` with the number of **seconds** that you want to disable pihole for.

Add a domain to one of your lists:
```python3
pihole.add("black", "google.com")
```
The example blacklists google.com. Replacing black with one of: **white**, **black**, **wild**, **regex**, or **audit** will change the list to be added to. To remove a domain form a list, replace `add()` with `sub()`

