var WebPageTest = require('webpagetest')
var fs = require('fs');

const querystring = require('querystring');
// const path = require('path');
var wpt = new WebPageTest("https://www.webpagetest.org/","A.57c0ecce925470118d73687951af28ee")

'use strict';
// reading from the user website
let web_name = process.argv[2]
data_id = []
processweb_add();
function processweb_add() {
			wpt.runTest(web_name,{
			connectivity: 'cable',             // 'cable' or '4G' (9 Mbps 170ms RTT) specifing connection
			location: 'Dulles:Chrome',		  // Dulles 'Italy:Chrome' or IOS location
			firstViewOnly: false,
			runs: 1,
			pollResults: 5,
			video: true
		}, function processTeststatus(err, result) {
			console.log(err || result)
		//		console.log('Data id: ', result.data.id)

			//collecting all the test_ids
			data_id.push(result.data.id)

			// check result status
			check_status();
			// console.log("inside",data_id)
		})
   // }
}

function check_status(){
	// console.log(data_id.length)
	for(var i=0; i < data_id.length; i++){
		// using the data.testId of the website this checks on the status of the test
		wpt.getTestStatus(data_id[i], function processTestStatus(err, result) {
			// console.log(err || result)
			console.log("outside",data_id)
		})

		// using the data.testId of the website we get the test resutl
		wpt.getTestResults(data_id[i], function processTestResult(err, result) {
			 console.log(err || result)
			// console.log('web address: ', result.data.url)


			//console.log(err || result) //this will return the specific testId etc...
			console.log('Load time:', result.data.average.firstView.loadTime)
			console.log('First byte:', result.data.average.firstView.TTFB)
			console.log('Start render:', result.data.average.firstView.render)
			console.log('Speed Index:', result.data.average.firstView.SpeedIndex)
			console.log('DOM elements:', result.data.average.firstView.domElements)


			console.log('(Doc complete) Requests:', result.data.average.firstView.requestsDoc)
			console.log('(Doc complete) Byets in:', result.data.average.firstView.bytesInDoc)


			console.log('(Fully loaded) Time:', result.data.average.firstView.fullyLoaded)
			console.log('(Fully loaded) Requests:', result.data.average.firstView.requestsFull)
			console.log('(Fully loaded) Bytes in:', result.data.average.firstView.bytesIn)

			console.log('Waterfall view:', result.data.runs[1].firstView.images.waterfall)
			var q_data = querystring.stringify({
			'web address:': result.data.url,
			'Load time:': result.data.average.firstView.loadTime,
			'First byte:': result.data.average.firstView.TTFB,
			'Start render:': result.data.average.firstView.render,
			'Speed Index:': result.data.average.firstView.SpeedIndex,
			'DOM elements:': result.data.average.firstView.domElements,
			'(Doc complete) Requests:': result.data.average.firstView.requestsDoc,
			'(Doc complete) Byets in:': result.data.average.firstView.bytesInDoc,
			'(Fully loaded) Time:': result.data.average.firstView.fullyLoaded,
			'(Fully loaded) Requests:': result.data.average.firstView.requestsFull,
			'(Fully loaded) Bytes in:': result.data.average.firstView.bytesIn,
			'Waterfall view:': result.data.runs[1].firstView.images.waterfall,

			},';',':');
			// custome Metrics values
			//console.log('Iframes:', result.data.average.firstView.iframes)
			//console.log('Ads:', result.data.average.firstView.ad)

			//var data = JSON.stringify(q_data, null, 2)
			// fs.writeFile('words2.json', q_data, response);
			fs.appendFile('Test_results/' + web_name + '.txt', q_data, response);
			console.log(q_data);
			function response(err){
				console.log('saving response');
				// console.log(path.dirname());
			}

		})
	}
}
