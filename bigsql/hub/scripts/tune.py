##################################################################
########    Copyright (c) 2016-2017 BigSQL         ###############
##################################################################

import util, os, json, sys, urllib2

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
import api
from PgInstance import PgInstance

## retrieve json file from REPO
def get_json_file(p_file):
  json_file = p_file + ".txt"
  repo = util.get_value("GLOBAL", "REPO")
  repo_file = repo + "/" + json_file
  out_dir = os.getenv("PGC_HOME") + os.sep + "conf" + os.sep + "cache"

  if util.http_get_file(False, json_file, repo, out_dir, False, ""):
    out_file = out_dir + os.sep + json_file
    try:
      return json.loads(util.read_file_string(out_file))
    except any:
      pass

  util.exit_message("ERROR: Cannot process json_file '" + p_file + "'", 1)

def do_pgc_tune(p_comp, email, print_json=False):

    tune_metadata="tuning_service_descriptor"
    tuning_service = get_json_file(tune_metadata)

    tune_request = {}
    tune_request['tune_request']={}

    util.read_env_file(p_comp)
    port = util.get_comp_port(p_comp)
    pg = PgInstance("localhost", "postgres", "postgres", int(port))
    pg.connect()
    tune_request['tune_request']['postgres_config'] = pg.get_raw_pg_settings()
    pg.close()


    tune_request['tune_request']['email'] = email
    tune_request['tune_request']['user_agent'] = 'pgc {}'.format(util.get_pgc_version())
    tune_request['tune_request']['postgres_config']['postgres_version'] = util.get_column('version', p_comp)
    tune_request['tune_request']['system_config'] = api.info(True, 'na', 'na', False)

    # Web request
    tune_url = tuning_service['bigtuna']['url']
    tune_url = tune_url + tuning_service['bigtuna']['path']
    req = urllib2.Request(tune_url)
    req.add_header('Content-Type', 'application/json')
    tune_result = urllib2.urlopen(req, json.dumps(tune_request))

    result = json.load(tune_result)

    if print_json:
        print json.dumps(result, sort_keys=True,
                         indent=2, separators=(',', ': '))
    else:
        for key in result['tune_result']:
            print "{} = {}".format(key, result['tune_result'][key])

