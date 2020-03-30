#-------------------------------------------------------------------------------
# Name:        VPN config generator
# Purpose:      generate specific vpn config for projects
#
# Author:      Calvin Kwok
#
# Created:     25/02/2020
# Copyright:   (c) Calvin Kwok 2020
# Licence:     <myself>
# please use python 3 or else printout will include brackets
# version 2.0 - 20200226
#-version 2.1-- added optional print and fix csvfile.close issue if q is entered from start
# version 2.2 -- more fine tuning, getvpnccfg() just get one customer out of the csvDictReader table
#               fix customer count error - by using length of customer list
#-------------------------------------------------- -------------------------

import sys, time, re
from os import path
import csv
# import pdb

def IsInputInt(desc):
# check if input is integer
    while True:
        try:

            idx = int(input(desc))

            return idx
            break
        except :

            print("not a number, Enter again!")


def Check_Input_File(desc):


### use this for python 2.7, parm = raw_input(desc)

    while True:

        parm = input(desc)

        if path.exists(parm.strip()) :

            return parm
            break

        else:

            print("File does not exist!!, try again!!")




def get_cust_idx(total_cust_num, file_handle):


    while True:
            print('Customer index starts from 2, last index is',total_cust_num + 1,'\n')
            custidx = IsInputInt('Enter Customer Index displayed in Excel worksheet :')

            if custidx < 2 :

                return 0

                print('print config for the first customer ...:\n')

            elif custidx > total_cust_num + 1 :

                print('Last customer index is',total_cust_num + 1,'enter again !!')

            else :
                return custidx - 2




def getvpncfg(custtbl):


        print('-------------  Printing VPN Migration config for customer',custtbl['Customer'],'  ------------\n' )
        print('-----------The Magic comes !!!---------------\n')
        print('\n----------IKE Phase 1 proposal configuration--------\n')
        print('set security ike proposal',custtbl['p1_proposal'],'lifetime-seconds',custtbl['lifetime_secs'])
        print('set security ike proposal',custtbl['p1_proposal'],'authentication-method',custtbl['auth_method']+'s')
        print('set security ike proposal',custtbl['p1_proposal'],'authentication-algorithm',custtbl['auth_algo'])
        print('set security ike proposal',custtbl['p1_proposal'],'encryption-algorithm',custtbl['enc_algo'])
        print('set security ike proposal',custtbl['p1_proposal'],'dh-group',custtbl['dh_group'])

#       ----------Phase 1 policy definition-----------
        print('\n---------Phase 1 policy configuration----------\n')
        print('set security ike policy',custtbl['ike_policy_name'],'description','"'+custtbl['ike_policy_description']+'"')
        print('set security ike policy',custtbl['ike_policy_name'],'proposals',custtbl['p1_proposal'] )
        print('set security ike policy',custtbl['ike_policy_name'],'mode',custtbl['p1_mode'])
        print('set security ike policy',custtbl['ike_policy_name'],custtbl['auth_method'],'ascii-text "',custtbl['p1_preshared_key'],'"')

#       -------IKE phase 2 - IPsec Proposal definition /define if not already exisi/-----
        print('\n---------IPSec P2 proposal configuration---------\n')
        print('set security ipsec proposal',custtbl['p2_proposal_name'], 'lifetime-seconds',custtbl['p2_lifetime_secs'])
        print('set security ipsec proposal',custtbl['p2_proposal_name'], 'protocol',custtbl['p2_protocol'])
        print('set security ipsec proposal',custtbl['p2_proposal_name'], 'authentication-algorithm',custtbl['p2_auth_algo'])
        print('set security ipsec proposal',custtbl['p2_proposal_name'], 'encryption-algorithm',custtbl['p2_enc_algo'])

