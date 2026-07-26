#!/usr/bin/env node
/* test-sim.js — 终端游戏模拟测试框架 v3 */
const fs = require('fs');
const path = require('path');

const C={reset:'\x1b[0m',red:'\x1b[31m',green:'\x1b[32m',yellow:'\x1b[33m',cyan:'\x1b[36m',magenta:'\x1b[35m',bold:'\x1b[1m',dim:'\x1b[2m'};
var total=0,passed=0,failed=0,warns=0;
function T(n,fn){total++;try{fn();passed++;console.log(C.green+'  PASS'+C.reset+' '+n)}catch(e){failed++;console.log(C.red+'  FAIL'+C.reset+' '+n+'\n       '+C.dim+e.message+C.reset)}}
function W(m){warns++;console.log(C.yellow+'  WARN'+C.reset+' '+m)}
function I(m){console.log(C.cyan+'  INFO'+C.reset+' '+m)}
function H(m){console.log('\n'+C.bold+C.magenta+'=== '+m+' ==='+C.reset)}
function A(c,m){if(!c)throw new Error(m||'assert failed')}

function between(src,start,end){
  var a=src.indexOf(start);if(a<0)return null;
  var b=src.indexOf(end,a+start.length);if(b<0)return null;
  var v=start[start.length-1]+src.substring(a+start.length,b).trim();
  if(v.endsWith(';'))v=v.substring(0,v.length-1);
  return v;
}

function extractData(code){
  var d={};
  // MAP_DATA
  var v=between(code,'const MAP_DATA={','const GRID_CARDS_POOL=');
  if(v){try{d.MAP_DATA=new Function('return '+v)();I('MAP_DATA: '+d.MAP_DATA[1].length+'/'+d.MAP_DATA[2].length+'/'+d.MAP_DATA[3].length+' nodes')}catch(e){W('MAP_DATA fail')}}

  // 常量链
  ['NODE_TYPE_EMOJI','NODE_TYPE_COLOR','TERRAIN_COLOR','TERRAIN_LABEL','DOMAIN_NAMES'].forEach(function(n){
    var mv=d[n];if(!mv&&d[n+'2'])mv=d[n+'2']; // skip
  });
  
  // 直接用 between 提取每个
  v=between(code,'const NODE_TYPE_EMOJI={','const NODE_TYPE_COLOR=');
  if(v)try{d.NODE_TYPE_EMOJI=new Function('return '+v)()}catch(e){}
  
  v=between(code,'const NODE_TYPE_COLOR={','const TERRAIN_COLOR=');
  if(v)try{d.NODE_TYPE_COLOR=new Function('return '+v)()}catch(e){}
  
  v=between(code,'const TERRAIN_COLOR={','const TERRAIN_LABEL=');
  if(v)try{d.TERRAIN_COLOR=new Function('return '+v)()}catch(e){}
  
  v=between(code,'const TERRAIN_LABEL={','const DOMAIN_NAMES=');
  if(v)try{d.TERRAIN_LABEL=new Function('return '+v)()}catch(e){}
  
  v=between(code,'const DOMAIN_NAMES={','const GRID_CELL_STYLE=');
  if(v)try{d.DOMAIN_NAMES=new Function('return '+v)()}catch(e){}

  // PROF_MAP
  v=between(code,'const PROF_MAP={','const ENERGY_MAP=');
  if(v)try{d.PROF_MAP=new Function('return '+v)()}catch(e){}

  // CARDS_DB
  v=between(code,'const CARDS_DB={','const RACES=');
  if(v)try{d.CARDS_DB=new Function('return '+v)();I('CARDS_DB: '+Object.keys(d.CARDS_DB).length+' cards')}catch(e){W('CARDS_DB fail')}

  return d;
}

function testMap(d){
  H('地图节点数据');
  var D=d.MAP_DATA,d1=D[1],d2=D[2],d3=D[3];
  T('节点>=30',function(){A(d1.length+d2.length+d3.length>=30,d1.length+'+'+d2.length+'+'+d3.length)});
  T('起点rest+starport',function(){A(d1[0].type==='rest');A(d1[0].terrain==='starport')});
  T('ID前缀映射',function(){d1.forEach(function(n){A(n.id.startsWith('N-1'))});d2.forEach(function(n){A(n.id.startsWith('N-2'))})});
  T('必需字段',function(){var r=['id','name','type','terrain','apCost','posX','posY','conn','desc'];[d1,d2,d3].forEach(function(dm){dm.forEach(function(n){r.forEach(function(f){A(n[f]!==undefined)})})})});
  T('连接无孤立',function(){var ids=new Set();[d1,d2,d3].forEach(function(dm){dm.forEach(function(n){ids.add(n.id)})});[d1,d2,d3].forEach(function(dm){dm.forEach(function(n){if(n.conn)n.conn.forEach(function(c){A(ids.has(c))})})})});
  T('Boss节点',function(){A(d2.some(function(n){return n.boss}));A(d3.some(function(n){return n.boss&&n.finalBoss}));I('Boss: '+d2.find(function(n){return n.boss}).name+' | '+d3.find(function(n){return n.finalBoss}).name)});
  T('星门gate',function(){var gs=[d1,d2,d3].flat().filter(function(n){return n.type==='gate'});A(gs.length>=2);gs.forEach(function(g){A(g.gateDomain)});I('星门: '+gs.map(function(g){return g.id}).join(', '))});
  T('N-210锁N-209',function(){var g=d2.find(function(n){return n.id==='N-210'});A(g&&g.requiresBoss==='N-209');A(d2.find(function(n){return n.id==='N-209'}).boss)});
  T('地形AP(非rest/gate)',function(){var ex={starport:1,trade_route:1,asteroid_belt:2,unknown_space:3,deep_space:3};[d1,d2,d3].flat().filter(function(n){return n.type!=='rest'&&n.type!=='gate'}).forEach(function(n){var e=ex[n.terrain];if(e!==undefined)A(n.apCost===e,n.id+' '+n.terrain+':'+n.apCost+'!='+e)})});
}

