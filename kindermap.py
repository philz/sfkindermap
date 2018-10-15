#!/usr/bin/python
#
# MIT License
#
# Copyright (c) 2018 Philip Zeyliger
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# You need to get a Google Maps API Key. This will make 75 * 5 = 375 requests,
# which should cost $5-10.

from urllib import quote_plus
import urllib2
import json
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--home", required=True, help="Home Address")
parser.add_argument("--work", required=True, help="Work Address")
parser.add_argument("--apikey", required=True, help="Google Maps API Key")
args = parser.parse_args()

# Compute the next weekday at 8am. Google needs a future
# date here. I'm only 70% sure the timezones here work
# out, and your machine may locally need to be running
# in pacific time for this to work.
t = datetime.date.today()
if t.weekday() >= 4:
  next_weekday = t + datetime.timedelta(days=7 - t.weekday())
else:
  next_weekday = t + datetime.timedelta(days=1)
next_weekday
assert t.weekday() < 5
depart = datetime.datetime(year=next_weekday.year, month=next_weekday.month, day=next_weekday.day, hour=8)
depart_s = depart.strftime("%s")

def time(origin, destination, mode):
  assert mode in ("driving", "transit")
  url = "".join(["https://maps.googleapis.com/maps/api/distancematrix/json?&origins=",
    quote_plus(origin),
    "&destinations=", quote_plus(destination),
    "&mode=", mode,
    "&key=", args.apikey.strip(),
    "&departure_time=", depart_s
  ])
  d = urllib2.urlopen(url).read()
  e = json.loads(d)
  if mode == "driving":
    zz = e["rows"][0]["elements"][0]["duration_in_traffic"]["value"]/60.0
  else:
    zz = e["rows"][0]["elements"][0]["duration"]["value"]/60.0
  return zz

schools = [ row.strip().split("\t") for row in file("schools.txt").read().splitlines() ]

home = args.home
work = args.work

header_printed = False
for name, school in schools:
  a = time(home, school, "transit")
  b = time(school, work, "transit")
  c = time(home, school, "driving")
  d = time(school, home, "driving")
  e = time(home, work, "driving")

  transit_transit = a + b
  drive_drive_transit = c + d + e
  delta = drive_drive_transit - transit_transit
  m = min(transit_transit, drive_drive_transit)
  if delta < 0:
    approach = "transit"
  else:
    approach = "drive"
  if not header_printed:
    print "\t".join(["School Name", "School Addr", "Time", "Approach", "Diff between transit and driving", 
      "Transit from Home", "Transit School to Work", "Transit Total",
      "Driving to School", "Driving School to Home", "Transit to Work", "Driving Approach Total"])
    header_printed = True
  print "\t".join(map(str, [name, school, m, approach, delta, a, b, a + b, c, d, e, c + d + e]))
