import csv
import sys
#input
#output = open("", "w")
#output.write("# domain,desktop_no_antiframe_headers,mobile_no_antiframe_headers\n")
#for elem in sys.argv[1:]:

listOfEntries = []
out = 0
with open("no_xfo_or_fa_or_sandbox_js.csv", 'r') as secHeaders:
    for secline in secHeaders:
        domain,desktop_mobile,isVulnerable = secline.split(',')
        #if "TIMEOUT_ERROR" == desktop:
        #    desktop=0
        #if "TIMEOUT_ERROR" == mobile:
        #    mobile=0
        listOfEntries.append((domain,desktop_mobile,isVulnerable))
with open("no_xfo_or_fa_or_sandbox_js.csv", 'r') as newSecHeaders:
    for line in newSecHeaders:
        domain,desktop_mobile,isVulnerable = line.split(',')
        generator = (entry for entry in listOfEntries if entry[0] == domain)
        matchingEntry = next(generator)
        if next(generator,None) is None:
            out+=1
            print domain
 #       else:
#            print "doubled " + domain
            #continue
print out
