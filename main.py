#!/usr/bin/env python3

"""""
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

from sys import argv
from src.fetch import fetch_all
from os.path import isdir

def main(args):
	if len(args) < 5:
		print("Inavlid Statent")
		return False
	ocean = args[1]
	page = args[2]
	ids = args[3:-1]
	output = argv[-1]
	if ocean not in ("meri", "emer", "ceru"):
		print("Invalid Ocean")
		return False
	elif page not in ("isld", "flag", "crew", "pirt"):
		print("Invalid Page")
		return False
	elif isdir(output) == False:
		print("Invalid Output Directory")
		return False
	else:
		fetch_all((ocean, page), ids, output)

if __name__	== "__main__":
	main(argv)
