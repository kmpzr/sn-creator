import httplib2
import ConfigParser, os
import json
import getopt, sys
from datetime import datetime, timedelta
config = ConfigParser.ConfigParser()
config.read('sn-creator.cfg')
config_section = "sn-creator"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "td:v", ["title=",
          "description="])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    title = None
    description = None
    for o, a in opts:
        if o in ("--t", "--title"):
            title = a
        elif o in ("--d", "--description"):
            description = a
        else:
            assert False, "unhandled option"

    if title == None or description == None:
      print "Arguments --t and --d is required"
      sys.exit(2)

    #Httplib2 initialization
    h = httplib2.Http(".cache")
    h.add_credentials(config.get(config_section, 'username'),
        config.get(config_section, 'password'))

    # Translate Team Names to sys_id
    url_get_groups = "%s/sys_user_group_list.do?JSON" % config.get(config_section, 'sn_url')
    resp, content = h.request(url_get_groups)
    groups = {x['name'].lower(): x['sys_id'] for x in json.loads(content)['records']}
    try:
        id_assigned = groups[config.get(config_section,'assigned_group').lower()]
        id_requestor = groups[config.get(config_section,'requestor_group').lower()]
    except KeyError as e:
        print "One of the Groups does not exists. Exiting...\n Exception: %s" % {e}
        sys.exit(2)

    url_post_new = "%s/u_service_desk.do?JSON&sysparm_action=insert" % config.get(config_section, 'sn_url')
    due_date = (datetime.now().replace(microsecond=0) +
        timedelta(minutes=30)).isoformat(' ')
    payload = {'u_requested_by_group': id_requestor, 'assignment_group': id_assigned,
    'short_description': title, 'description': description, 'due_date':
    due_date}
    print "The following payload information:\n"
    print json.dumps(payload)
    print "\nWill be posted to the following URL:\n"
    print url_post_new
    print "\n+++++++ DO YOU WANT TO CONTINUE?(Y/N) +++++++"
    res = raw_input("")
    if (res != "Y") and (res != "y"):
      sys.exit(2)
    headers = {'Content-type': 'application/json'}
    resp, content = h.request(url_post_new, 'POST', headers=headers,
        body=json.dumps(payload))
    print "Content:\n"
    print content
    print "\nResp:\n"
    print resp

if __name__ == "__main__":
    main()
