#-------------------------------------------------------------------------------
# Name:     generate srx firewall objects
# Purpose:  paste mulitple lines of obj, IP or objt port and port number/range separated
#           by space to the input
#           and it will generate statement for creating objects for juniper SRX firewall
#
# Author:     F Kwok
#
# Created:     08/03/2020
# Copyright:   (c) F Kwok 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys, fileinput

def gensrxfwrobj():

    print("paste objects with name and ip separated by space, then Ctrl ^Z to end: \n")
    lines = [ line for line in fileinput.input()]

    for each_objpair in lines:
        if each_objpair.strip() == '\n' :
            pass
        elif len(each_objpair.split()) == 2:
            fwobjlist = each_objpair.split()

            print('set security address-book global address',fwobjlist[0],fwobjlist[1])

        elif len(each_objpair.split()) == 1 or len(each_objpair.split()) > 2 :
            print("syntax error!!",'"',each_objpair.split()[0],'"'," <object name> <IP address/network>")


def genappobjs():

    print("paste objects with <port name> <port type> <port number> separated by space, then Ctrl ^Z to end: \n")
    lines = [ line for line in fileinput.input()]
##appobj = []
    for eachline in lines:

        if eachline.strip() == '\n':
            pass
        elif len(eachline.split()) == 3 :
            appobj = eachline.split()

            print('set applications application',appobj[0],'protocol',appobj[1],'destination-port',appobj[2])
        elif len(eachline.split()) == 1 or len(eachline.split()) > 3 :

            print("syntax error!! syntax : <port name> <port type> <port number>")



if __name__ == '__main__':
   # print('\n************commands for firewall objects*************')
    gensrxfwrobj()
    print('\n************commands for ports*************')
    genappobjs()
