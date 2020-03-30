##  Generate firewall rules in html format
##  please run 'show security policies | display json | no-more ' to get the json formatted rule
## then just include, save only what is in between curly the braces { } in the json file
## written by Fung Y Kwok, March 2020

import json
from json2html import *
from os import path

def Check_Input_File(desc):


### use this for python 2.7, parm = raw_input(desc)

    while True:

        parm = input(desc)

        if path.exists(parm.strip()) :

            return parm
            break

        else:

            print('File does not exist!!, try again!!')

def main():
    pass

## produce a simpler version of firwwall rules in a dictionary format
def fwr2array() :

    fwr_json = Check_Input_File('enter your json file which contains the firewall rules: ')
    with open(fwr_json, 'r') as fwr_rule_in_json_format:
        return json.load(fwr_rule_in_json_format)
    fwr_rule_in_json_format.close()


def simplify_fwr(count,jdict) :

# convert from show security policies | display json
# This method is deprecated

        simpfwr = {}
        zone_cnt = jdict['multi-routing-engine-results'][0]['multi-routing-engine-item'][0]['security-policies'][0]['security-context']
        policy_id = zone_cnt[rcnt]['policies'][0]['policy-information'][0]
        policy_name = policy_id['policy-name'][0]['data']
        from_zone = zone_cnt[rcnt]['context-information'][0]['source-zone-name'][0]['data']
        to_zone = zone_cnt[rcnt]['context-information'][0]['destination-zone-name'][0]['data']
        src_objs_list = policy_id['source-addresses'][0]['source-address']
        dst_objs_list = policy_id['destination-addresses'][0]['destination-address']
        app_objs_list = policy_id['applications'][0]['application']
        num_src_objs = len(src_objs_list)
        num_dst_objs = len(dst_objs_list)
        num_app_objs = len(app_objs_list)
        source_objects = [ src_objs_list[i]['address-name'][0]['data'] for i in range(num_src_objs) ]
        dest_objects = [ dst_objs_list[i]['address-name'][0]['data'] for i in range(num_dst_objs) ]
        service_objs = [ app_objs_list[i]['application-name'][0]['data'] for i in range(num_app_objs) ]
        policy_action = zone_cnt[rcnt]['policies'][0]['policy-information'][0]['policy-action'][0]['action-type'][0]['data']

        try :
            applicaiton_traffic_ruleset = policy_id['policy-application-services'][0]['application-traffic-control'][0]['rule-set-name'][0]['data']
        except (indexError, KeyError ) :
            application_traffic_ruleset = 'none'

        try :
            if policy_id['policy-action'][0]['log'][0]['data'][0] is None :
                policy_log_option = "session-init"

        except KeyError :
                policy_log_option = ""


        simpfwr['policy_name'] = policy_name
        simpfwr['from_zone'] = from_zone
        simpfwr['to_zone'] = to_zone
        simpfwr['source_objects'] = source_objects
        simpfwr['dest_objects'] = dest_objects
        simpfwr['service'] = service_objs
        simpfwr['action'] = policy_action
        simpfwr['traffic_ruleset'] = application_traffic_ruleset
        simpfwr['log'] = policy_log_option

        return simpfwr

     # return rule in dictionary format


def simpfwr(rcnt, fwrdict):

## convert show configuration security policy | display json


    simpfwr = {}
    zcnt = len(fwrdict['configuration']['security']['policies']['policy'])

    policy_zone = fwrdict['configuration']['security']['policies']['policy']
    from_zone = policy_zone[rcnt]['from-zone-name']
    to_zone = policy_zone[rcnt]['to-zone-name']
    policy_id = policy_zone[rcnt]['policy'][0]
    policy_name = policy_id['name']

    src_objs_list = policy_id['match']['source-address']
    dst_objs_list = policy_id['match']['destination-address']
    app_objs_list = policy_id['match']['application']

    num_src_objs = len(src_objs_list)
    num_dst_objs = len(dst_objs_list)
    num_app_objs = len(app_objs_list)

    source_objects = [ src_objs_list[i] for i in range(num_src_objs) ]
    dest_objects = [ dst_objs_list[i] for i in range(num_dst_objs) ]
    service_objs = [ app_objs_list[i] for i in range(num_app_objs) ]

    policy_action = list(policy_id['then'])[0]

    try :

        policy_log_option = list(policy_id['then']['log'])[0]
    except  (TypeError, IndexError, KeyError) :
        policy_log_option = ""

    try :
        application_traffic_ruleset = policy_id['then']['permit']['application-services']['application-traffic-control']['rule-set']

    except (TypeError, IndexError, KeyError) :
        application_traffic_ruleset = ""


    simpfwr['policy_name'] = policy_name
    simpfwr['from_zone'] = from_zone
    simpfwr['to_zone'] = to_zone
    simpfwr['source_objects'] = source_objects
    simpfwr['dest_objects'] = dest_objects
    simpfwr['service'] = service_objs
    simpfwr['action'] = policy_action
    simpfwr['traffic_ruleset'] = application_traffic_ruleset
    simpfwr['log'] = policy_log_option

    return simpfwr

def simpfwr2json() :


    simpjsonfwr = simplify_fwr()


    fwhtml = json2html.convert(json = simpjsonfwr )
    return fwhtml




if __name__ == '__main__':
    main()

    print('please run from command line \'show security policies | display json | no-more \' \nto get the json formatted rule. Then just include, save only what is in between the curly braces { } in the json file.\n')

    outputfile = input('enter output filename in <file>.html :')

    fwrdict = fwr2array()

    fwarray = []
    simpfwrdict = {}
  #  zone_cnt = fwrdict['multi-routing-engine-results'][0]['multi-routing-engine-item'][0]['security-policies'][0]['security-context']
    zone_cnt = fwrdict['configuration']['security']['policies']['policy']

    for rcnt in range(len(zone_cnt)-1) :
        simpfwrdict = simpfwr(rcnt,fwrdict)
        fwarray.append(simpfwrdict)

    firewall_name = input('Enter Firewall name :')
    with open(outputfile,'a') as htmlfile:

        simpfwrjson = json.dumps(fwarray)
        fwr_in_html = json2html.convert( json = simpfwrjson )

        htmlfile.write('Firewall Policy for {} \n'.format(firewall_name))
        htmlfile.write('Commited on {} \n'.format(fwrdict['configuration']['@']['junos:commit-localtime']))
        htmlfile.write(fwr_in_html)

        htmlfile.close()
