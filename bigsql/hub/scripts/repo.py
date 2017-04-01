
##################################################################
########    Copyright (c) 2016-2017 BigSQL         ###############
##################################################################

import os, commands, re, json, urllib2, datetime
import util, meta, api

PGDG_REPO_LIST="json-pgdg-repo-list"

YUM_LIST = ['el6', 'el7']
APT_LIST = ['precise', 'trusty', 'xenial']


def discover(p_repo):
  rlist = [p_repo]
  if p_repo == "pgdg":
    rlist = []
    repo_dict = get_json_file(PGDG_REPO_LIST)
    os = util.get_os()
    for rl in repo_dict:
      if os == rl['os']:
        rlist.append(rl['repo'])

  for r in rlist:
    [pghome, pgver, svcname, svcfile, datadir, port, logdir] = get_pgdg_base(r)
    if pghome != "1":
      print("########################################")
      print("#  pghome = " + pghome)
      print("#   pgver = " + pgver)
      print("# svcname = " + svcname)
      print("# svcfile = " + svcfile)
      print("# datadir = " + datadir)
      print("#    port = " + port)
      print("#  logdir = " + logdir)
      print("########################################")
      meta.put_components(p_repo, "pgdg", pgver + "-1", "linux64", port, "Enabled", 
                          "on", datadir, logdir, svcname, "postgres")
  return


def get_pgdg_base(p_repo):
  basedir = None
  ver = None
  svcname = None
  datadir = None
  port = None
  logdir = None
  to_devnull = " >/dev/null 2>&1"

  if p_repo == "pgdg10":
    ver = "10"
  elif p_repo == "pgdg96":
    ver = "9.6"
  elif p_repo == "pgdg95":
    ver = "9.5"
  elif p_repo == "pgdg94":
    ver = "9.4"
  elif p_repo == "pgdg93":
    ver = "9.3"
  elif p_repo == "pgdg92":
    ver = "9.2"
  else:
    util.exit_message("Invalid PGDG Repo, " + p_repo, 1)
  
  basedir = "/usr/pgsql-" + ver
  svcname = "postgresql-" + ver

  pgbin = basedir + "/bin/postgres"
  if os.path.isfile(pgbin):
    print("\n## PostgreSQL found at " + pgbin)
  else:
    print("\nPostgreSQL not found at " + pgbin)
    return ("1111111")

  if util.is_systemd():
    sysdir = util.get_systemd_dir()
    svcfile = sysdir + "/" + svcname + ".service"
  else:
    sysdir = "/etc/init.d"
    svcfile = sysdir + "/" + svcname
  if not os.path.isfile(svcfile):
    print("Service Control file not found at " + svcfile)
    return ("1111111")

  datadir = "/var/lib/pgsql/" + ver + "/data"
  cmd = "sudo ls " + datadir
  rc = os.system(cmd + to_devnull)
  if rc != 0:
    print("DATADIR not found at " + datadir)
    return ("1111111")

  pidfile = datadir + "/postmaster.pid"
  cmd = "sudo ls " + pidfile
  rc = os.system(cmd + to_devnull)
  if rc == 0:
    cmd = "sudo cat " + pidfile + " | sed -n '4p'"
    port = commands.getoutput(cmd)
  else:
    port = "1"

  logdir = datadir + "/pg_log"
  cmd = "sudo ls " + logdir
  rc = os.system(cmd + to_devnull)
  if rc != 0:
    logdir = ""
  
  return([basedir, ver, svcname, svcfile, datadir, port, logdir])


## retrieve json file from REPO
def get_json_file(p_file):
  json_file = p_file + ".txt"
  repo = util.get_value("GLOBAL", "REPO")
  repo_file = repo + "/" + json_file
  out_dir = os.getenv("PGC_HOME") + os.sep + "conf" + os.sep + "cache"

  if util.http_get_file(False, json_file, repo, out_dir, False, ""):
    out_file = out_dir + os.sep + json_file
    try:
      return(json.loads(util.read_file_string(out_file)))
    except:
      pass

  util.exit_message("Cannot process json_file '" + p_file + "'", 1)


