var fs=require('fs');
var h=fs.readFileSync('root.html','utf8');
var s=h.indexOf('<script>');
var e=h.lastIndexOf('</script>');
var c=h.substring(s+8,e);

// Find renderCrew and check brace balance
var start=c.indexOf('function renderCrew(){');
var end=c.indexOf('function calcCrewBonus(){');
if(start<0||end<0){console.log('not found',start,end);process.exit(1)}
var fn=c.substring(start,end+1); // include the first char of next function

console.log('renderCrew ends at',end,'calcCrew at',end);
console.log('Last 100 chars:',JSON.stringify(fn.substring(Math.max(0,fn.length-150))));

// Check braces ignoring string content
var inStr=false,inEsc=false,inTpl=false;
var d=0;
var err=null;
for(var i=0;i<fn.length;i++){
  var ch=fn[i],prev=i>0?fn[i-1]:'';
  if(inEsc){inEsc=false;continue}
  if(ch==='\\'){inEsc=true;continue}
  if(!inTpl&&(ch==='"'||ch==="'")){
    if(!inStr)inStr=ch;
    else if(inStr===ch)inStr=false;
    continue;
  }
  if(ch==='`'){inTpl=!inTpl;continue}
  if(inStr||inTpl)continue;
  if(ch==='{')d++;
  if(ch==='}'){
    d--;
    if(d<0){console.log('EXCESS } at',i,'context:',JSON.stringify(fn.substring(i-30,i+10)));break}
  }
}
console.log('Brace diff:',d);
console.log('renderCrew status:',d===0?'BALANCED':'IMBALANCED');
if(d===0)console.log('renderCrew OK - checking calcCrewBonus...');

// Also check calcCrewBonus
var fn2=c.substring(end,end+300);
var d2=0;
for(var j=0;j<fn2.length;j++){
  var ch2=fn2[j];
  if(ch2==='{')d2++;
  if(ch2==='}'){d2--;if(d2<0)console.log('EXCESS in calcCrew at',j)}
}
console.log('calcCrew diff:',d2);
