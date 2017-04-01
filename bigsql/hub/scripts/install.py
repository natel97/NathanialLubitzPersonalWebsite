##################################################################
########    Copyright (c) 2016-2017 BigSQL         ###############
##################################################################

import sys, os
PGC_VER=os.getenv("PGC_VER", "3.1.4")
PGC_REPO=os.getenv("PGC_REPO", "http://s3.amazonaws.com/pgcentral")

if sys.version_info < (2, 6) or sys.version_info >= (3, 0):
  print("ERROR: BigSQL requires Python 2.6 or (preferably) Python 2.7")
  sys.exit(1)

import urllib2, tarfile

IS_64BITS = sys.maxsize > 2**32
if not IS_64BITS:
  print("ERROR: This is a 32bit machine and BigSQL packages are 64bit.")
  sys.exit(1)

if os.path.exists("bigsql"):
  print("ERROR: Cannot install over an existing 'bigsql' directory.")
  sys.exit(1)

pgc_file="bigsql-pgc-" + PGC_VER + ".tar.bz2"
f = PGC_REPO + "/" + pgc_file

if not os.path.exists(pgc_file):
  print("\nDownloading BigSQL PGC " + PGC_VER + " ...")
  try:
    fu = urllib2.urlopen(f)
    local_file = open(pgc_file, "wb")
    local_file.write(fu.read())
    local_file.close()
  except (urllib2.URLError, urllib2.HTTPError) as e:
    print("ERROR: Unable to download " + f + "\n" + str(e))
    sys.exit(1)

print("\nUnpacking ...")
try:
  tar = tarfile.open(pgc_file)
  tar.extractall(path=".")
  print("\nCleaning up")
  tar.close()
  os.remove(pgc_file)
except Exception as e:
  print("ERROR: Unable to unpack \n" + str(e))
  sys.exit(1)

print("\nSetting REPO to " + PGC_REPO)
pgc_cmd = "bigsql" + os.sep + "pgc"
os.system(pgc_cmd + " set GLOBAL REPO " + PGC_REPO)

print("\nUpdating Metadata")
os.system(pgc_cmd + " update --silent")

print("\nBigSQL PGC installed.  Try '" + pgc_cmd + " help' to get started.\n")

sys.exit(0)