#       ---------IKE P1 Remote Gateway configuration---------
        print('\n---------Phase 1 IKE Gateway configuration----------\n')
        print('set security ike gateway' ,custtbl['p1_ike_gateway_name'] , 'ike-policy' ,custtbl['ike_policy_name'])
        print('set security ike gateway' ,custtbl['p1_ike_gateway_name'] , 'address' ,custtbl['remote_ike_gw_ip'])

        if  custtbl['DPD_interval'] == "":
            pass
        else :
            print('set security ike gateway' ,custtbl['p1_ike_gateway_name'] , 'dead-peer-detection',custtbl['DPD_opt'],'interval',custtbl['DPD_interval'])

        if custtbl['NAT_keepalive'] == "":
            pass
        else :
            print('set security ike gateway' ,custtbl['p1_ike_gateway_name'] , 'nat-keepalive' ,custtbl['NAT_keepalive'])

        print('set security ike gateway' ,custtbl['p1_ike_gateway_name'] , 'external-interface' ,custtbl['GW_ext_intf'])

        if custtbl['netscr_local_id'] == '':
            pass
        else :

            print('set security ike gateway' ,custtbl['p1_ike_gateway_name'] , 'local-identity inet' ,custtbl['local_vpn_endpoint'])

#

#       ------IPSec P2 IPSec policy definition------
        print('\n---------IPSec Policy Configuration ------------\n')
        print('set security ipsec policy',custtbl['p2_ipsec_policy_name'],'proposals',custtbl['p2_proposal_name'])
        print('set security ipsec policy',custtbl['p2_ipsec_policy_name'],custtbl['p2_pfs_option'])



#       --------IPSec P2 VPN tunnel configuration--------
        print('\n---------IPSec P2 Tunnel Configuration ----------\n')
        print('set security ipsec vpn',custtbl['p2_vpntun_name'],'ike ipsec-policy',custtbl['p2_ipsec_policy_name'])
        print('set security ipsec vpn',custtbl['p2_vpntun_name'],'ike gateway',custtbl['p1_ike_gateway_name'])
        print('set security ipsec vpn',custtbl['p2_vpntun_name'],'ike proxy-identity local',custtbl['p2_ike_proxy_id_local'])
        print('set security ipsec vpn',custtbl['p2_vpntun_name'],'ike proxy-identity remote',custtbl['p2_ike_proxy_id_remote'])
        print('set security ipsec vpn',custtbl['p2_vpntun_name'],'ike proxy-identity service',custtbl['p2_ike_proxy_id_srv'])
        print('set security ipsec vpn',custtbl['p2_vpntun_name'],'establish-tunnels',custtbl['p2_establish_tunnels'])

#        print('\n---remove below 2 lines if they are not needed !!\n')
        if custtbl['anti_replay'] == "yes" :
            pass
        else :
           print('set security ipsec vpn',custtbl['p2_vpntun_name'],'ike no-anti-replay')
        if custtbl['dscp_val'] == "":
            pass
        else :
            print('set class-of-service interfaces st0 unit',custtbl['p2_tunnel_unit'][4:],'classifiers dscp',custtbl['dscp_val'])



        #       -------IKE phase 2 Tunnel interface binding & VPN monitor -------
        print('\n---------IPSec P2 tunnel interface binding & VPN monitor------\n')

