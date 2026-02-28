(function(){const a=document.createElement("link").relList;if(a&&a.supports&&a.supports("modulepreload"))return;for(const t of document.querySelectorAll('link[rel="modulepreload"]'))r(t);new MutationObserver(t=>{for(const s of t)if(s.type==="childList")for(const n of s.addedNodes)n.tagName==="LINK"&&n.rel==="modulepreload"&&r(n)}).observe(document,{childList:!0,subtree:!0});function e(t){const s={};return t.integrity&&(s.integrity=t.integrity),t.referrerPolicy&&(s.referrerPolicy=t.referrerPolicy),t.crossOrigin==="use-credentials"?s.credentials="include":t.crossOrigin==="anonymous"?s.credentials="omit":s.credentials="same-origin",s}function r(t){if(t.ep)return;t.ep=!0;const s=e(t);fetch(t.href,s)}})();const we="modulepreload",Se=function(i){return"/"+i},ie={},ue=function(a,e,r){let t=Promise.resolve();if(e&&e.length>0){let n=function(f){return Promise.all(f.map(M=>Promise.resolve(M).then(m=>({status:"fulfilled",value:m}),m=>({status:"rejected",reason:m}))))};document.getElementsByTagName("link");const u=document.querySelector("meta[property=csp-nonce]"),o=(u==null?void 0:u.nonce)||(u==null?void 0:u.getAttribute("nonce"));t=n(e.map(f=>{if(f=Se(f),f in ie)return;ie[f]=!0;const M=f.endsWith(".css"),m=M?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${f}"]${m}`))return;const p=document.createElement("link");if(p.rel=M?"stylesheet":we,M||(p.as="script"),p.crossOrigin="",p.href=f,o&&p.setAttribute("nonce",o),document.head.appendChild(p),M)return new Promise((v,P)=>{p.addEventListener("load",v),p.addEventListener("error",()=>P(new Error(`Unable to preload CSS for ${f}`)))})}))}function s(n){const u=new Event("vite:preloadError",{cancelable:!0});if(u.payload=n,window.dispatchEvent(u),!u.defaultPrevented)throw n}return t.then(n=>{for(const u of n||[])u.status==="rejected"&&s(u.reason);return a().catch(s)})},de=[{year:-5e3,title:"Before Creation",type:"planetary",phase:"before-creation"},{year:-4077,title:"Proto-Saturn joins Sun's orbit — Golden Age begins",type:"planetary",phase:"golden-age"},{year:-3147,title:"Golden Age ends violently — collinear configuration breaks",type:"planetary",phase:"dark-age"},{year:-3067,title:"Planets are at war — Jupiter assaults Saturn",type:"planetary",phase:"dark-age"},{year:-2860,title:"Non-linear 'Round Table' orbit stabilizes",type:"planetary",phase:"dark-age"},{year:-2349,title:"Jupiter disappears — Venus attacks Earth (Deluge)",type:"planetary",phase:"dark-age"},{year:-2193,title:"Earth leaves last Absu layer — Jupiter consumes Venus",type:"planetary",phase:"dark-age"},{year:-1936,title:"Sodom & Gomorrah destroyed by Mars",type:"planetary",phase:"dark-age"},{year:-1492,title:"Passover of Comet Venus — Exodus",type:"planetary",phase:"dark-age"},{year:-1442,title:"Sun stands still for Joshua",type:"planetary",phase:"dark-age"},{year:-806,title:"Mars, Earth, Mercury finalize orbits",type:"planetary",phase:"dark-age"},{year:-670,title:"Priori-Mars loses outer shell — Iron Age begins",type:"planetary",phase:"dark-age"},{year:-684,title:"Solar system becomes stable",type:"planetary",phase:"stability"},{year:-670,endYear:1053,title:"The Blip: 7th c. BCE to 10th c. CE never occurred (Fomenko)",type:"blip",phase:"blip"},{year:1053,title:"'Year of our Lord' Deception — 1053-year shift",type:"map",lat:41.01,lng:28.98,chapter:"05",phase:"empire-formation"},{year:1053,title:"Deep State centralizes world religion at Jerusalem",type:"map",lat:31.77,lng:35.23,chapter:"05",phase:"empire-formation"},{year:1152,title:"Historical Christ born in Crimea",type:"map",lat:44.95,lng:34.1,chapter:"06",phase:"empire-formation"},{year:1185,title:"Historical Christ crucified in Istanbul",type:"map",lat:41.01,lng:28.98,chapter:"06",phase:"empire-formation"},{year:1196,title:"First Crusade / Trojan War (revenge for Christ)",type:"map",lat:39.96,lng:26.24,chapter:"06",phase:"empire-formation"},{year:1200,title:"Russian Horde 'Tartarian' Empire emerges",type:"map",lat:55.75,lng:37.62,chapter:"07",phase:"empire-formation"},{year:1258,title:"Historical Christ dies",type:"map",lat:41.01,lng:28.98,chapter:"07",phase:"empire-formation"},{year:1285,title:"First Olympic Games",type:"map",lat:37.64,lng:21.63,chapter:"07",phase:"empire-formation"},{year:1300,title:"Great Expansion of Mongol-Slavic Horde",type:"map",lat:55.75,lng:37.62,chapter:"08",phase:"peak-empire"},{year:1380,title:"Battle of Kulikovo — Giants defeated",type:"map",lat:53.67,lng:38.67,chapter:"08",phase:"peak-empire"},{year:1421,title:"Meteorite falls on Yaroslavl",type:"map",lat:57.63,lng:39.87,chapter:"09",phase:"fragmentation"},{year:1431,title:"Jeanne d'Arc executed (Fomenko: ~1580)",type:"map",lat:49.44,lng:1.1,chapter:"09",phase:"fragmentation"},{year:1453,title:"Fall of Czar-Grad (Constantinople)",type:"map",lat:41.01,lng:28.98,chapter:"09",phase:"fragmentation"},{year:1455,title:"Gutenberg Bible translated into Latin",type:"map",lat:49.99,lng:8.27,chapter:"09",phase:"fragmentation"},{year:1486,title:"Revelation of the coming Apocalypse",type:"map",lat:41.9,lng:12.5,chapter:"09",phase:"fragmentation"},{year:1492,title:"The Apocalypse Crusade",type:"map",lat:37.39,lng:-5.98,chapter:"09",phase:"fragmentation"},{year:1517,title:"Protestant Reformation begins",type:"map",lat:51.87,lng:12.64,chapter:"10",phase:"religious-schism"},{year:1523,title:"Jesuits 'Pilgrimage' to Palestine",type:"map",lat:31.77,lng:35.23,chapter:"10",phase:"religious-schism"},{year:1542,title:"The Holy Inquisition",type:"map",lat:41.9,lng:12.5,chapter:"10",phase:"religious-schism"},{year:1548,title:"Jesuits reach Africa",type:"map",lat:9.03,lng:38.74,chapter:"10",phase:"religious-schism"},{year:1552,title:"Khazar Rebellion in Rus-Horde Empire",type:"map",lat:55.79,lng:49.11,chapter:"10",phase:"religious-schism"},{year:1565,title:"Oprichnina coup (Romanov dynasty)",type:"map",lat:55.75,lng:37.62,chapter:"10",phase:"religious-schism"},{year:1582,title:"Gregorian Calendar introduced",type:"map",lat:41.9,lng:12.5,chapter:"10",phase:"religious-schism"},{year:1611,title:"King James Bible published",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1613,title:"Romanov dynasty takes the throne",type:"map",lat:55.75,lng:37.62,chapter:"11",phase:"romanov-split"},{year:1618,title:"Thirty Years War begins (Horde provinces vs Vatican)",type:"map",lat:50.08,lng:14.44,chapter:"11",phase:"romanov-split"},{year:1627,title:"Deep State erases Russian Empire from chronology",type:"map",lat:55.75,lng:37.62,chapter:"11",phase:"romanov-split"},{year:1642,title:"English Civil War begins",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1648,title:"Cossack-Polish War — ethnic cleansing in Ukraine",type:"map",lat:50.45,lng:30.52,chapter:"11",phase:"romanov-split"},{year:1664,title:"Great Comet of 1664",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1666,title:"London burns / Sabbatean crisis / Apocalypse of 1666",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1694,title:"Bank of England — central banking solidified",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1718,title:"Secret Society of Jesus goes public",type:"map",lat:51.51,lng:-.13,chapter:"12",phase:"collapse"},{year:1773,title:"Pugachev Rebellion — Final Tartary vs Romanov war",type:"map",lat:51.67,lng:55.1,chapter:"12",phase:"collapse"},{year:1774,title:"Carbon-14 spike / MudFlood begins",type:"map",lat:55.75,lng:37.62,chapter:"12",phase:"collapse"},{year:1803,title:"Napoleonic Wars begin",type:"map",lat:48.86,lng:2.35,chapter:"13",phase:"post-horde"},{year:1812,title:"Napoleon invades Russia",type:"map",lat:55.75,lng:37.62,chapter:"13",phase:"post-horde"},{year:1840,title:"Ecliptic pathway of the Absu last seen",type:"map",lat:55.75,lng:37.62,chapter:"13",phase:"post-horde"},{year:1848,title:"Battle for Communism's Soul: Marx vs Kinkel",type:"map",lat:50.94,lng:6.96,chapter:"13",phase:"post-horde"},{year:1883,title:"Hijacking of Communism",type:"map",lat:51.51,lng:-.13,chapter:"13",phase:"post-horde"},{year:1917,title:"Bolshevik Revolution",type:"map",lat:59.93,lng:30.32,chapter:"14",phase:"modern"}],T=[{id:"pre-empire",label:"No Empires / No Borders",yearStart:1053,yearEnd:1149,color:"#888888",opacity:.1},{id:"empire-formation",label:"Rus-Horde Formation",yearStart:1150,yearEnd:1299,color:"#c62828",opacity:.3},{id:"peak-empire",label:"Great Tartary — Peak Expansion",yearStart:1300,yearEnd:1399,color:"#b71c1c",opacity:.45},{id:"fragmentation",label:"Regional Fragmentation — Ottoman/Spain/Habsburg",yearStart:1400,yearEnd:1499,color:"#e65100",opacity:.35},{id:"religious-schism",label:"Protestant vs Orthodox Schism",yearStart:1500,yearEnd:1599,color:"#f57f17",opacity:.35},{id:"romanov-split",label:"Romanov Takeover — Empire Fractures",yearStart:1600,yearEnd:1699,color:"#ff6f00",opacity:.3},{id:"collapse",label:"Final Collapse — Pugachev / MudFlood",yearStart:1700,yearEnd:1799,color:"#4e342e",opacity:.3},{id:"post-horde",label:"Post-Horde — Nation-States Emerge",yearStart:1800,yearEnd:1899,color:"#37474f",opacity:.2},{id:"modern",label:"Modern Borders",yearStart:1900,yearEnd:2026,color:"#263238",opacity:.15}],oe=[{id:"before-creation",yearStart:-5e3,yearEnd:-4077,label:"Before Creation",description:"Chaotic plasma environment. Saturn coalescing. Proto-configuration forming.",saturn:{glow:.3,rings:!1,position:[0,2,0]},venus:null,mars:null,earth:null,skyColor:"#1a0a2e"},{id:"golden-age",yearStart:-4077,yearEnd:-3147,label:"Golden Age — Collinear Configuration",description:"Saturn-Venus-Mars-Earth aligned. Tree of Life visible. Northern: Wheel of Heaven. Southern: Petroglyph figures.",saturn:{glow:1,rings:!1,position:[0,4,0],color:"#ffcc00"},venus:{type:"plasmoid",points:8,position:[0,2,0],color:"#ffffff"},mars:{type:"solid",position:[0,.5,0],color:"#cc3300"},earth:{position:[0,-1.5,0],color:"#3366cc"},skyColor:"#0d1b4a",yearLength:225},{id:"breakup",yearStart:-3147,yearEnd:-3067,label:"Collinear Configuration Breaks Apart",description:"All 9 planets break from configuration. Exit Saturn's plasma sheath.",saturn:{glow:.6,rings:!1,position:[0,5,0]},venus:{type:"plasmoid",points:6,position:[2,3,1],color:"#ffffff"},mars:{type:"solid",position:[-1,1,2],color:"#cc3300"},earth:{position:[-3,-1,-2],color:"#3366cc"},skyColor:"#2d0a0a",chaotic:!0},{id:"round-table",yearStart:-3067,yearEnd:-2349,label:"Non-Linear 'Round Table' — Jupiter Dominates",description:"Jupiter's 'Round Table' configuration. Planets in circular mini-orbit around Sun.",saturn:{glow:.3,rings:!1,position:[3,2,0]},venus:{type:"comet",position:[-2,1,3],color:"#ffeeaa"},mars:{type:"solid",position:[1,0,-2],color:"#cc3300"},earth:{position:[-1,-1,1],color:"#3366cc"},jupiter:{type:"dominant",position:[0,3,0],color:"#cc9944"},skyColor:"#1a0505",yearLength:273},{id:"deluge",yearStart:-2349,yearEnd:-2193,label:"The Deluge — Jupiter Disappears, Venus Attacks",description:"Jupiter disappears. Venus attacks Earth. Catastrophic flooding.",saturn:{glow:.2,rings:!1,position:[5,3,0]},venus:{type:"comet",position:[.5,.5,0],color:"#ff4444",threatening:!0},mars:{type:"solid",position:[2,-1,3],color:"#cc3300"},earth:{position:[0,0,0],color:"#3366cc",flooding:!0},skyColor:"#330000",yearLength:273},{id:"post-deluge",yearStart:-2193,yearEnd:-1492,label:"Post-Deluge — Destabilization Continues",description:"Jupiter consumes Venus. Sodom & Gomorrah. Configuration widening.",saturn:{glow:.15,rings:!1,position:[6,4,0]},venus:{type:"consumed",position:[3,3,0]},mars:{type:"solid",position:[.5,0,-1],color:"#cc3300",closeApproach:!0},earth:{position:[0,0,0],color:"#3366cc"},skyColor:"#1a0505",yearLength:273},{id:"venus-returns",yearStart:-1492,yearEnd:-806,label:"Venus Returns as Comet — Exodus",description:"Passover of Comet Venus. Venus and Mars tethered as 'the dragon'.",saturn:{glow:.1,rings:!1,position:[8,5,0]},venus:{type:"comet",position:[-1,1,0],color:"#ffaa00"},mars:{type:"solid",position:[-.5,.8,0],color:"#cc3300",tetheredToVenus:!0},earth:{position:[0,0,0],color:"#3366cc"},skyColor:"#0a0a1a",yearLength:290},{id:"stabilization",yearStart:-806,yearEnd:-670,label:"Orbits Finalize — Mars Loses Outer Shell",description:"Mars, Earth, Mercury move to final orbits. Iron Age begins.",saturn:{glow:.08,rings:!0,position:[10,6,0]},venus:{type:"planet",position:[-3,0,0],color:"#ffcc88"},mars:{type:"solid",position:[2,0,0],color:"#cc3300",shedding:!0},earth:{position:[0,0,0],color:"#3366cc"},skyColor:"#0a1a2a",yearLength:350},{id:"modern-solar",yearStart:-670,yearEnd:1053,label:"Modern Solar System — Phantom Period (The Blip)",description:"Solar system stable. 7th c. BCE to 10th c. CE is phantom time per Fomenko.",saturn:{glow:.05,rings:!0,position:[12,7,0],color:"#ccaa66"},venus:{type:"planet",position:[-4,0,0],color:"#ffcc88"},mars:{type:"planet",position:[3,0,0],color:"#cc3300"},earth:{position:[0,0,0],color:"#3366cc"},skyColor:"#0a1a3a",yearLength:365}];function J(i){return i<0?`${Math.abs(i)} BCE`:`${i} CE`}function xe(i,a,e,r=25){return i.filter(t=>e==="map"?t.type==="map":t.type==="planetary"||t.type==="blip").filter(t=>Math.abs(t.year-a)<=r).sort((t,s)=>t.year-s.year)}let z=null;const Ce="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png";async function Pe(i,a){z||(z=(await ue(async()=>{const{default:m}=await import("./leaflet-src-CzM8vlq-.js").then(p=>p.l);return{default:m}},[])).default);const e=z.map(i,{center:[48,40],zoom:4,minZoom:2,maxZoom:10,zoomControl:!0,attributionControl:!1});z.tileLayer(Ce,{subdomains:"abcd",maxZoom:19}).addTo(e);const r=JSON.parse(a),t={},s=[];let n=1053;r.features.forEach(m=>{const p=m.properties,v=z.geoJSON(m,{style:()=>({color:se(p.phase),weight:2,opacity:0,fillColor:se(p.phase),fillOpacity:0,dashArray:p.subRegion?"5,5":null})});v.bindTooltip(p.label||p.name,{className:"empire-tooltip",direction:"center",permanent:!1}),v.addTo(e),t[p.name]={layer:v,props:p}}),de.filter(m=>m.type==="map"&&m.lat).forEach(m=>{const p=z.divIcon({className:"pulse-marker",iconSize:[12,12]}),v=z.marker([m.lat,m.lng],{icon:p,opacity:0});v.bindPopup(`<div class="event-popup">
        <h3>${m.title}</h3>
        <p class="year">${J(m.year)}</p>
      </div>`,{maxWidth:250}),v.addTo(e),s.push({marker:v,evt:m})});function o(m){n=m,Object.values(t).forEach(({layer:p,props:v})=>{const P=m>=v.yearStart&&m<=v.yearEnd,I=T.find(V=>V.id===v.phase);let $=0;if(P){const V=v.yearEnd-v.yearStart,K=m-v.yearStart,Q=v.yearEnd-m,Y=Math.min(50,V*.1),X=Math.min(1,K/Y),R=Math.min(1,Q/Y);$=Math.min(X,R)*(I?I.opacity:.3)}p.setStyle({opacity:P?.7:0,fillOpacity:$})}),s.forEach(({marker:p,evt:v})=>{const P=Math.abs(v.year-m)<=10,I=v.year<=m;p.setOpacity(I?P?1:.3:0)})}function f(){const m=T.find(p=>n>=p.yearStart&&n<=p.yearEnd);return m?m.label:""}function M(){e.remove()}return{map:e,setYear:o,getPhaseLabel:f,destroy:M}}function se(i){const a=T.find(e=>e.id===i);return a?a.color:"#888"}let d=null;const O=-3147,E=.8,L={R:10,period:1,jupiter:{dist:1.5},saturn:{dist:3.5},venus:{dist:5.5},mars:{dist:7},earth:{dist:8.5},mercury:{dist:10},neptune:{dist:11.5},uranus:{dist:13}},w={sunPos:[-10,-3,0],saturn:{rx:5,ry:3.5,tilt:.2,period:10},venus:{rx:3.5,ry:2,tilt:.5,period:.615},mars:{rx:3,ry:2.5,tilt:-.3,period:1.88},earth:{rx:2.2,ry:1.5,tilt:-.1,period:1},mercury:{rx:1,ry:.8,tilt:.4,period:.24},neptune:{rx:6.5,ry:4,tilt:-.2,period:164},uranus:{rx:6,ry:3.8,tilt:.6,period:84}},S={mercury:{r:2,period:.24},venus:{r:3.5,period:.615},earth:{r:5,period:1},mars:{r:7,period:1.88},jupiter:{r:10,period:11.86},saturn:{r:13,period:29.46},uranus:{r:16,period:84},neptune:{r:19,period:164}};async function ke(i){d||(d=await ue(()=>import("./three.module-BtCAaDxU.js"),[]));const a=new d.Scene,e=new d.PerspectiveCamera(60,i.clientWidth/i.clientHeight,.1,1e3);e.position.set(0,10,25),e.lookAt(0,2,0);const r=new d.WebGLRenderer({canvas:i,antialias:!0,alpha:!0});r.setSize(i.clientWidth,i.clientHeight),r.setPixelRatio(Math.min(window.devicePixelRatio,2)),r.toneMapping=d.ACESFilmicToneMapping,r.toneMappingExposure=1.4,a.add(new d.AmbientLight(8952251,1.4));const t=new d.PointLight(16777164,3,120);t.position.set(0,0,0),a.add(t);const s=new d.DirectionalLight(11189196,.6);s.position.set(0,5,15),a.add(s);const n={};Be(a,n,d),je(a,n,d),Ge(a,n,d),Oe(a,n,d),Fe(a,n,d),ze(a,n,d),Ne(a,n,d),Ve(a,n,d),_e(a,n,d),De(a,n,d);const u=$e(a,d);Je(a,d);const o={};o.sun=A("SUN","#ffffaa",d),o.saturn=A("SATURN","#ff8833",d),o.venus=A("VENUS","#33ff77",d),o.mars=A("MARS","#ff6644",d),o.earth=A("EARTH","#66aaff",d),o.jupiter=A("JUPITER","#ffaa44",d),o.mercury=A("MERCURY","#bbaa88",d),o.neptune=A("NEPTUNE","#4466ff",d),o.uranus=A("URANUS","#66dddd",d),o.moon=A("MOON","#cccccc",d),Object.values(o).forEach(c=>a.add(c));const f={};f.collinear=Le(a,d),f.roundTable=Ie(a,d),f.modern=Ae(a,d),_(f.collinear,!1),_(f.roundTable,!1),_(f.modern,!1);let M=-5e3,m="",p={},v=null,P=new d.Vector3(0,10,25),I=new d.Vector3(0,2,0);const $=()=>{const c=i.clientWidth,l=i.clientHeight;!c||!l||(e.aspect=c/l,e.updateProjectionMatrix(),r.setSize(c,l))};window.addEventListener("resize",$);function V(){var c,l,b,y,h,g,x,C;v=requestAnimationFrame(V),n.sun&&(n.sun.rotation.y+=.001),(c=n.saturn)!=null&&c.visible&&(n.saturn.rotation.y+=.002),(l=n.venus)!=null&&l.visible&&(n.venus.rotation.y+=.005),(b=n.mars)!=null&&b.visible&&(n.mars.rotation.y+=.004),(y=n.earth)!=null&&y.visible&&(n.earth.rotation.y+=.003),(h=n.jupiter)!=null&&h.visible&&(n.jupiter.rotation.y+=.001),(g=n.mercury)!=null&&g.visible&&(n.mercury.rotation.y+=.006),(x=n.neptune)!=null&&x.visible&&(n.neptune.rotation.y+=.001),(C=n.uranus)!=null&&C.visible&&(n.uranus.rotation.y+=.001),u!=null&&u.visible&&(u.rotation.y+=5e-4,u.rotation.x=Math.sin(performance.now()*1e-4)*.05),e.position.lerp(P,.03),e.lookAt(I),B(o.sun,n.sun,1.4,e),B(o.saturn,n.saturn,1.8,e),B(o.venus,n.venus,.8,e),B(o.mars,n.mars,.7,e),B(o.earth,n.earth,.8,e),B(o.jupiter,n.jupiter,1.4,e),B(o.mercury,n.mercury,.5,e),B(o.neptune,n.neptune,.7,e),B(o.uranus,n.uranus,.7,e),B(o.moon,n.moon,.4,e),r.render(a,e)}V();function K(c){M=c;const l=oe.find(g=>c>=g.yearStart&&c<=g.yearEnd);if(!l)return;a.background=new d.Color(l.skyColor);const b=l.yearLength||365,y=c-l.yearStart;let h="none";if(l.id==="golden-age"?h="collinear":l.id==="round-table"?h="roundTable":(l.id==="stabilization"||l.id==="modern-solar")&&(h="modern"),h!==m&&(_(f.collinear,h==="collinear"),_(f.roundTable,h==="roundTable"),_(f.modern,h==="modern"),m=h,h==="collinear"?(P.set(0,18,22),I.set(0,0,0)):h==="roundTable"?(P.set(0,10,22),I.set(0,0,0)):h==="modern"?(P.set(0,30,30),I.set(0,0,0)):(P.set(0,8,22),I.set(0,1,0))),n.sun.visible=!0,o.sun.visible=!0,h==="collinear"?Q(y,l):h==="roundTable"?Y(y,l):h==="modern"?X(y,l):R(l),c>=O&&n.earth.visible){n.moon.visible=!0,o.moon.visible=!0;const g=Math.min(1,(c-O)/(-670-O)),x=10+(27.3-10)*g,F=(c-O)*b/x*Math.PI*2;n.moon.position.set(n.earth.position.x+E*Math.cos(F),n.earth.position.y+E*Math.sin(F)*.25,n.earth.position.z+E*Math.sin(F))}else n.moon.visible=!1,o.moon.visible=!1;if(u.visible=c<-806,u.visible&&(u.material.opacity=Math.max(0,Math.min(1,(-c-670)/2477))*.6),p={},h==="collinear"?(p.column=Math.abs(y),p.earth=Math.abs(y)):h==="roundTable"?(p.earth=Math.abs(y),p.venus=Math.abs(y/.615),p.mars=Math.abs(y/1.88),p.saturn=Math.abs(y/10),p.mercury=Math.abs(y/.24)):h==="modern"&&(p.mercury=Math.abs(y/.24),p.venus=Math.abs(y/.615),p.earth=Math.abs(y),p.mars=Math.abs(y/1.88),p.jupiter=Math.abs(y/11.86),p.saturn=Math.abs(y/29.46)),c>=O){const g=Math.min(1,(c-O)/(-670-O)),x=10+(27.3-10)*g;p.moon=Math.abs((c-O)*b/x)}}function Q(c,l){var x,C;const b=c/L.period*Math.PI*2,y=Math.cos(b),h=Math.sin(b);n.sun.position.set(0,0,0),t.position.set(0,0,0);const g=(F,U,re,Me)=>{Me?(F.visible=!0,U&&(U.visible=!0),F.position.set(y*re,0,h*re)):(F.visible=!1,U&&(U.visible=!1))};g(n.jupiter,o.jupiter,L.jupiter.dist,!0),g(n.saturn,o.saturn,L.saturn.dist,!0),n.saturnGlow.material.opacity=(((x=l.saturn)==null?void 0:x.glow)||.5)*.6,n.saturnRings.material.opacity=(C=l.saturn)!=null&&C.rings?.5:0,g(n.venus,o.venus,L.venus.dist,!!l.venus),g(n.mars,o.mars,L.mars.dist,!!l.mars),g(n.earth,o.earth,L.earth.dist,!!l.earth),g(n.mercury,o.mercury,L.mercury.dist,!0),g(n.neptune,o.neptune,L.neptune.dist,!0),g(n.uranus,o.uranus,L.uranus.dist,!0)}function Y(c,l){n.sun.position.set(...w.sunPos),t.position.set(...w.sunPos),n.jupiter.visible=!0,o.jupiter.visible=!0,n.jupiter.position.set(0,0,0);const b=(y,h,g,x)=>{if(!x){y.visible=!1,h&&(h.visible=!1);return}y.visible=!0,h&&(h.visible=!0);const C=c/g.period*Math.PI*2;y.position.set(g.rx*Math.cos(C),g.ry*Math.sin(C)*Math.cos(g.tilt),g.ry*Math.sin(C)*Math.sin(g.tilt))};b(n.saturn,o.saturn,w.saturn,!!l.saturn),l.saturn&&(n.saturnGlow.material.opacity=(l.saturn.glow||.3)*.6,n.saturnRings.material.opacity=l.saturn.rings?.5:0),b(n.venus,o.venus,w.venus,!!l.venus),b(n.mars,o.mars,w.mars,!!l.mars),b(n.earth,o.earth,w.earth,!!l.earth),b(n.mercury,o.mercury,w.mercury,!0),b(n.neptune,o.neptune,w.neptune,!0),b(n.uranus,o.uranus,w.uranus,!0)}function X(c,l){n.sun.position.set(0,0,0),t.position.set(0,0,0);const b=(y,h,g,x)=>{if(!x){y.visible=!1,h&&(h.visible=!1);return}y.visible=!0,h&&(h.visible=!0);const C=c/g.period*Math.PI*2;y.position.set(g.r*Math.cos(C),0,g.r*Math.sin(C))};b(n.mercury,o.mercury,S.mercury,!0),b(n.venus,o.venus,S.venus,!!l.venus),b(n.earth,o.earth,S.earth,!!l.earth),b(n.mars,o.mars,S.mars,!!l.mars),b(n.jupiter,o.jupiter,S.jupiter,!!l.jupiter),b(n.saturn,o.saturn,S.saturn,!!l.saturn),l.saturn&&(n.saturnGlow.material.opacity=(l.saturn.glow||.05)*.6,n.saturnRings.material.opacity=l.saturn.rings?.5:0),b(n.uranus,o.uranus,S.uranus,!0),b(n.neptune,o.neptune,S.neptune,!0)}function R(c){n.sun.position.set(0,-3,-5),t.position.set(0,-3,-5);const l=(b,y)=>{y&&b.position.lerp(new d.Vector3(y[0],y[1],y[2]),.05)};c.saturn&&(n.saturn.visible=!0,o.saturn.visible=!0,l(n.saturn,c.saturn.position),n.saturnGlow.material.opacity=(c.saturn.glow||.3)*.6,n.saturnRings.material.opacity=c.saturn.rings?.5:0),c.venus?(n.venus.visible=!0,o.venus.visible=!0,l(n.venus,c.venus.position)):(n.venus.visible=!1,o.venus.visible=!1),c.mars?(n.mars.visible=!0,o.mars.visible=!0,l(n.mars,c.mars.position)):(n.mars.visible=!1,o.mars.visible=!1),c.earth?(n.earth.visible=!0,o.earth.visible=!0,l(n.earth,c.earth.position)):(n.earth.visible=!1,o.earth.visible=!1),c.jupiter?(n.jupiter.visible=!0,o.jupiter.visible=!0,l(n.jupiter,c.jupiter.position)):(n.jupiter.visible=!1,o.jupiter.visible=!1),n.mercury.visible=!1,o.mercury.visible=!1,n.neptune.visible=!1,o.neptune.visible=!1,n.uranus.visible=!1,o.uranus.visible=!1}function ge(){const c=oe.find(l=>M>=l.yearStart&&M<=l.yearEnd);return c?{label:c.label,description:c.description}:{label:"",description:""}}function be(){return{...p}}function ve(){v&&cancelAnimationFrame(v),window.removeEventListener("resize",$),r.dispose()}return{setYear:K,getPhaseInfo:ge,getOrbitInfo:be,destroy:ve}}function A(i,a,e){const r=document.createElement("canvas"),t=r.getContext("2d");r.width=256,r.height=64,t.clearRect(0,0,r.width,r.height),t.font="bold 48px Arial, sans-serif",t.textAlign="center",t.textBaseline="middle",t.shadowColor="rgba(0,0,0,0.8)",t.shadowBlur=6,t.fillStyle=a,t.fillText(i,r.width/2,r.height/2);const s=new e.CanvasTexture(r);s.minFilter=e.LinearFilter;const n=new e.Sprite(new e.SpriteMaterial({map:s,transparent:!0,depthTest:!1}));return n.scale.set(2.5,.6,1),n.visible=!1,n}function B(i,a,e,r){!(i!=null&&i.visible)||!(a!=null&&a.visible)||(i.position.set(a.position.x,a.position.y+e,a.position.z),i.quaternion.copy(r.quaternion))}function ne(i,a,e,r){const t=new r.BufferGeometry().setFromPoints(i),s=new r.LineBasicMaterial({color:a,transparent:!0,opacity:e,depthWrite:!1});return new r.Line(t,s)}function _(i,a){Array.isArray(i)?i.forEach(e=>{e.visible=a}):i&&(i.visible=a)}function Le(i,a){const e=[];for(let t=0;t<=96;t++){const s=t/96*Math.PI*2;e.push(new a.Vector3(L.R*Math.cos(s),0,L.R*Math.sin(s)))}const r=ne(e,16746547,.3,a);return i.add(r),[r]}function Ie(i,a){const e=[],r=[{...w.saturn,color:16746547},{...w.venus,color:3407735},{...w.mars,color:16737860},{...w.earth,color:6728447},{...w.mercury,color:12298888},{...w.neptune,color:4482815},{...w.uranus,color:6741469}];for(const t of r){const s=[];for(let u=0;u<=80;u++){const o=u/80*Math.PI*2;s.push(new a.Vector3(t.rx*Math.cos(o),t.ry*Math.sin(o)*Math.cos(t.tilt),t.ry*Math.sin(o)*Math.sin(t.tilt)))}const n=ne(s,t.color,.25,a);i.add(n),e.push(n)}return e}function Ae(i,a){const e=[],r=[{r:S.mercury.r,color:12298888},{r:S.venus.r,color:3407735},{r:S.earth.r,color:6728447},{r:S.mars.r,color:16737860},{r:S.jupiter.r,color:16755268},{r:S.saturn.r,color:16746547},{r:S.uranus.r,color:6741469},{r:S.neptune.r,color:4482815}];for(const t of r){const s=[];for(let u=0;u<=96;u++){const o=u/96*Math.PI*2;s.push(new a.Vector3(t.r*Math.cos(o),0,t.r*Math.sin(o)))}const n=ne(s,t.color,.25,a);i.add(n),e.push(n)}return e}function G(i,a){const r=document.createElement("canvas");r.width=128,r.height=128;const t=r.getContext("2d"),s=new a.Color(i),n=Math.round(s.r*255),u=Math.round(s.g*255),o=Math.round(s.b*255),f=t.createRadialGradient(128/2,128/2,0,128/2,128/2,128/2);return f.addColorStop(0,`rgba(${n},${u},${o},1)`),f.addColorStop(.3,`rgba(${n},${u},${o},0.5)`),f.addColorStop(1,`rgba(${n},${u},${o},0)`),t.fillStyle=f,t.fillRect(0,0,128,128),new a.CanvasTexture(r)}function Be(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.8,32,32),new e.MeshStandardMaterial({color:16777164,emissive:16768324,emissiveIntensity:1.5,roughness:0}));i.add(r),a.sun=r;const t=new e.Sprite(new e.SpriteMaterial({map:G(16768324,e),color:16768324,transparent:!0,opacity:.7,blending:e.AdditiveBlending}));t.scale.set(5,5,1),r.add(t)}function je(i,a,e){const r=new e.Mesh(new e.SphereGeometry(1.2,32,32),new e.MeshStandardMaterial({color:16746547,emissive:13395490,emissiveIntensity:.8,roughness:.3}));i.add(r),a.saturn=r;const t=new e.Sprite(new e.SpriteMaterial({map:G(16746547,e),color:16746547,transparent:!0,opacity:.6,blending:e.AdditiveBlending}));t.scale.set(5,5,1),r.add(t),a.saturnGlow=t;const s=new e.Mesh(new e.RingGeometry(1.6,2.4,64),new e.MeshBasicMaterial({color:13412966,side:e.DoubleSide,transparent:!0,opacity:0}));s.rotation.x=Math.PI/2.3,r.add(s),a.saturnRings=s}function Ge(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.4,16,16),new e.MeshStandardMaterial({color:3407735,emissive:2280533,emissiveIntensity:1,roughness:0}));i.add(r),a.venus=r;const t=new e.Sprite(new e.SpriteMaterial({map:G(3407735,e),color:3407735,transparent:!0,opacity:.5,blending:e.AdditiveBlending}));t.scale.set(3,3,1),r.add(t),a.venusGlow=t}function Oe(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.35,16,16),new e.MeshStandardMaterial({color:16729122,emissive:13382400,emissiveIntensity:.6,roughness:.6,metalness:.2}));i.add(r),a.mars=r;const t=new e.Sprite(new e.SpriteMaterial({map:G(16729122,e),color:16729122,transparent:!0,opacity:.25,blending:e.AdditiveBlending}));t.scale.set(1.5,1.5,1),r.add(t)}function Fe(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.45,24,24),new e.MeshStandardMaterial({color:4491519,emissive:2245802,emissiveIntensity:.5,roughness:.4,metalness:.1}));i.add(r),a.earth=r;const t=new e.Sprite(new e.SpriteMaterial({map:G(4491519,e),color:4491519,transparent:!0,opacity:.2,blending:e.AdditiveBlending}));t.scale.set(1.8,1.8,1),r.add(t)}function ze(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.9,24,24),new e.MeshStandardMaterial({color:14527044,emissive:8939042,emissiveIntensity:.5,roughness:.5}));r.visible=!1,i.add(r),a.jupiter=r;const t=new e.Sprite(new e.SpriteMaterial({map:G(14527044,e),color:14527044,transparent:!0,opacity:.3,blending:e.AdditiveBlending}));t.scale.set(3,3,1),r.add(t)}function Ne(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.2,16,16),new e.MeshStandardMaterial({color:12298888,emissive:8943445,emissiveIntensity:.4,roughness:.7}));r.visible=!1,i.add(r),a.mercury=r;const t=new e.Sprite(new e.SpriteMaterial({map:G(12298888,e),color:12298888,transparent:!0,opacity:.2,blending:e.AdditiveBlending}));t.scale.set(1,1,1),r.add(t)}function Ve(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.5,20,20),new e.MeshStandardMaterial({color:4482815,emissive:2241450,emissiveIntensity:.5,roughness:.4}));r.visible=!1,i.add(r),a.neptune=r;const t=new e.Sprite(new e.SpriteMaterial({map:G(4482815,e),color:4482815,transparent:!0,opacity:.25,blending:e.AdditiveBlending}));t.scale.set(2,2,1),r.add(t)}function _e(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.5,20,20),new e.MeshStandardMaterial({color:6741469,emissive:4500138,emissiveIntensity:.5,roughness:.4}));r.visible=!1,i.add(r),a.uranus=r;const t=new e.Sprite(new e.SpriteMaterial({map:G(6741469,e),color:6741469,transparent:!0,opacity:.25,blending:e.AdditiveBlending}));t.scale.set(2,2,1),r.add(t)}function De(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.15,16,16),new e.MeshStandardMaterial({color:12303291,emissive:6710886,emissiveIntensity:.3,roughness:.8}));r.visible=!1,i.add(r),a.moon=r;const t=new e.Sprite(new e.SpriteMaterial({map:G(11184810,e),color:11184810,transparent:!0,opacity:.15,blending:e.AdditiveBlending}));t.scale.set(.6,.6,1),r.add(t)}function $e(i,a){const r=new Float32Array(6e3),t=new Float32Array(2e3*3);for(let o=0;o<2e3;o++){const f=Math.random()*Math.PI*2,M=Math.random()*Math.PI,m=6+Math.random()*3;r[o*3]=m*Math.sin(M)*Math.cos(f),r[o*3+1]=m*Math.cos(M),r[o*3+2]=m*Math.sin(M)*Math.sin(f),t[o*3]=.3+Math.random()*.3,t[o*3+1]=.1+Math.random()*.2,t[o*3+2]=.5+Math.random()*.5}const s=new a.BufferGeometry;s.setAttribute("position",new a.BufferAttribute(r,3)),s.setAttribute("color",new a.BufferAttribute(t,3));const n=new a.PointsMaterial({size:.08,vertexColors:!0,transparent:!0,opacity:.6,blending:a.AdditiveBlending,depthWrite:!1}),u=new a.Points(s,n);return i.add(u),u}function Je(i,a){const r=new Float32Array(15e3);for(let s=0;s<5e3;s++)r[s*3]=(Math.random()-.5)*200,r[s*3+1]=(Math.random()-.5)*200,r[s*3+2]=(Math.random()-.5)*200;const t=new a.BufferGeometry;t.setAttribute("position",new a.BufferAttribute(r,3)),i.add(new a.Points(t,new a.PointsMaterial({size:.1,color:16777215,transparent:!0,opacity:.6})))}const Ye=`{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Rus-Horde Core",
                "phase": "empire-formation",
                "yearStart": 1150,
                "yearEnd": 1775,
                "label": "Great Tartary / Mongol Empire",
                "fomenkoName": "Rus-Horde"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            30,
                            45
                        ],
                        [
                            35,
                            42
                        ],
                        [
                            40,
                            38
                        ],
                        [
                            45,
                            40
                        ],
                        [
                            50,
                            42
                        ],
                        [
                            55,
                            43
                        ],
                        [
                            60,
                            45
                        ],
                        [
                            70,
                            48
                        ],
                        [
                            80,
                            50
                        ],
                        [
                            90,
                            52
                        ],
                        [
                            100,
                            53
                        ],
                        [
                            110,
                            52
                        ],
                        [
                            120,
                            50
                        ],
                        [
                            130,
                            48
                        ],
                        [
                            135,
                            45
                        ],
                        [
                            130,
                            55
                        ],
                        [
                            120,
                            60
                        ],
                        [
                            110,
                            62
                        ],
                        [
                            100,
                            63
                        ],
                        [
                            90,
                            64
                        ],
                        [
                            80,
                            65
                        ],
                        [
                            70,
                            66
                        ],
                        [
                            60,
                            65
                        ],
                        [
                            50,
                            63
                        ],
                        [
                            45,
                            60
                        ],
                        [
                            40,
                            58
                        ],
                        [
                            35,
                            55
                        ],
                        [
                            30,
                            52
                        ],
                        [
                            28,
                            48
                        ],
                        [
                            30,
                            45
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Ottoman Region",
                "phase": "fragmentation",
                "yearStart": 1400,
                "yearEnd": 1922,
                "label": "Ottoman Empire (= Ataman/Horde Province)",
                "fomenkoName": "Ataman",
                "subRegion": true
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            20,
                            35
                        ],
                        [
                            25,
                            33
                        ],
                        [
                            30,
                            32
                        ],
                        [
                            35,
                            33
                        ],
                        [
                            40,
                            35
                        ],
                        [
                            42,
                            37
                        ],
                        [
                            40,
                            40
                        ],
                        [
                            35,
                            42
                        ],
                        [
                            30,
                            43
                        ],
                        [
                            27,
                            42
                        ],
                        [
                            25,
                            40
                        ],
                        [
                            22,
                            38
                        ],
                        [
                            20,
                            36
                        ],
                        [
                            20,
                            35
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Spain / Iberia",
                "phase": "fragmentation",
                "yearStart": 1400,
                "yearEnd": 1700,
                "label": "Spain (= Horde Colony per Fomenko)",
                "fomenkoName": "Horde Colony — Iberia",
                "subRegion": true
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10,
                            36
                        ],
                        [
                            -9,
                            37
                        ],
                        [
                            -8,
                            39
                        ],
                        [
                            -7,
                            41
                        ],
                        [
                            -5,
                            43
                        ],
                        [
                            -2,
                            43
                        ],
                        [
                            0,
                            42
                        ],
                        [
                            2,
                            42
                        ],
                        [
                            3,
                            40
                        ],
                        [
                            1,
                            38
                        ],
                        [
                            -1,
                            37
                        ],
                        [
                            -3,
                            36
                        ],
                        [
                            -5,
                            36
                        ],
                        [
                            -7,
                            36
                        ],
                        [
                            -10,
                            36
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Habsburg Territories",
                "phase": "fragmentation",
                "yearStart": 1450,
                "yearEnd": 1800,
                "label": "Habsburg / Holy Roman Empire",
                "fomenkoName": "Western Horde Province",
                "subRegion": true
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            5,
                            46
                        ],
                        [
                            8,
                            44
                        ],
                        [
                            12,
                            44
                        ],
                        [
                            15,
                            45
                        ],
                        [
                            17,
                            46
                        ],
                        [
                            20,
                            47
                        ],
                        [
                            22,
                            48
                        ],
                        [
                            20,
                            50
                        ],
                        [
                            18,
                            51
                        ],
                        [
                            15,
                            52
                        ],
                        [
                            12,
                            51
                        ],
                        [
                            10,
                            50
                        ],
                        [
                            7,
                            49
                        ],
                        [
                            5,
                            48
                        ],
                        [
                            5,
                            46
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Protestant Zone",
                "phase": "religious-schism",
                "yearStart": 1517,
                "yearEnd": 1700,
                "label": "Protestant Territories",
                "conflictType": "protestant-vs-orthodox",
                "subRegion": true
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            5,
                            52
                        ],
                        [
                            8,
                            50
                        ],
                        [
                            12,
                            49
                        ],
                        [
                            15,
                            50
                        ],
                        [
                            10,
                            55
                        ],
                        [
                            8,
                            56
                        ],
                        [
                            5,
                            55
                        ],
                        [
                            3,
                            54
                        ],
                        [
                            5,
                            52
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Eastern Orthodox Zone",
                "phase": "religious-schism",
                "yearStart": 1053,
                "yearEnd": 1700,
                "label": "Eastern Orthodox Territories",
                "conflictType": "protestant-vs-orthodox",
                "subRegion": true
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            25,
                            42
                        ],
                        [
                            30,
                            40
                        ],
                        [
                            35,
                            42
                        ],
                        [
                            40,
                            45
                        ],
                        [
                            45,
                            50
                        ],
                        [
                            50,
                            55
                        ],
                        [
                            45,
                            58
                        ],
                        [
                            40,
                            60
                        ],
                        [
                            35,
                            58
                        ],
                        [
                            30,
                            55
                        ],
                        [
                            28,
                            50
                        ],
                        [
                            25,
                            46
                        ],
                        [
                            25,
                            42
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Muscovy (Romanov Split)",
                "phase": "romanov-split",
                "yearStart": 1613,
                "yearEnd": 1917,
                "label": "Muscovy / Romanov Russia",
                "fomenkoName": "Romanov rebel state",
                "subRegion": true
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            28,
                            52
                        ],
                        [
                            32,
                            50
                        ],
                        [
                            38,
                            50
                        ],
                        [
                            42,
                            52
                        ],
                        [
                            48,
                            55
                        ],
                        [
                            50,
                            58
                        ],
                        [
                            48,
                            62
                        ],
                        [
                            42,
                            64
                        ],
                        [
                            36,
                            63
                        ],
                        [
                            32,
                            60
                        ],
                        [
                            30,
                            57
                        ],
                        [
                            28,
                            55
                        ],
                        [
                            28,
                            52
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "British Empire Zone",
                "phase": "romanov-split",
                "yearStart": 1583,
                "yearEnd": 1997,
                "label": "British Empire (Deep State Instrument)",
                "subRegion": true
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -8,
                            50
                        ],
                        [
                            -6,
                            50
                        ],
                        [
                            -5,
                            51
                        ],
                        [
                            -3,
                            52
                        ],
                        [
                            0,
                            53
                        ],
                        [
                            2,
                            52
                        ],
                        [
                            2,
                            51
                        ],
                        [
                            0,
                            50
                        ],
                        [
                            -2,
                            50
                        ],
                        [
                            -4,
                            49
                        ],
                        [
                            -6,
                            49
                        ],
                        [
                            -8,
                            50
                        ]
                    ]
                ]
            }
        }
    ]
}`;let N=1053,k="map",Z=!1,W=null,me=80,H=null,ee=null;const j=document.getElementById("timeline-slider"),ye=document.getElementById("btn-map"),he=document.getElementById("btn-3d"),te=document.getElementById("btn-play"),ae=document.getElementById("btn-pause"),Ue=document.getElementById("btn-reset"),le=document.getElementById("speed-select"),We=document.getElementById("map-view"),qe=document.getElementById("planet-view"),Ze=document.getElementById("map-year-display"),Ke=document.getElementById("map-phase-label"),Qe=document.getElementById("planet-year-display"),Xe=document.getElementById("planet-phase-label"),Re=document.getElementById("planet-description"),Ee=document.getElementById("event-feed"),Te=document.getElementById("timeline-markers");document.addEventListener("DOMContentLoaded",async()=>{H=await Pe(document.getElementById("map"),Ye),ee=await ke(document.getElementById("planet-canvas")),fe(),D(N),He()});function He(){ye.addEventListener("click",()=>pe("map")),he.addEventListener("click",()=>pe("3d")),j.addEventListener("input",()=>{D(parseInt(j.value,10))}),te.addEventListener("click",ce),ae.addEventListener("click",q),Ue.addEventListener("click",()=>{q(),D(k==="map"?1053:-5e3)}),le.addEventListener("change",()=>{me=parseInt(le.value,10),Z&&(q(),ce())})}function pe(i){k=i,ye.classList.toggle("active",k==="map"),he.classList.toggle("active",k==="3d"),We.classList.toggle("active",k==="map"),qe.classList.toggle("active",k==="3d"),k==="map"?(j.min=1053,j.max=2026,N<1053&&D(1053)):(j.min=-5e3,j.max=1053,N>1053&&D(-4077)),j.value=N,fe()}function D(i){if(N=i,j.value=i,k==="map")H.setYear(i),Ze.textContent=J(i),Ke.textContent=H.getPhaseLabel();else{ee.setYear(i);const a=ee.getPhaseInfo();Qe.textContent=J(i),Xe.textContent=a.label,Re.textContent=a.description}en(i)}function ce(){if(Z)return;Z=!0,te.style.display="none",ae.style.display="";const i=k==="map"?1:N<-3e3?10:5,a=k==="map"?2026:1053;W=setInterval(()=>{const e=N+i;if(e>a){q();return}D(e)},me)}function q(){Z=!1,te.style.display="",ae.style.display="none",W&&(clearInterval(W),W=null)}function en(i){const a=xe(de,i,k);Ee.innerHTML=a.map(e=>`<div class="event-item ${Math.abs(e.year-i)<=5?"active":""}">${J(e.year)} — ${e.title}</div>`).join("")}function fe(){const i=parseInt(j.min,10),a=parseInt(j.max,10),e=k==="map"?100:500,r=[];for(let t=i;t<=a;t+=e)r.push(`<span>${J(t)}</span>`);Te.innerHTML=r.join("")}
