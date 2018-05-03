import csv
import sys

def is_valid_xfo(xfo):
    xfo = xfo.strip()
    return xfo == "DENY" or xfo == "SAMEORIGIN"


def is_valid_csp(csp):
    csp = csp.strip()
    csp_directives = [directive.strip() for directive in csp.split(';')]
    frame_ancestors = next((directive for directive in csp_directives
                            if directive.startswith("frame-ancestors")), None)
    if frame_ancestors:
        frame_ancestor_sources = frame_ancestors.split()[1:]
        if "'self'" or "'none'" in frame_ancestor_sources:
            return True
    return False


output = open("no_xfo_or_fa.csv", "w")
output.write("# domain,desktop_no_antiframe_headers,mobile_no_antiframe_headers\n")
for elem in sys.argv[1:]:
    print elem
    with open(elem, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader)  # skip header row
        for row in reader:
            domain, desktop_xfo, desktop_csp, mobile_redir, mobile_xfo, mobile_csp = row
            domain = domain.lstrip("http://")
            if desktop_xfo.strip() == "TIMEOUT_ERROR":
                d_url = desktop_xfo.strip()
            else:
                d_url = 1 if not is_valid_xfo(desktop_xfo) and not is_valid_csp(desktop_csp) else 0
            m_url = 1 if not is_valid_xfo(mobile_xfo) and not is_valid_csp(mobile_csp) else 0
            if (d_url and d_url != "TIMEOUT_ERROR") or (m_url and m_url != "TIMEOUT_ERROR"):
                output.write("{},{},{}\n".format(domain, d_url, m_url))
output.close()

"""
def has_framebust_header(security_headers):
    # FIXME: this is probably incomplete
    # FIXME: consider cases where XFO takes precedent over CSP or vice versa
    def is_framebust_header(header):
        hname = header['name'].lower()
        hvalue = header['value'].lower()

        if hname == 'x-frame-options':
            if (hvalue == 'sameorigin' or
                hvalue == 'deny'):
                return True
        elif hname == 'content-security-policy':
            csp_directives = [directive.strip() for directive in hvalue.split(';')]
            frame_ancestors = next((directive for directive in csp_directives
                                   if directive.startswith("frame-ancestors")), None)
            if frame_ancestors:
                frame_ancestor_sources = frame_ancestors.split()[1:]
                if "'self'" or "'none'" in frame_ancestor_sources:
                    return True
        return False

    return any(is_framebust_header(header) for header in security_headers)
"""