## check whether a postgresql repo (yum or apt) is installed
def is_installed(p_repo):
  this_os = util.get_os()
  if this_os in YUM_LIST:
    cmd = "sudo yum repolist | grep " + p_repo + " >/dev/null"
    rc = os.system(cmd)
    if rc == 0:
      return(True)

  if this_os in APT_LIST:
    repo_file_name = get_apt_repo_file_name()
    if os.path.isfile(repo_file_name):
      return(True)

  return(False)


def get_apt_repo_file_name():
    rf_prefix = "/var/lib/apt/lists/apt.postgresql.org_pub_repos_apt_dists_"
    rf_suffix = "_main_binary-amd64_Packages"
    return(rf_prefix + util.get_os() + "-pgdg" + rf_suffix)


## list repositories
def list():
  repo_dict = get_json_file(PGDG_REPO_LIST)
  os = util.get_os()
  kount = 0
  for rl in repo_dict:
    if os == rl['os']:
      kount = kount + 1
      if is_installed(rl['repo']):
        print("@" + rl['repo'])
      else:
        print(rl['repo'])

  if kount == 0:
    print("No repo's available for os = " + os)
    return 1

  return 0


def get_repo(p_repo):
  if util.get_os() in APT_LIST:
    jf = "json-" + p_repo
    pkg_mgr = "apt"
  else:
    jf = "json-" + p_repo + "-" + util.get_os()
    pkg_mgr = "yum"
  rd = get_json_file(jf)

  pkg_prod = get_json_file("json-pgdg-pkg-prod")
  pkg_filter = []
  for p in pkg_prod:
    try:
      p[pkg_mgr]
      pkg_filter.append(p[pkg_mgr].replace('XX', rd['ver']))
    except:
      pass

  key = ""
  if util.get_os() in APT_LIST:
    key = rd['key']
  
  return([rd['repo-type'], rd['name'], rd['url'], rd['package'], key, pkg_filter])
  


def is_repo(p_repo):
  repo_dict = get_json_file(PGDG_REPO_LIST)
  os = util.get_os()
  for rl in repo_dict:
    if os == rl['os']:
      if rl['repo'] == p_repo:
        return(True)
  return(False)


def validate_os():
  os = util.get_os()
  if (os in YUM_LIST) or (os in APT_LIST):
    return;
  util.exit_message("OS '" + os + "' not supported for this command.", 1)


def install_packages(p_repo, p_pkg_list):
  if not is_repo(p_repo):
    print (p_repo + " is not a valid repo.")
    return(1)

  os = util.get_os()
  if os == "el6":
    cmd = "yum --enablerepo=" + p_repo + " install " + options()
  else:
    cmd = "yum repo-pkgs " + p_repo + " install " + options()
  for pl in p_pkg_list:
    cmd = cmd + " " + str(pl)
  util.run_sudo(cmd, True)
  return 0


def remove_packages(p_repo, p_pkg_list):
  if not is_repo(p_repo):
    print (p_repo + " is not a valid repo.")
    return(1)

  os = util.get_os()
  if os == "el6":
    cmd = "yum --enablerepo=" + p_repo + " remove " + options()
  else:
    cmd = "yum repo-pkgs " + p_repo + " remove " + options()
  for pl in p_pkg_list:
    cmd = cmd + " " + str(pl)
  util.run_sudo(cmd, True)
  return 0