# if vpn monitor is not needed, just route thru un-numbered interface ie. config interface unit inet without ip addr
        if custtbl['p2_vpn_mon_src_ip'] == "" :
            print('set interfaces st0 unit',custtbl['p2_tunnel_unit'][4:],'family inet')
            print('set interfaces st0 unit',custtbl['p2_tunnel_unit'][4:],'description','"'+custtbl['p2_tunnel_desc']+'"')
            print('set security zones security-zone',custtbl['p2_security_zone'], 'interfaces',custtbl['p2_tunnel_unit'], 'host-inbound-traffic system-services ping')
        else :

            print('set interfaces st0 unit',custtbl['p2_tunnel_unit'][4:], 'description','"'+custtbl['p2_tunnel_desc']+'"','family inet address',custtbl['p2_vpn_mon_src_ip'])
            print('set security zones security-zone',custtbl['p2_security_zone'], 'interfaces',custtbl['p2_tunnel_unit'], 'host-inbound-traffic system-services ping')
            print('set security ipsec vpn',custtbl['p2_vpntun_name'],'vpn-monitor source-interface',custtbl['p2_tunnel_unit'])
            print('set security ipsec vpn',custtbl['p2_vpntun_name'],'vpn-monitor destination-ip',custtbl['p2_vpn_mon_dst_ip'])


        if  custtbl['p2_vpn_mon_opt'] == "" :
            pass
        else :
            print('set security ipsec vpn',custtbl['p2_vpntun_name'],'vpn-monitor',custtbl['p2_vpn_mon_opt'])

        print('set security ipsec vpn',custtbl['p2_vpntun_name'],'bind-interface',custtbl['p2_tunnel_unit'])
        print('set routing-instances',custtbl['routing_instance'],'interface',custtbl['p2_tunnel_unit'])



#----------------Add routes -----------------------------
        print('\n---------Add following routes-------------\n')
        print(custtbl['routes'])

#----------------Deactivate routes before cutover------------
        print('\n--------Deactivate route before cutover -------------\n')
        route_string1 = re.sub('next-hop\s.*','', custtbl['routes'])
        deac_route_statement = re.sub('set','deactivate',route_string1)
        print(deac_route_statement)

#----------------Deactivate config before cutover----------------
        print('\n-----------Deactivate config before cutover ---------------\n')
        print('deactivate routing-instances',custtbl['routing_instance'],'interface',custtbl['p2_tunnel_unit'])
        print('deactivate security ike gateway',custtbl['p1_ike_gateway_name'])
        print('deactivate security zones security-zone',custtbl['p2_security_zone'],'interfaces',custtbl['p2_tunnel_unit'])
        print('deactivate interfaces',custtbl['p2_tunnel_unit'])
        print('deactivate security ipsec vpn',custtbl['p2_vpntun_name'])

#---------------Activate routes for cutover------------
        print('\n--------Activate route at cutover -------------\n')
        ac_route_statement = re.sub("set","activate", route_string1)
        print(ac_route_statement)


#------------ Activate config at cutover -------------------------
        print('\n-----------activate config at cutover ---------------\n')
        print('activate routing-instances',custtbl['routing_instance'],'interface',custtbl['p2_tunnel_unit'])
        print('activate security ike gateway',custtbl['p1_ike_gateway_name'])
        print('activate security zones security-zone',custtbl['p2_security_zone'],'interfaces',custtbl['p2_tunnel_unit'])
        print('activate interfaces',custtbl['p2_tunnel_unit'])
        print('activate security ipsec vpn',custtbl['p2_vpntun_name'])
        print('\n')




def main():

    if sys.version_info[0] < 3 :
        print(" I need Python 3.7 to run or the output will not be correct !!")
        time.sleep(3)


    print('||||||||||   VPN Migration config generator v2.2  |||||||||||\n')

    while True :
# wait for a key pressed

        keypressed = input("Press 'Enter' to start or Press q to exit!")
#if key pressed is carriage return '\r'

        if keypressed == "" :


            print("continue...\n")

            csv_fname = Check_Input_File("Enter CSV file name :")

            csvfile_handle = open(csv_fname, 'r')

            custlist = csv.DictReader(csvfile_handle, skipinitialspace = True, delimiter = ',')

            customer_table = list(custlist)

            num_of_rows = len(customer_table)

            custidx = get_cust_idx(num_of_rows, csvfile_handle)

            customer = customer_table[custidx]

            getvpncfg(customer)

            csvfile_handle.close()


 #if key is 'q'
        elif keypressed == 'q' :


            print("Bye! Thanks for using my script...Exiting program !!")
            time.sleep(1)
            break
        else :
            continue



if __name__ == "__main__":

    main()


#### progrm ends
