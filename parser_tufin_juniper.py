# The codes below can handle variety of outputs. Please modify the filenames for your input data.
# You can modify the codes below to suit your need if you want to express your data differently.
import textfsm as tfm
import sys

# -show route | no more - command to list route table in Juniper SRX and save
#change the file name below to your output file
raw_file = "/python_scripts/sample_rules_generated_by_Tufin.txt"
input_rawfile = open(raw_file, 'r')
raw_text_data = input_rawfile.read()
input_rawfile.close()
#print(raw_text_data)
#open template file and initialize a new TextFSM object with it

template_file = "/python_scripts/juniper_policy_tmpla.txt"
template = open(template_file, 'r')
re_table = tfm.TextFSM(template)

# Read until EOF, then pass this to the FSM for parsing.
fsm_rt_list = re_table.ParseText(raw_text_data)

#write out result as a csv formatted file below

#change the filename below for your output file
outfile_name = "juniper_policy_tuf.csv"
outfile = open(outfile_name, 'w')

# Print header
 
for item in re_table.header[0][0] :
 
     print(', '.join(re_table.header))
     outfile.write(': '.join(re_table.header))
outfile.write('\n')

# below will hang your IDE if the list is going to be huge comment it out!
print(fsm_rt_list)

counter = 0
index = 0
#write out data from list
for row in fsm_rt_list :
# modify following to present how your data will look like
     for row_data in row :
          stripped_data = str(row_data).strip("[").strip("]").replace("'","")
#         try:
          outfile.write("{}: ".format(stripped_data))
#         except IndexError :
     outfile.write("\n")
     counter += 1


print("Write {} records".format(counter)) 
# write all rows

outfile.close()