## list packages within a repository
def list_packages(p_repo, p_SHOWDUPS, p_isJSON, p_isEXTRA):
  if not is_repo(p_repo):
    print (p_repo + " is not a valid repo.")
    return(1)

  [repo_type, name, url, package, key, pkg_filter] = get_repo(p_repo)

  if not is_installed(p_repo):
    print(p_repo + " is not registered.")
    return(1) 

  options = ""
  if p_SHOWDUPS:
    options = "--showduplicates"

  if util.get_os() in APT_LIST:
    return list_apt_packages(p_repo, p_isJSON)

  os = util.get_os()
  if os == "el6":
    cmd = "yum list all | grep " + p_repo
  else:
    cmd = "yum repo-pkgs " + p_repo + " list " + options
  cmd = cmd + " | awk '"

  ## filter package list unless asked to show --extra or --test
  kount = 0
  if not p_isEXTRA:
    for p in pkg_filter:
      kount = kount + 1
      ps = "/" + p.replace('.','\.') + "/"
      if kount > 1:
        cmd = cmd + " || " + ps
      else:
        cmd = cmd + ps

  cmd = cmd + " { print }' | awk '!/debug/ && !/docs/ { print }'"
  outp = commands.getoutput("sudo " + cmd)

  repo_pkg = []
  for line in outp.splitlines():
    data = line.split()
    if len(data) != 3:
      continue
    p1 = data[0].find('.')
    pkg_nm = data[0][0:p1]
    p2 = data[1].find('.rhel')
    if p2 > 0:
      pkg_ver = data[1][0:p2]
    else:
      pkg_ver = data[1]
    status = ""
    if data[2].startswith("@"):
      status = "Installed"
    repo_pkg.append([pkg_nm, pkg_ver, status])

  response = urllib2.urlopen(url)
  content = response.read()
  http_pkg = []
  for line in content.splitlines():
    if line.startswith("<tr>"):
      p1 = line.find('href="') + 6
      p2 = line.find('"', p1)
      pkg_file = line[p1:p2]
      p3 = line.find('class="m">', p2) + 10
      p4 = line.find(' ', p3)
      pkg_dt = line[p3:p4]
      if "debug" not in pkg_file and pkg_file.endswith(".rpm"):
        http_pkg.append([pkg_dt, pkg_file])

  repoList = []
  for r in repo_pkg:
    pkg_nm = r[0]
    pkg_ver = r[1]
    status = r[2]
    pkg_dt = ""
    repoDict = {}
    for h in http_pkg:
      pkg_file = h[1]
      if pkg_file.find(pkg_nm) > -1:
        if pkg_file.find(pkg_ver) > -1:
          pkg_dt = h[0]
          repoDict['component'] = pkg_nm
          repoDict['version'] = pkg_ver
          try:
            d2 = datetime.datetime.strptime(pkg_dt,'%Y-%b-%d').strftime('%Y-%m-%d')
            repoDict['release_date'] = d2
          except:
            repoDict['release_date'] = pkg_dt
          repoDict['status'] = status
          repoDict['repo'] = p_repo
          repoList.append(repoDict)
          break

  keys = ['component', 'version', 'release_date', 'status', 'repo']
  headers = ['Component', 'Version', 'RlsDate', 'Status', 'Repo']

  if p_isJSON:
    print(json.dumps(repoList, sort_keys=True, indent=2))
  else:
    print(api.format_data_to_table(repoList, keys, headers))

  return(0)


def list_apt_packages(p_repo, p_isJSON):
  raw_list = util.read_file_string(get_apt_repo_file_name())
  repoList = []
  repoDict = {}
  for line in raw_list.splitlines():
    data = line.split()
    if len(data) != 2:
      continue
    if data[0] == "Package:":
      repoDict['component'] = data[1]
    if data[0] == "Version:":
      version = data[1]
      
    if data[0] == "Filename:":
      repoDict['filename'] = data[1]
      p1 =  version.find(".pgdg16.04")
      if p1 > 0:
        repoDict['version'] = version[0:p1]
        repoList.append(repoDict)
      repoDict = {}

  keys = ['component', 'version']
  headers = ['Component', 'Version']

  if p_isJSON:
    print(json.dumps(repoList, sort_keys=True, indent=2))
  else:
    print(api.format_data_to_table(repoList, keys, headers))

  return(0)



## process register/unregister REPO command
def process_cmd(p_mode, p_repo):
  if not is_repo(p_repo):
    print("ERROR: " + p_repo + " not available.")
    return(1)

  isInstalled = is_installed(p_repo)

  if p_mode == "register":
    if isInstalled:
      print(p_repo + " already registered.")
      return(0)
    else:
      return(register(p_repo))

  if p_mode == "unregister":
    if isInstalled:
      return(unregister(p_repo))
    else:
      print(p_repo + " is not registered.")
      return(0)

  return 1


## register REPO
def register(p_repo):
  [repo_type, name, url, package, key, repo_filter] = get_repo(p_repo)
  repo_pkg = url + "/" + package
  util.run_sudo("yum install " + options() + repo_pkg)
  return 0


## unregister REPO
def unregister(p_repo):
  [repo_type, name, url, package, key, repo_filter] = get_repo(p_repo)
  util.run_sudo("yum remove " + options() + name)
  return 0


def options():
  opts = ""
  if os.getenv('isYes','') == "True":
    opts = "-y "
  return(opts)

