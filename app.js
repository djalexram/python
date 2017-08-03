const exec = require('child_process').exec;
var url = "http://s3.amazonaws.com/iris-playground/cosmos/test_pages/qabrightcovenextgen.html"

function getFile(file, regexp) {
	var fs = require("fs"),
     path = require('path')
     fs.readFile(path.join(__dirname + "/reports/", file+ ".html"), 'utf8', function(err, contents) {
    		//console.log(contents);
    		return contents;
		});
	}
fname = "test_report" + new Date().getTime()

exec('python ovp-test.py --report ' + fname + ' --url ' + url, (e, stdout, stderr)=> {
    if (e instanceof Error) {
        console.error(e);
        throw e;
    }
    console.log('stdout ', stdout);

    getFile(fname)
    console.log('stderr ', stderr);
});