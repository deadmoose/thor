"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License,
or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.
"""

author = ["Thorkill"]
version = "0.1"

from multiprocessing.pool import Pool
import requests
from time import time
from .save import save_json
from .pirt_parse import pirt_parse
from .crew_parse import crew_parse
from .flag_parse import flag_parse
from .isld_parse import isld_parse

def build(page_type, urls):
	#Builds a yoweb URL
	#Expects a tuple (ocean, type) and the island/flag/crew id or a pirate name
    types = {"isld":"island/info.wm?islandid=", "flag":"flag/info.wm?flagid=", 
    		"crew":"crew/info.wm?crewid=", "pirt":"pirate.wm?target="}
    ocean = {"meri":"http://meridian", "emer":"http://emerald", "ceru":"http://cerulean"}
    page = ".puzzlepirates.com/yoweb/"
    for x in range(len(urls)):
    	urls[x] = ocean[page_type[0]] + page + types[page_type[1]] + urls[x]
    return urls

def fetch(url, page_type, output):
	#Fetches a yoweb page and times the request
	start = time()
	reqs = requests.get(url)
	html = reqs.text
	#Should probaly be expressed in regular miliseconds
	func = {"pirt" : pirt_parse, "crew" : crew_parse, "flag" : flag_parse, "isld" : isld_parse}
	save_json(func[page_type](html), output)
	final = time() - start
	print("Fetched %s in %s" %(url, final))

def fetch_all(page_type, ids, output):
	#Python multithreding mess incoming
	start = time()
	pages = []
	links = build(page_type, ids)
	#Number of worker processes to start
	num_of_proc = 8
	pool = Pool(processes=num_of_proc)
	#Fetches pages asynchronously
	results = [pool.apply_async(fetch, (url, page_type[1], output,)) for url in links]
	#Appends the fetched pages into the pages list
	for result in results:
		result.get()
	print("Fetched all in %s" %(time() - start))

if __name__ == "__main__":
	fetch_all(("meri", "isld"), [str(x) for x in range(20)], "output")
