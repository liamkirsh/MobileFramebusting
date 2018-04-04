const KEY = "securityHeaders"
const HEADERS_TO_LOG = ["x-frame-options", "content-security-policy"]

chrome.webRequest.onHeadersReceived.addListener(function(data) {
        if ("main_frame" === data.type) {
            processResponseHeaders(data.responseHeaders);
        }
    },
    {urls: ["<all_urls>"] },
    ['responseHeaders', 'blocking']);

function processResponseHeaders(headers) {
    var security_headers = headers.filter(
        header => HEADERS_TO_LOG.indexOf(header['name'].toLowerCase()) > -1
    );
    //console.log(security_headers);
    // square brackets around KEY tell JS to compute the string
    chrome.storage.local.set({[KEY]: security_headers});
}
