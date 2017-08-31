// Node module components used =====================================================================
var express  = require('express');
var cors = require('cors');
var bodyParser = require('body-parser'); 
   // pull information from HTML POST (express4)

var app      = express();
    app.use(cors());                             // create our app w/ express
    app.use(bodyParser.urlencoded({
    extended: true }));
const querystring = require('querystring');

var serveIndex = require('serve-index');

function getNewestFile(dir, regexp) {
    var fs = require("fs"),
     path = require('path'),
    newest = null,
    files = fs.readdirSync(__dirname + "/" + dir),
    one_matched = 0,
    i

    for (i = 0; i < files.length; i++) {

        if (regexp.test(files[i]) == false)
            continue
        else if (one_matched == 0) {
            newest = files[i];
            one_matched = 1;
            continue
        }

        f1_time = fs.statSync(path.join(dir, files[i])).mtime.getTime()
        f2_time = fs.statSync(path.join(dir, newest)).mtime.getTime()
        if (f1_time > f2_time)
            newest[i] = files[i]  
    }

    if (newest != null)
    	fs.readFile(path.join(__dirname + "/" + dir, newest), 'utf8', function(err, contents) {
    		console.log(contents);
    		return contents;
		});
    
    return null
}

function getFile(file, regexp) {
	var fs = require("fs"),
     path = require('path')
     fs.readFile(path.join(__dirname + "/reports/", file), 'utf8', function(err, contents) {
    		console.log(contents);
    		return contents;
		});
	}


app.use('/reports', serveIndex('reports'));
app.use('/reports', express.static('reports'))
fname = "test_report" + new Date().getTime() + ".html"

app.get('/', function(req, res) {
       res.sendFile('views/index.html', { root: __dirname }); // load the single view file (angular will handle the page changes on the front-end)
    });


// application ================================================================================
app.post("/run_test", function(req, res){
   
    var jsonData = JSON.stringify(req.body);

    console.log(jsonData);
    

    var thumbs = req.body.thumb_state;
    var skip = req.body.skip_state;
    var time = req.body.timeout;
    var ads = req.body.ads;
    var browser = req.body.browser;
    var url = "http://s3.amazonaws.com/iris-playground/cosmos/test_pages/qabrightcovenextgen.html"
    if (req.body.player_url && req.body.player_url !="") url = req.body.player_url;
    if (url.indexOf("?") >0) {
        i = url.indexOf("?")
        url = url.slice(0,i+1)  + encodeURIComponent(url.slice(i+1));
    }
    var m = "accounts"
    var b=""
    var pre_roll =""
    var forward = "";
    if (browser != "firefox") b=" --browser=" + browser;
    if (ads != "false") pre_roll = " --ads=" + ads;
    if (skip == "false") forward = " --skip=False"

    if (thumbs == "false" && skip == "true" ) m = "nothumbs";
    else if (thumbs == "false" && skip == "false" ) m = "nobuttons";
    var timeout = "";
    if (time > 60 || time < 60) timeout = " --timeout="+time
    
    var command = 'pytest -m ' + m + timeout + b + pre_roll + forward +  ' --accounts=True --html=reports/' + fname + ' --url=' + url;
    console.log(command)
    const{ exec } = require('child_process');
    exec(command, (e, stdout, stderr)=> {
        if (e instanceof Error) {
            console.error(e);
            throw e;
        }
        console.log('stdout ', stdout);
        //getNewestFile("reports",new RegExp('.*\.html'))
        getFile(fname)
        console.log('stderr ', stderr);
    });
    res.json({ report: 'reports/' + fname })
});

// listen (start app) ====================================================================
app.listen(8777);
console.log("App listening on port 8777");