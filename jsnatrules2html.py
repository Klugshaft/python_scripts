
##  Generate Junper firewall NAT rules in LSYS or without LSYS into  HTML
##  please run 'show configuration security nat | display json | no-more ' to get the json formatted rule
## then just include, save only what is in between curly the braces { } in the json file
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
        # after json mod read, return file pointer to the beginning
        fwrinjson.seek(0)

        for line in fwrinjson.readlines():
            # check if it's in an lsys
            if "logical-systems" in line :
                is_in_lsys = True
                # print(line)
                break

        fwrinjson.close()
        #print(is_in_lsys)
        return fwr_list




def ft_nat_fwr(cnt, arr_prefix, natfwrdict):

## convert show configuration security policy | display json

    natfwrlist = []

    rset_cnt = len(arr_prefix['security']['nat']['source']['rule-set'])
    #print("there are ", rcnt,  "of rules")

    ruleset = arr_prefix['security']['nat']['source']['rule-set'][cnt]
    ruleset_name =  ruleset['name']
    from_zone = ruleset['from']['zone']
    to_zone = ruleset['to']['zone']

    ruleset_rule = ruleset['rule']
    rsr_cnt = len(ruleset_rule)



    for cntrule in range(rsr_cnt) :
        nat_rules = {}

        rs_rule_cnt = ruleset_rule[cntrule]

        rs_rule_name = rs_rule_cnt['name']
        rs_rule_src = rs_rule_cnt['src-nat-rule-match']['source-address-name']
        rs_rule_dst = rs_rule_cnt['src-nat-rule-match']['destination-address']

        num_rsr_src = len(rs_rule_src)
        num_rsr_dst = len(rs_rule_dst)

        rsr_src_objs = [rs_rule_src[i] for i in range(num_rsr_src)]
        rsr_dst_objs = [rs_rule_dst[i] for i in range(num_rsr_dst)]

        rs_rule_pool_name = rs_rule_cnt['then']['source-nat']['pool']['pool-name']

        nat_rules['ruleset name'] = ruleset_name
        nat_rules['from_zone'] = from_zone
        nat_rules['to_zone'] = to_zone
        nat_rules['rule name'] = rs_rule_name
        nat_rules['source'] = rsr_src_objs
        nat_rules['destination'] = rsr_dst_objs
        nat_rules['source nat pool'] = rs_rule_pool_name

        natfwrlist.append(nat_rules)


    return natfwrlist

def ft_srcnat_pool(cnt, arr_prefix, snatpooldict):

## convert show configuration security nat source | display json

    srcnatpool = []

    poolcnt = len(arr_prefix['security']['nat']['source']['pool'])
    #print("there are ", poolcnt,  "of snatpool")

    snatpool = arr_prefix['security']['nat']['source']['pool'][cnt]

    snatpoolname = snatpool['name']
    snatpooladdrlist = snatpool['address']
    num_snatpooladdr = len(snatpooladdrlist)

    snatpooladdr_objs = [ snatpooladdrlist[i] for i in range(num_snatpooladdr)]

    #for num_snatpool in range(poolcnt) :

    srcnatpooldict = {}
    srcnatpooldict['pool name'] = snatpoolname
    srcnatpooldict['address'] = snatpooladdr_objs

    srcnatpool.append(srcnatpooldict)



    return srcnatpool





if __name__ == '__main__':
    main()

    print('please run from command line \'show configuration security nat source | display json | no-more \' \nto get the json formatted rule. Then just include, save only what is in between the curly braces { } in the json file.\n')

    firewall_name = input('Enter firewall name for SNAT rules :')
    outputfile = input('enter output filename in <file>.html :')

    snatruledict = decode_fwr_in_json()
    print(is_in_lsys)

    if is_in_lsys is True :
        arr_prefix = snatruledict['configuration']['logical-systems'][0]
    else :

        arr_prefix = snatruledict['configuration']

    pcnt = len(arr_prefix['security']['nat']['source']['pool'])
    rset_cnt = len(arr_prefix['security']['nat']['source']['rule-set'])

    with open(outputfile,'w') as htmlfile:
        # write header

        htmlfile.write('Firewall Policy for {} \n'.format(firewall_name))
        htmlfile.write('Commited on {} \n'.format(fwrdict['configuration']['@']['junos:commit-localtime']))

        # start extracting SNATPOOL
        for snp in range(pcnt) :

            snatpools = []
            snatpool_item = ft_srcnat_pool(snp, arr_prefix, snatruledict)
            snatpools.append(snatpool_item)
            snatpooljson = json.dumps(snatpools)
            snatpool_in_html = json2html.convert( json = snatpooljson )
            htmlfile.write(snatpool_in_html)

        ## start extracting NAT rules
        for rscnt in range(rset_cnt) :

            natrsList = []
            natrsList_item = ft_nat_fwr(rscnt, arr_prefix, snatruledict)
            natrsList.append(natrsList_item)
            natrsListjson = json.dumps(natrsList)
            natrsList_in_html = json2html.convert( json = natrsList )
            htmlfile.write(natrsList_in_html)


    htmlfile.close()











