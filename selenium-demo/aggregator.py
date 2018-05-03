import csv
import sys
#input
#output = open("", "w")
#output.write("# domain,desktop_no_antiframe_headers,mobile_no_antiframe_headers\n")
#for elem in sys.argv[1:]:
elem = "fileeeeee"
desktopNotTimedOut = 0
mobileNotTimedOut = 0
with open("fileeeeee", 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    next(reader)  # skip header row
    for row in reader:
        domain, desktop_xfo, desktop_csp, mobile_redir, mobile_xfo, mobile_csp = row
        #domain = domain.lstrip("http://")
        if desktop_xfo.strip() != "TIMEOUT_ERROR":
            desktopNotTimedOut += 1
        if mobile_xfo.strip() != "TIMEOUT_ERROR":
            mobileNotTimedOut += 1

print desktopNotTimedOut,mobileNotTimedOut
#output.close()

