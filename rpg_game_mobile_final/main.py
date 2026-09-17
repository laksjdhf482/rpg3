import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import mimetypes
import json

st.set_page_config(page_title="거지 탈출 RPG", page_icon="💰", layout="centered", initial_sidebar_state="collapsed")

BASE = Path(__file__).parent
ASSETS = BASE / "assets"

def data_uri(path):
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    return "data:" + mime + ";base64," + base64.b64encode(path.read_bytes()).decode()

stage_images = [data_uri(ASSETS / f"stage{i}.jpg") for i in range(1, 6)]
character_images = [data_uri(ASSETS / f"character{i}.png") for i in range(5)]

stage_images_json = json.dumps(stage_images, ensure_ascii=False)
character_images_json = json.dumps(character_images, ensure_ascii=False)

html = r'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000;font-family:Arial,"Noto Sans KR",sans-serif;touch-action:none}
body{overscroll-behavior:none}
button{font:inherit;color:#111;touch-action:manipulation}
#game{position:fixed;inset:0;width:100vw;height:100dvh;min-height:0;overflow:hidden;background-position:center;background-size:cover;background-repeat:no-repeat;user-select:none;-webkit-user-select:none}
#shade{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(255,255,255,.03),rgba(0,0,0,.10));pointer-events:none;z-index:0}
#top{position:absolute;left:10px;right:10px;top:max(8px,env(safe-area-inset-top));z-index:5;display:flex;justify-content:space-between;align-items:flex-start;gap:10px;pointer-events:none}
.info{color:#111;text-shadow:0 1px 2px rgba(255,255,255,.72),1px 0 0 rgba(255,255,255,.5),-1px 0 0 rgba(255,255,255,.5)}
#stageTitle{font-size:clamp(18px,5.2vw,27px);font-weight:900;line-height:1.05}
#moneyArea{text-align:right}
#moneyLabel{font-size:9px;font-weight:900}
#money{font-size:clamp(19px,6vw,31px);font-weight:900;line-height:1.02}
#clickIncome{font-size:clamp(9px,2.7vw,13px);font-weight:900;margin-top:3px}
#character{position:absolute;left:50%;bottom:5dvh;transform:translateX(-50%);width:auto;height:min(58dvh,520px);max-width:72vw;object-fit:contain;object-position:center bottom;filter:drop-shadow(0 5px 4px rgba(0,0,0,.38));z-index:2;pointer-events:none}
#progressArea{position:absolute;left:10px;right:10px;top:clamp(54px,12dvh,82px);z-index:5;pointer-events:none}
#progressText{display:flex;justify-content:space-between;gap:10px;color:#111;text-shadow:0 1px 2px rgba(255,255,255,.75),1px 0 0 rgba(255,255,255,.5),-1px 0 0 rgba(255,255,255,.5);font-size:clamp(9px,2.8vw,13px);font-weight:900}
#bar{height:6px;margin-top:4px;border:1px solid #111;border-radius:99px;overflow:hidden;background:rgba(255,255,255,.25)}
#fill{height:100%;width:0%;background:#111;transition:width .12s linear}
#notice{text-align:center;min-height:15px;margin-top:2px;color:#111;text-shadow:0 1px 2px rgba(255,255,255,.8);font-size:11px;font-weight:900}
#shopButton{position:absolute;right:10px;bottom:max(48px,calc(env(safe-area-inset-bottom) + 42px));z-index:20;width:60px;height:60px;border-radius:50%;border:3px solid #111;background:rgba(245,205,94,.95);font-size:12px;font-weight:900;box-shadow:3px 3px 0 rgba(0,0,0,.65);touch-action:manipulation}
#shop{display:none;position:absolute;z-index:30;left:50%;top:50%;transform:translate(-50%,-50%);width:min(91vw,410px);max-height:82dvh;overflow:auto;background:rgba(235,220,187,.96);border:3px solid #111;border-radius:15px;padding:11px;box-shadow:5px 5px 0 rgba(0,0,0,.7);color:#111;touch-action:auto}
#shop.open{display:block}
#shopHead{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
#shopTitle{font-size:22px;font-weight:900}
#closeShop{width:34px;height:34px;border:2px solid #111;border-radius:8px;background:#d9c9a8;font-weight:900}
.item{border:2px solid #111;border-radius:10px;padding:8px;margin:5px 0;background:rgba(220,202,164,.88)}
.itemName{font-size:15px;font-weight:900}
.itemDesc{font-size:10px;margin-top:2px}
.itemRow{display:flex;justify-content:space-between;align-items:center;gap:7px;margin-top:6px}
.level{font-size:10px;font-weight:800}
.action{border:2px solid #111;border-radius:8px;padding:6px 8px;background:#e7d8b7;font-weight:900;font-size:10px}
#reset{width:100%;margin-top:6px;padding:7px;border:2px solid #111;border-radius:8px;background:#d9c9a8;font-weight:900;font-size:10px}
.float{position:absolute;z-index:15;pointer-events:none;font-size:clamp(17px,5.5vw,29px);font-weight:900;color:#111;text-shadow:1px 1px 0 rgba(255,255,255,.8),-1px -1px 0 rgba(255,255,255,.5);animation:floatUp .72s ease-out forwards;white-space:nowrap}
@keyframes floatUp{from{opacity:1;transform:translate(-50%,0) scale(1)}to{opacity:0;transform:translate(-50%,-65px) scale(1.12)}}
#clear{display:none;position:absolute;z-index:40;inset:0;background:rgba(224,207,171,.88);align-items:center;justify-content:center;text-align:center;color:#111}
#clear.open{display:flex}.clearCard{width:min(86vw,350px);padding:20px 14px;border:3px solid #111;border-radius:16px;background:rgba(235,220,187,.97);box-shadow:5px 5px 0 #111}.clearTitle{font-size:28px;font-weight:900}.clearText{font-size:13px;margin:6px 0 14px}
@media(max-width:430px){#character{height:min(54dvh,450px);max-width:69vw;bottom:4dvh}#top{left:8px;right:8px}#shopButton{width:56px;height:56px;right:8px}}
@media(max-height:650px){#character{height:43dvh;bottom:4dvh}#shopButton{width:52px;height:52px}#progressArea{top:52px}}
</style>
</head>
<body>
<div id="game">
<div id="shade"></div>
<div id="top">
<div class="info"><div id="stageTitle"></div></div>
<div id="moneyArea" class="info"><div id="moneyLabel">보유 금액</div><div id="money">0원</div><div id="clickIncome">터치 +1,000원</div></div>
</div>
<img id="character" alt="캐릭터">
<div id="progressArea">
<div id="progressText"><span id="progressNow">0원</span><span id="progressGoal">목표 1,000,000원</span></div>
<div id="bar"><div id="fill"></div></div>
<div id="notice"></div>
</div>
<button id="shopButton" type="button">상점</button>
<div id="shop">
<div id="shopHead"><div id="shopTitle">상점</div><button id="closeShop" type="button">×</button></div>
<div class="item"><div class="itemName">돈 증가</div><div class="itemDesc">터치 1회당 벌리는 돈 +1,000원</div><div class="itemRow"><span class="level" id="moneyLevel">Lv.0</span><button class="action" id="buyMoney" type="button"></button></div></div>
<div class="item">
    <div class="itemName">인생역전</div>
    <div class="itemDesc">5,000원으로 5회 추첨 · 1등 0.2% / 2등 0.8% / 3등 1%</div>
    <div class="itemRow"><span class="level">5회 묶음</span><button class="action" id="buyLottery" type="button">5,000원</button></div>
    <div id="lotteryResult"></div>
  </div>

  <div class="item"><div class="itemName">클릭 더블</div><div class="itemDesc">Lv.1부터 ×2, 이후 업그레이드마다 ×2</div><div class="itemRow"><span class="level" id="doubleLevel">미구매</span><button class="action" id="buyDouble" type="button"></button></div></div>
<button id="reset" type="button">게임 초기화</button>
</div>
<div id="clear"><div class="clearCard"><div class="clearTitle">탈출 성공</div><div class="clearText">12억 5천만 원을 모아 최종 탈출했습니다</div><button class="action" id="clearReset" type="button">처음부터 다시</button></div></div>
</div>
<script>
const STAGES=__STAGES__;
const BACKGROUNDS=__BACKGROUNDS__;
const CHARACTERS=__CHARACTERS__;
const $=id=>document.getElementById(id);
const game=$("game"), character=$("character"), shop=$("shop"), shopButton=$("shopButton");
let saved=null;
try{saved=JSON.parse(localStorage.getItem("beggar_rpg_save")||"null")}catch(e){}
let money=saved?.money??0, stage=saved?.stage??0, moneyLevel=saved?.moneyLevel??0, doubleLevel=saved?.doubleLevel??0, cleared=saved?.cleared??false, lotteryResult=saved?.lotteryResult??"";
function fmt(n){return Math.floor(n).toLocaleString("ko-KR")+"원"}
function cost(l){return Math.floor(1000*Math.pow(1.5,l))}
function moneyBonus(){
  if(moneyLevel<=0) return 1000;
  return 1000 + Math.floor((moneyLevel-1)/5)*500;
}
function doubleMultiplier(){
  return Math.pow(2,doubleLevel);
}
function gainPerTouch(){
  return moneyBonus()*doubleMultiplier();
}
function save(){localStorage.setItem("beggar_rpg_save",JSON.stringify({money,stage,moneyLevel,doubleLevel,cleared,lotteryResult}))}
function render(){
 const s=STAGES[stage];
 game.style.backgroundImage=`url("${BACKGROUNDS[stage]}")`;
 character.src=CHARACTERS[stage];
 $("stageTitle").textContent=s.name; $("money").textContent=fmt(money);
 const gain=gainPerTouch(); $("clickIncome").textContent="터치 +"+fmt(gain);
 $("progressNow").textContent=fmt(money); $("progressGoal").textContent="목표 "+fmt(s.goal); $("fill").style.width=Math.min(100,money/s.goal*100)+"%";
 $("moneyLevel").textContent="Lv."+moneyLevel+" · +"+fmt(moneyBonus());
 $("buyMoney").textContent="구매 "+fmt(cost(moneyLevel));
 $("doubleLevel").textContent="Lv."+doubleLevel+" · ×"+doubleMultiplier();
 $("buyDouble").textContent="구매 "+fmt(cost(doubleLevel));
 $("buyDouble").disabled=false;
 if($("lotteryResult")) $("lotteryResult").textContent=lotteryResult;
 $("clear").classList.toggle("open",cleared);
}
function checkStage(){
 while(stage<4 && money>=STAGES[stage].goal){stage++; $("notice").textContent="다음 스테이지로 이동!"}
 if(stage===4 && money>=STAGES[4].goal){cleared=true; $("notice").textContent=""}
}
let audioCtx=null;
function playCoin(){
 try{
   const AC=window.AudioContext||window.webkitAudioContext; if(!AC)return;
   if(!audioCtx) audioCtx=new AC();
   if(audioCtx.state==="suspended") audioCtx.resume();
   const o=audioCtx.createOscillator(), g=audioCtx.createGain(), t=audioCtx.currentTime;
   o.type="sine"; o.frequency.setValueAtTime(900,t); o.frequency.exponentialRampToValueAtTime(1400,t+0.055);
   g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(0.20,t+0.006); g.gain.exponentialRampToValueAtTime(0.0001,t+0.13);
   o.connect(g); g.connect(audioCtx.destination); o.start(t); o.stop(t+0.14);
 }catch(e){}
}
function earn(ev){
 // 상점과 상점 버튼 영역만 돈 벌기에서 제외
 if(ev.target.closest("#shop,#shopButton")) return;
 if(cleared) return;
 if(ev.pointerType==="mouse" && ev.button!==0) return;
 ev.preventDefault();
 const gain=gainPerTouch(); money+=gain;
 const r=game.getBoundingClientRect();
 const x=Math.max(18,Math.min(r.width-18,ev.clientX-r.left));
 const y=Math.max(18,Math.min(r.height-25,ev.clientY-r.top));
 const f=document.createElement("div");
 f.className="float"; f.textContent="+"+fmt(gain); f.style.left=x+"px"; f.style.top=y+"px";
 game.appendChild(f); setTimeout(()=>f.remove(),760);
 playCoin(); checkStage(); save(); render();
}
// 게임 화면 전체에서 터치 가능: 위쪽/아래쪽/캐릭터 위도 모두 포함
window.addEventListener("pointerdown",earn,{passive:false});
shopButton.addEventListener("pointerdown",e=>{e.stopPropagation();e.preventDefault();shop.classList.toggle("open")},{passive:false});
$("closeShop").addEventListener("pointerdown",e=>{e.stopPropagation();e.preventDefault();shop.classList.remove("open")},{passive:false});
$("buyMoney").addEventListener("pointerdown",e=>{e.stopPropagation();e.preventDefault();const c=cost(moneyLevel);if(money<c){$("notice").textContent="돈이 부족합니다";return}money-=c;moneyLevel++;$("notice").textContent="돈 증가 업그레이드 완료";save();render()},{passive:false});
$("buyDouble").addEventListener("pointerdown",e=>{e.stopPropagation();e.preventDefault();const c=cost(doubleLevel);if(money<c){$("notice").textContent="돈이 부족합니다";return}money-=c;doubleLevel++;$("notice").textContent="클릭 더블 업그레이드 완료";save();render()},{passive:false});
function lottery(){
  const c=5000;
  if(money<c){
    $("notice").textContent="인생역전은 5,000원이 필요합니다";
    return;
  }

  money-=c;

  let total=0;
  let results=[];

  for(let i=0;i<5;i++){
    const r=Math.random()*100;

    if(r<0.2){
      total+=500000000;
      results.push("1등 +5억");
    }else if(r<1.0){
      total+=5000000;
      results.push("2등 +500만원");
    }else if(r<2.0){
      total+=10000;
      results.push("3등 +1만원");
    }else{
      results.push("꽝");
    }
  }

  money+=total;
  lotteryResult="최근 결과: "+results.join(" / ")+" · 총 "+fmt(total);
  $("notice").textContent=total>0?"인생역전 당첨!":"이번에는 꽝입니다";

  checkStage();
  save();
  render();
}

function resetGame(){money=0;stage=0;moneyLevel=0;doubleLevel=0;cleared=false;lotteryResult="";$("notice").textContent="";shop.classList.remove("open");save();render()}
$("buyLottery").addEventListener("pointerdown",e=>{
  e.stopPropagation();
  e.preventDefault();
  lottery();
},{passive:false});

$("reset").addEventListener("pointerdown",e=>{e.stopPropagation();e.preventDefault();resetGame()},{passive:false});
$("clearReset").addEventListener("pointerdown",e=>{e.stopPropagation();e.preventDefault();resetGame()},{passive:false});
render();
</script>
</body>
</html>'''

html = html.replace("__STAGES__", json.dumps([
    {"name":"STAGE 1. 시골","goal":1_000_000},
    {"name":"STAGE 2. 인도","goal":5_000_000},
    {"name":"STAGE 3. 서울역","goal":50_000_000},
    {"name":"STAGE 4. 반지하","goal":250_000_000},
    {"name":"STAGE 5. 지방 도시의 아파트","goal":1_250_000_000}
], ensure_ascii=False))
html = html.replace("__BACKGROUNDS__", stage_images_json)
html = html.replace("__CHARACTERS__", character_images_json)

components.html(html, height=700, scrolling=False)
