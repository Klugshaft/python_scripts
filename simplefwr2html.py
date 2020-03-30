#-------------------------------------------------------------------------------
# Name:        fwr2html
# Purpose:     translate firewall rules in json format to html
#
# Author:     FKwok
#
# Created:     11/03/2020
# Copyright:   (c) FKwok 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
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

            print("File does not exist!!, try again!!")

def main():
    pass

def outtohtml():

    fwr_json = Check_Input_File("enter your json file which contains the firewall rules: ")
    with open(fwr_json, "r") as injson:
        jdict = json.load(injson)

        #print(jdict)
        fwhtml = json2html.convert(json =  jdict )
        return fwhtml
    injson.close



if __name__ == '__main__':
    main()
    outputfile = input("enter output filename in <file>.html :")
    with open(outputfile,'w') as htmlfile:
        htmlstring = outtohtml()
        htmlfile.write(htmlstring)
        htmlfile.close()
