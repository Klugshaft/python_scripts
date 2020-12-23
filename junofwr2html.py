##  Generate Junper firewall rules in LSYS or without LSYS into  HTML
##  please run 'show configuration security policies | display json | no-more ' to get the json formatted rule
## then just include, save only what is in between curly the braces { } in the json file
## 23/12/20 - added separate function to extract global firewall rules
## written by  - Calvin Kwok, Oct2020

import json
from json2html import *
from os import path

global is_in_lsys
is_in_lsys = False

def main():
    pass

def input_File(desc):


### use this for python 2.7, parm = raw_input(desc)

    while True:

        parm = input(desc)

        if path.exists(parm.strip()) :

            return parm
            break

        else:

            print('File does not exist!!, try again!!')
            return False


## produce a simpler version of firwwall rules in a dictionary format
def decode_fwr_in_json() :


    global is_in_lsys
    fwr_json = input_File('enter your json file which contains the firewall rules: ')

    with open(fwr_json, 'r') as fwrinjson :

        fwr_list = json.load(fwrinjson)
        # after json api read, return file pointer to the beginning
        fwrinjson.seek(0)

        for line in fwrinjson.readlines():
            if "logical-systems" in line :
                is_in_lsys = True
                # print(line)
                break

        fwrinjson.close()
        #print(is_in_lsys)
        return fwr_list




def ft_lsys_fwr(pcnt, fwr_arr_prefix):

## convert show configuration security policy | display json

    lsysfwrlist = []
    rcnt = len(fwr_arr_prefix['security']['policies']['policy'][pcnt]['policy'])
    #print("there are ", rcnt,  "of rules")

    policy_zone = fwr_arr_prefix['security']['policies']['policy'][pcnt]
    from_zone = policy_zone['from-zone-name']
    to_zone = policy_zone['to-zone-name']

    for rule in range(rcnt):

        lsysfwr = {}
        rule_id = policy_zone['policy'][rule]
        policy_name = rule_id['name']

        src_objs_list = rule_id['match']['source-address']
        dst_objs_list = rule_id['match']['destination-address']
        app_objs_list = rule_id['match']['application']

        num_src_objs = len(src_objs_list)
        num_dst_objs = len(dst_objs_list)
        num_app_objs = len(app_objs_list)

        source_objects = [ src_objs_list[i] for i in range(num_src_objs) ]
        dest_objects = [ dst_objs_list[i] for i in range(num_dst_objs) ]
        service_objs = [ app_objs_list[i] for i in range(num_app_objs) ]

        policy_action = list(rule_id['then'])[0]

        try :

            policy_log_option = list(rule_id['then']['log'])[0]
        except  (TypeError, IndexError, KeyError) :
            policy_log_option = ""

        try :
            application_traffic_ruleset = rule_id['then']['permit']['application-services']['application-traffic-control']['rule-set']

        except (TypeError, IndexError, KeyError) :
            application_traffic_ruleset = ""


        lsysfwr['policy_name'] = policy_name
        lsysfwr['from_zone'] = from_zone
        lsysfwr['to_zone'] = to_zone
        lsysfwr['source_objects'] = source_objects
        lsysfwr['dest_objects'] = dest_objects
        lsysfwr['service'] = service_objs
        lsysfwr['action'] = policy_action
        lsysfwr['traffic_ruleset'] = application_traffic_ruleset
        lsysfwr['log'] = policy_log_option


        lsysfwrlist.append(lsysfwr)

    return lsysfwrlist

def ft_global_fwr(gfwr_arr_prefix):

## convert show configuration security policy | display json

    globalfwrlist = []

    ## extract global policy
    try:

        global_policy = gfwr_arr_prefix['security']['policies']['global']['policy']
    except (TypeError, IndexError, KeyError) :
        print("global policy does not exist!")
        global_fwr = {}
    else:
        rcnt = len(gfwr_arr_prefix['security']['policies']['global']['policy'])
        print("there are ",rcnt," global policy")

        rnum = 0
        for grule in range(rcnt):

            global_fwr = {}
            rnum  = rnum + 1
            rule_id = global_policy[grule]
            policy_name = rule_id['name']

            src_objs_list = rule_id['match']['source-address']
            dst_objs_list = rule_id['match']['destination-address']
            app_objs_list = rule_id['match']['application']

            num_src_objs = len(src_objs_list)
            num_dst_objs = len(dst_objs_list)
            num_app_objs = len(app_objs_list)

            source_objects = [ src_objs_list[i] for i in range(num_src_objs) ]
            dest_objects = [ dst_objs_list[i] for i in range(num_dst_objs) ]
            service_objs = [ app_objs_list[i] for i in range(num_app_objs) ]

            policy_action = list(rule_id['then'])[0]

            try :

                policy_log_option = list(rule_id['then']['log'])[0]
            except  (TypeError, IndexError, KeyError) :
                policy_log_option = ""

            try :
                application_traffic_ruleset = rule_id['then']['permit']['application-services']['application-traffic-control']['rule-set']

            except (TypeError, IndexError, KeyError) :
                application_traffic_ruleset = ""

            global_fwr['num'] = rnum
            global_fwr['policy_name'] = policy_name
            global_fwr['source_objects'] = source_objects
            global_fwr['dest_objects'] = dest_objects
            global_fwr['service'] = service_objs
            global_fwr['action'] = policy_action
            global_fwr['traffic_ruleset'] = application_traffic_ruleset
            global_fwr['log'] = policy_log_option

            globalfwrlist.append(global_fwr)

    return globalfwrlist

if __name__ == '__main__':
    main()



    print('please run from command line \'show configuration security policies | display json | no-more \' \nto get the json formatted rule. Then just include, save only what is in between the curly braces { } in the json file.\n')

    outputfile = input('enter output filename in <file>.html :')

    fwrdict = decode_fwr_in_json()

    print(is_in_lsys)

    if is_in_lsys is True :
        fwr_arr_prefix = fwrdict['configuration']['logical-systems'][0]
    else :

        fwr_arr_prefix = fwrdict['configuration']

   # layout juniper fw rules with LSYS in json formatted list

    zcnt = len(fwr_arr_prefix['security']['policies']['policy'])
    print("there are ", zcnt, "different sets of policy with different src and dest zones.")
   # rcnt = len(fwrdict['configuration']['logical-systems'][0]['security']['policies']['policy'][0]['policy'])


    firewall_name = input('Enter Firewall name :')

    with open(outputfile,'w') as htmlfile:
        # write header

        htmlfile.write('Firewall Policy for {} \n'.format(firewall_name))
        htmlfile.write('Commited on {} \n'.format(fwrdict['configuration']['@']['junos:commit-localtime']))

        # start extracting rules in different set of src & dest zones
        fwrarray = []
        for zn in range(zcnt) : 
            fwr_in_zone = ft_lsys_fwr(zn, fwr_arr_prefix, fwrdict)
            fwrarray.append(fwr_in_zone[0])
            
        ## start with reformatting global firewall rules 
        gfwrules = ft_global_fwr(fwr_arr_prefix)
        fwrarray.append(gfwrules)
        allfwr_in_json = json.dumps(fwrarray)
        fwr_in_html = json2html.convert( json = allfwr_in_json )
        htmlfile.write(fwr_in_html)
    
    htmlfile.close()

