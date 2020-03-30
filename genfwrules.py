#-------------------------------------------------------------------------------
# Name:        generate juniper SRX rules
# Purpose:
#
# Author:      F Kwok
#
# Created:     07/03/2020
# Copyright:   (c) Calvin Kwok 2020
# Licence:     open source
#-------------------------------------------------------------------------------
import json
from os import path

def Check_Input_File(desc):


### use this for python 2.7, parm = raw_input(desc)

    while True:

        parm = input(desc)

        if path.exists(parm.strip()) :

            return parm
            break

        else:

            print("File does not exist!!, try again!!")


def main():

    fwr_json = Check_Input_File("enter your json file which contains the firewall rules: ")
    with open(fwr_json, "r") as injson:
        jsdict = json.load(injson)

        for numrul in range(len(jsdict['fwrule'])) :
            for srcobjs in range(len(jsdict['fwrule'][numrul]['source_object'])) :
                print('set security policies from-zone',jsdict['fwrule'][numrul]['from_zone'],'to-zone',jsdict['fwrule'][numrul]['to_zone'],'policy',jsdict['fwrule'][numrul]['rule_name'],'match source-address',jsdict['fwrule'][numrul]['source_object'][srcobjs])
            for dstobjs in range(len(jsdict['fwrule'][numrul]['dest_object'])) :
                print('set security policies from-zone',jsdict['fwrule'][numrul]['from_zone'],'to-zone',jsdict['fwrule'][numrul]['to_zone'],'policy',jsdict['fwrule'][numrul]['rule_name'],'match destination-address',jsdict['fwrule'][numrul]['dest_object'][dstobjs])
            for appidx in range(len(jsdict['fwrule'][numrul]['service'])) :
                print('set security policies from-zone',jsdict['fwrule'][numrul]['from_zone'],'to-zone',jsdict['fwrule'][numrul]['to_zone'],'policy',jsdict['fwrule'][numrul]['rule_name'],'match application',jsdict['fwrule'][numrul]['service'][appidx])
            if jsdict['fwrule'][numrul]['traffic_control'] == "" :
                print('set security policies from-zone',jsdict['fwrule'][numrul]['from_zone'],'to-zone',jsdict['fwrule'][numrul]['to_zone'],'policy',jsdict['fwrule'][numrul]['rule_name'],'then',jsdict['fwrule'][numrul]['action'])

            else :
                print('set security policies from-zone',jsdict['fwrule'][numrul]['from_zone'],'to-zone',jsdict['fwrule'][numrul]['to_zone'],'policy',jsdict['fwrule'][numrul]['rule_name'],'then',jsdict['fwrule'][numrul]['action'],'application-servies application-traffic-control rule-set',jsdict['fwrule'][numrul]['traffic_control'])

            print('set security policies from-zone',jsdict['fwrule'][numrul]['from_zone'],'to-zone',jsdict['fwrule'][numrul]['to_zone'],'policy',jsdict['fwrule'][numrul]['rule_name'],'then log',jsdict['fwrule'][numrul]['log'])

            print('\n')


##  print(list(jsdict['fwrule'][0]['source_object']))


if __name__ == '__main__':
    main()

# example below
