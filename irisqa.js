(function() { 
var player='unknown',player_ver='',scripts= [],css=[],html,err="",msg="",frames,frame=false,stage='s3.amazonaws.com/iris-playground',prod='ovp.iris.tv/plugins';

try {
if (typeof bc != "undefined" && typeof bc.VERSION != "undefined") player= "Brightcove"; else if(typeof jwplayer != "undefined") player= "JW"; else if(typeof kWidget != "undefined" || typeof KWidget != "undefined") player="Kaltura"; else if (typeof AKAMAI_MEDIA_PLAYER != "undefined" || typeof akamai != "undefined") player="AKAMAI_MEDIA_PLAYER"; else if (typeof vdb != "undefined" || typeof vidible != "undefined") player="VIDIBLE"; else if (typeof tpScriptPath != "undefined" || typeof tpk != "undefined") player="THE PLATFORM"; else if (typeof THEOplayer != "undefined" || typeof theoplayer != "undefined") player="O PLayer";
var elscripts = [].slice.call(document.querySelectorAll("script[src*='" + stage + "'], script[src*='" + prod + "']"));
	for (var i = 0, len = elscripts.length; i < len; i++) {
     	scripts.push(elscripts[i].src)
	}
var elcss = [].slice.call(document.querySelectorAll("link[href*='iris-bc.standard'], link[href*='kaltura_ui.min.css'], link[href*='iris-bc.adaptive.css']"));
	for (var i = 0, len = elcss.length; i < len; i++) {
     	css.push(elcss[i].href)
	}
frames = document.getElementsByTagName('iframe');
frame = frames[0];
if(frame){
	var elfscripts= [].slice.call(frame.contentWindow.document.querySelectorAll("script[src*='s3.amazonaws.com/iris-playground'], script[src*='ovp.iris.tv/plugins']"));
	var elfcss = [].slice.call(frame.contentWindow.document.querySelectorAll("link[href*='iris-bc.standard'], link[href*='kaltura_ui.min.css'], link[href*='iris-bc.adaptive.css']"));
	if(elfscripts >0) {
		for (var i = 0, len = elfscripts.length; i < len; i++) {
     		scripts.push(elfscripts[i].src)
		}
	}
	if(elfcss.length >0) {
		for (var i = 0, len = elfcss.length; i < len; i++) {
     		css.push(elfcss[i].href)
		}
	}
}
if(css.length==0) msg="<font color=red>Looks like there was no Iris CSS file loaded/added </font></br>" ;
if(scripts.length==0) err="There was no Iris Javascript loaded/added </br>" ;
if (typeof bc != "undefined" && typeof bc.VERSION != "undefined") player_ver = "Brightcove v" + bc.VERSION;

if(scripts.length >0 || css.length>0) {
	scripts = scripts.join("</br> ");
	css = css.join("</br> ");
	html="IRIS FILES: </br>";
	html += scripts + "</br>" + css + "</br>";
}

var todo = document.body.innerHTML;
var re = new RegExp('data-account\s*=\s*("*|\'*)([^"\']+)("*|\'*)','ig');
//var token = todo.match(re)[2];
var m, token = [];
while (m = re.exec(todo)) {
    token.push(m[2]);
}
token = token.filter(function (x, i, a) { return a.indexOf(x) == i; });
var reu = new RegExp('thumbs_up\s*:\s*false','i');
var red = new RegExp('thumbs_down\s*:\s*false','i');
var res = new RegExp('skip_on_thumbs_down\s*:\s*false','i');
var tu = reu.test(todo);
var td = red.test(todo);
var skip = res.test(todo);

var re2 = new RegExp('data-player\s*=\s*("*|\'*)([^"\']+)("*|\'*)','ig');
var regPlayer = new RegExp('platform_id:*\s*=*\s*("*|\'*)([^"\']+)("*|\'*)','ig');
var platform_id = todo.match(regPlayer)[2];
var matches, playerIds = [];
while (matches = re2.exec(todo)) {
    playerIds.push(matches[2]);
}
playerIds = playerIds.filter(function (x, i, a) { return a.indexOf(x) == i; });
html += "Player type: " + player + "</br>";
if(player_ver != "") html += "Player version: " + player_ver + "</br>";
if(scripts.indexOf(".standard.") > 0 || css.indexOf(".standard.") > 0) html += "Iris Plugin type: Standard (old)</br>";
if(scripts.indexOf(".adaptive.") > 0 || css.indexOf(".adaptive.") > 0) html += "Iris Plugin type: Adaptive (new)</br>";
if(msg != "") html += msg;
if((scripts.indexOf(stage) > 0 && scripts.indexOf(prod) > 0) || (css.indexOf(stage) > 0 && css.indexOf(prod) > 0)) html += "<font color=red>ERROR: Page contains files for both Iris stage and production</font></br>";
if((scripts.indexOf(".adaptive.") > 0 && scripts.indexOf(".standard.") > 0) || (css.indexOf(".adaptive.") > 0 && css.indexOf(".standard.") > 0)) html += "<font color=red>ERROR: Page contains files for both Iris adaptive and standard</font></br>";
if(err != "") html += "<font color=red>ERROR: " + err + "</font></br>";
if(tu) html += "<font color=red>WARN: thumbs_up was set to false</font></br>";
if(td) html += "<font color=red>WARN: thumbs_down was set to false</font></br>";
if(td) html += "<font color=red>WARN: skip_on_thumbs_down was set to false</font></br>";
if(err != "") html += "<font color=red>ERROR: " + err + "</font></br>";
if(platform_id.indexOf("player") >=0) html += "<font color=red>ERROR: platform_id: " + platform_id + ", appears to be setup incorrectly </font></br>";

if(token.length>0) html += "TOKEN(S) FOUND: " + token.join(" , ") + "</br>";
if(playerIds.length>0) html += "PLAYER ID(S) FOUND: " + playerIds.join(" , ") + "</br>";
if(token.length>0 || playerIds.length>0) html += "Token and Player IDs found include any items that may have been commented out";
if(document.querySelector('[id*=thumbs_up]') === null && document.querySelector('[id*=thumbs-up]') === null && document.querySelector('[src*="brightcove/buttons/like.png"]') === null) html+= "<font color=red>WARN: Could not locate thumbs_up icon might be in an iFrame</font></br>";
if(document.querySelector('[id*=thumbs_down]') === null && document.querySelector('[id*=thumbs-down]') === null && document.querySelector('[src*="brightcove/buttons/dislike.png"]') === null) html+= "<font color=red>WARN: Could not locate thumbs_down icon might be in an iFrame</font></br>";
if(document.querySelector('[id*=skip_back]') === null && document.querySelector('[id*=skip-back]') === null && document.querySelector('[src*="brightcove/buttons/prev.png"]') === null) html+= "<font color=red>WARN: Could not locate skip back icon might be in an iFrame</font></br>";
if(document.querySelector('[id*=skip_forward]') === null && document.querySelector('[id*=skip-forward]') === null && document.querySelector('[src*="brightcove/buttons/next.png"]') === null) html+= "<font color=red>WARN: Could not locate skip forward icon might be in an iFrame</font></br>";
var iDiv = document.createElement('div');
iDiv.id = 'iris-qa';
iDiv.innerHTML = html;
document.getElementsByTagName('body')[0].appendChild(iDiv);
}
catch(e) {
	if(window.console && window.console.log) console.log(e);
}

} )();