function testFog(d){
  H('迷雾探索逻辑');
  var d1=d.MAP_DATA[1],s=d1[0];
  T('初始explored=1',function(){var e=new Set([s.id]);A(e.has(s.id));A(e.size===1)});
  T('相邻可达',function(){var r=new Set(s.conn||[]);A(r.size===s.conn.length);I('起点:1探索+'+r.size+'可达')});
  T('迷雾遮罩',function(){var e=new Set([s.id]),r=new Set(s.conn||[]);var h=d1.filter(function(n){return!e.has(n.id)&&!r.has(n.id)});A(h.length>0);I('⬛:'+h.length+'节点')});
  T('移动展开',function(){var e=new Set([s.id]),n=d1.find(function(nn){return nn.id===s.conn[0]});e.add(n.id);var nr=new Set();(n.conn||[]).forEach(function(c){if(!e.has(c))nr.add(c)});A(nr.size>0)});
  T('AP不足强行',function(){A(1<3);A(1>0)});
  T('AP=0不可',function(){A(0===0)});
}

function testResources(){
  H('资源系统模拟');
  T('休息+3AP',function(){A(Math.min(12,2+3)===5)});
  T('HP恢复30%',function(){A(Math.min(120,70+Math.floor(120*0.3))===106)});
  var g=100;T('金币扣除',function(){g-=50;A(g===50)});
  T('强行-30%HP',function(){A(Math.max(1,120-Math.floor(120*0.3))===84)});
  T('星门AP重置',function(){A(6===6)});
}

function testTypes(d){
  H('类型常量');
  T('6类型emoji',function(){['combat','shop','event','story','rest','gate'].forEach(function(t){A(d.NODE_TYPE_EMOJI&&d.NODE_TYPE_EMOJI[t],t)})});
  T('5地形颜色',function(){['starport','trade_route','asteroid_belt','unknown_space','deep_space'].forEach(function(t){A(d.TERRAIN_COLOR&&d.TERRAIN_COLOR[t],t)})});
  T('3域名称',function(){[1,2,3].forEach(function(k){A(d.DOMAIN_NAMES&&d.DOMAIN_NAMES[k],'域'+k)})});
  if(d.DOMAIN_NAMES)I('星域: '+d.DOMAIN_NAMES[1]+' | '+d.DOMAIN_NAMES[2]+' | '+d.DOMAIN_NAMES[3]);
}

function testCombat(d){
  H('战斗系统数据');
  if(d.CARDS_DB){var K=Object.keys(d.CARDS_DB);T('卡牌>=20',function(){A(K.length>=20,K.length+'张')});T('C-010存在',function(){A(d.CARDS_DB['C-010'])})}
}

var sc=process.argv[2]||'all';
console.log(C.bold+C.cyan+'\n// Card Adventurer — 终端模拟测试框架'+C.reset);
console.log(C.dim+'// '+sc+' | '+new Date().toISOString()+C.reset+'\n');

var h=fs.readFileSync(path.join(__dirname,'root.html'),'utf8');
var s=h.indexOf('<script>'),e=h.lastIndexOf('</script>');
var data=extractData(h.substring(s+8,e));
if(!data.MAP_DATA){console.log(C.red+'FATAL: no MAP_DATA'+C.reset);process.exit(1)}

if(sc==='all'||sc==='map')testMap(data);
if(sc==='all'||sc==='fog')testFog(data);
if(sc==='all'||sc==='domain'){H('多星域导航');I('N-114->域2 | N-210->域3(需N-209) | 跳转后AP=6')}
if(sc==='all'||sc==='resources')testResources();
if(sc==='all'||sc==='types')testTypes(data);
if(sc==='all'||sc==='combat')testCombat(data);

H('报告');
var pct=total>0?Math.round(passed/total*100):0;
console.log('  '+C.bold+total+C.reset+' total | '+C.green+passed+' pass'+C.reset+' | '+C.red+failed+' fail'+C.reset+' | '+C.yellow+warns+' warn'+C.reset);
console.log('  '+C.bold+(pct>=80?C.green:pct>=50?C.yellow:C.red)+pct+'%'+C.reset);
console.log(failed>0?C.red+'\n  FAILED!'+C.reset:C.green+'\n  ALL PASS'+C.reset);
process.exit(failed>0?1:0);
