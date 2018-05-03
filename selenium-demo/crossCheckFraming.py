import os

output = open("no_xfo_or_fa_or_sandbox_js.csv", "w")
#d = "./headers/no_xfo_or_fa"
blank = open("isBlank.txt",'r')
noSecHeaders = open("no_xfo_or_fa.csv","r")
next(noSecHeaders)
listOfEntries = []
for secline in noSecHeaders:
    domain,desktop,mobile = secline.split(',')
    if "TIMEOUT_ERROR" == desktop:
        desktop=0
    if "TIMEOUT_ERROR" == mobile:
        mobile=0
    listOfEntries.append((domain,desktop,mobile))


for line in blank:
    name,isVulnerable = line.split(",")
    isVulnerable.strip()
    isVulnerable = int(isVulnerable)
    if "mobile_" in name:
        name = name.lstrip("mobile_")
        isMobile = 1
    else:
        isMobile = 0
    name = name.rstrip(".png")
    
    generator = (entry for entry in listOfEntries if entry[0]== name )
    matchingEntry = next(generator,None)
    if matchingEntry:
        if isMobile:
            if int(matchingEntry[2]):
                if isVulnerable:
                    output.write( "{},Mobile,{}\n".format(matchingEntry[0],isVulnerable))
                
        else:
            if int(matchingEntry[1]):
                if isVulnerable:
                    output.write(  "{},Desktop,{}\n".format(matchingEntry[0],isVulnerable) )

output.close()
