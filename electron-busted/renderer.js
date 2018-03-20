// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.

window.BUSTED = require('./node_modules/busted/busted.js');
 
var URL = 'http://www.nytimes.com';
var iframe = document.getElementById('frame');
var output = document.getElementById('output');
var fs = require('fs');
var content = "";
var fileName = "output.txt";
var sites;
// fileName is a string that contains the path and filename created in the save file dialog.  

fs.readFile("Top450.txt", 'utf-8', (err, data) => {
        if(err){
            alert("An error ocurred reading the file :" + err.message);
            return;
        }
        // Change how to handle the file content
	sites = data.split("\n");
	var i;
	for(i = 0; i < sites.length; i++){
//		console.log(sites[i]);
		URL = sites[i];
		iframe.src = URL;
 
 
		//iframe.onload = function() {
  		//	var passed = window.BUSTED.iframeTest(URL, iframe);
  			//alert(URL + (passed ? ' passed ' : ' failed ') + 'the iframe test.');
		//	frameTest = passed ? "passed" : "failed";
			window.BUSTED.headersTest(URL, function(url, response) {
				var frameAncest = "no frame-ancestors";
				console.log(response.csp);
				if(response.csp && response.csp.includes("frame-ancestors")) {
					 frameAncest = "frame-ancestors";
				}
  				content += url + "," + response.xFrame + "," + frameAncest + "\n";
				//console.log(content);
				output.textContent = content;
			});
		//}
	}
	
        //console.log("The file content is : " + data);
}); 
