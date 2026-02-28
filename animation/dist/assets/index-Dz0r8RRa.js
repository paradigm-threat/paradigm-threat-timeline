(function(){const a=document.createElement("link").relList;if(a&&a.supports&&a.supports("modulepreload"))return;for(const t of document.querySelectorAll('link[rel="modulepreload"]'))r(t);new MutationObserver(t=>{for(const s of t)if(s.type==="childList")for(const n of s.addedNodes)n.tagName==="LINK"&&n.rel==="modulepreload"&&r(n)}).observe(document,{childList:!0,subtree:!0});function e(t){const s={};return t.integrity&&(s.integrity=t.integrity),t.referrerPolicy&&(s.referrerPolicy=t.referrerPolicy),t.crossOrigin==="use-credentials"?s.credentials="include":t.crossOrigin==="anonymous"?s.credentials="omit":s.credentials="same-origin",s}function r(t){if(t.ep)return;t.ep=!0;const s=e(t);fetch(t.href,s)}})();const ke="modulepreload",Ie=function(i){return"/"+i},se={},me=function(a,e,r){let t=Promise.resolve();if(e&&e.length>0){let n=function(y){return Promise.all(y.map(M=>Promise.resolve(M).then(d=>({status:"fulfilled",value:d}),d=>({status:"rejected",reason:d}))))};document.getElementsByTagName("link");const m=document.querySelector("meta[property=csp-nonce]"),o=(m==null?void 0:m.nonce)||(m==null?void 0:m.getAttribute("nonce"));t=n(e.map(y=>{if(y=Ie(y),y in se)return;se[y]=!0;const M=y.endsWith(".css"),d=M?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${y}"]${d}`))return;const c=document.createElement("link");if(c.rel=M?"stylesheet":ke,M||(c.as="script"),c.crossOrigin="",c.href=y,o&&c.setAttribute("nonce",o),document.head.appendChild(c),M)return new Promise((g,P)=>{c.addEventListener("load",g),c.addEventListener("error",()=>P(new Error(`Unable to preload CSS for ${y}`)))})}))}function s(n){const m=new Event("vite:preloadError",{cancelable:!0});if(m.payload=n,window.dispatchEvent(m),!m.defaultPrevented)throw n}return t.then(n=>{for(const m of n||[])m.status==="rejected"&&s(m.reason);return a().catch(s)})},ye=[{year:-5e3,title:"Before Creation",type:"planetary",phase:"before-creation"},{year:-4077,title:"Proto-Saturn joins Sun's orbit — Golden Age begins",type:"planetary",phase:"golden-age"},{year:-3147,title:"Golden Age ends violently — collinear configuration breaks",type:"planetary",phase:"dark-age"},{year:-3067,title:"Planets are at war — Jupiter assaults Saturn",type:"planetary",phase:"dark-age"},{year:-2860,title:"Non-linear 'Round Table' orbit stabilizes",type:"planetary",phase:"dark-age"},{year:-2349,title:"Jupiter disappears — Venus attacks Earth (Deluge)",type:"planetary",phase:"dark-age"},{year:-2193,title:"Earth leaves last Absu layer — Jupiter consumes Venus",type:"planetary",phase:"dark-age"},{year:-1936,title:"Sodom & Gomorrah destroyed by Mars",type:"planetary",phase:"dark-age"},{year:-1492,title:"Passover of Comet Venus — Exodus",type:"planetary",phase:"dark-age"},{year:-1442,title:"Sun stands still for Joshua",type:"planetary",phase:"dark-age"},{year:-806,title:"Mars, Earth, Mercury finalize orbits",type:"planetary",phase:"dark-age"},{year:-670,title:"Priori-Mars loses outer shell — Iron Age begins",type:"planetary",phase:"dark-age"},{year:-684,title:"Solar system becomes stable",type:"planetary",phase:"stability"},{year:-670,endYear:1053,title:"The Blip: 7th c. BCE to 10th c. CE never occurred (Fomenko)",type:"blip",phase:"blip"},{year:1053,title:"'Year of our Lord' Deception — 1053-year shift",type:"map",lat:41.01,lng:28.98,chapter:"05",phase:"empire-formation"},{year:1053,title:"Deep State centralizes world religion at Jerusalem",type:"map",lat:31.77,lng:35.23,chapter:"05",phase:"empire-formation"},{year:1152,title:"Historical Christ born in Crimea",type:"map",lat:44.95,lng:34.1,chapter:"06",phase:"empire-formation"},{year:1185,title:"Historical Christ crucified in Istanbul",type:"map",lat:41.01,lng:28.98,chapter:"06",phase:"empire-formation"},{year:1196,title:"First Crusade / Trojan War (revenge for Christ)",type:"map",lat:39.96,lng:26.24,chapter:"06",phase:"empire-formation"},{year:1200,title:"Russian Horde 'Tartarian' Empire emerges",type:"map",lat:55.75,lng:37.62,chapter:"07",phase:"empire-formation"},{year:1258,title:"Historical Christ dies",type:"map",lat:41.01,lng:28.98,chapter:"07",phase:"empire-formation"},{year:1285,title:"First Olympic Games",type:"map",lat:37.64,lng:21.63,chapter:"07",phase:"empire-formation"},{year:1300,title:"Great Expansion of Mongol-Slavic Horde",type:"map",lat:55.75,lng:37.62,chapter:"08",phase:"peak-empire"},{year:1380,title:"Battle of Kulikovo — Giants defeated",type:"map",lat:53.67,lng:38.67,chapter:"08",phase:"peak-empire"},{year:1421,title:"Meteorite falls on Yaroslavl",type:"map",lat:57.63,lng:39.87,chapter:"09",phase:"fragmentation"},{year:1431,title:"Jeanne d'Arc executed (Fomenko: ~1580)",type:"map",lat:49.44,lng:1.1,chapter:"09",phase:"fragmentation"},{year:1453,title:"Fall of Czar-Grad (Constantinople)",type:"map",lat:41.01,lng:28.98,chapter:"09",phase:"fragmentation"},{year:1455,title:"Gutenberg Bible translated into Latin",type:"map",lat:49.99,lng:8.27,chapter:"09",phase:"fragmentation"},{year:1486,title:"Revelation of the coming Apocalypse",type:"map",lat:41.9,lng:12.5,chapter:"09",phase:"fragmentation"},{year:1492,title:"The Apocalypse Crusade",type:"map",lat:37.39,lng:-5.98,chapter:"09",phase:"fragmentation"},{year:1517,title:"Protestant Reformation begins",type:"map",lat:51.87,lng:12.64,chapter:"10",phase:"religious-schism"},{year:1523,title:"Jesuits 'Pilgrimage' to Palestine",type:"map",lat:31.77,lng:35.23,chapter:"10",phase:"religious-schism"},{year:1542,title:"The Holy Inquisition",type:"map",lat:41.9,lng:12.5,chapter:"10",phase:"religious-schism"},{year:1548,title:"Jesuits reach Africa",type:"map",lat:9.03,lng:38.74,chapter:"10",phase:"religious-schism"},{year:1552,title:"Khazar Rebellion in Rus-Horde Empire",type:"map",lat:55.79,lng:49.11,chapter:"10",phase:"religious-schism"},{year:1565,title:"Oprichnina coup (Romanov dynasty)",type:"map",lat:55.75,lng:37.62,chapter:"10",phase:"religious-schism"},{year:1582,title:"Gregorian Calendar introduced",type:"map",lat:41.9,lng:12.5,chapter:"10",phase:"religious-schism"},{year:1611,title:"King James Bible published",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1613,title:"Romanov dynasty takes the throne",type:"map",lat:55.75,lng:37.62,chapter:"11",phase:"romanov-split"},{year:1618,title:"Thirty Years War begins (Horde provinces vs Vatican)",type:"map",lat:50.08,lng:14.44,chapter:"11",phase:"romanov-split"},{year:1627,title:"Deep State erases Russian Empire from chronology",type:"map",lat:55.75,lng:37.62,chapter:"11",phase:"romanov-split"},{year:1642,title:"English Civil War begins",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1648,title:"Cossack-Polish War — ethnic cleansing in Ukraine",type:"map",lat:50.45,lng:30.52,chapter:"11",phase:"romanov-split"},{year:1664,title:"Great Comet of 1664",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1666,title:"London burns / Sabbatean crisis / Apocalypse of 1666",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1694,title:"Bank of England — central banking solidified",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1718,title:"Secret Society of Jesus goes public",type:"map",lat:51.51,lng:-.13,chapter:"12",phase:"collapse"},{year:1773,title:"Pugachev Rebellion — Final Tartary vs Romanov war",type:"map",lat:51.67,lng:55.1,chapter:"12",phase:"collapse"},{year:1774,title:"Carbon-14 spike / MudFlood begins",type:"map",lat:55.75,lng:37.62,chapter:"12",phase:"collapse"},{year:1803,title:"Napoleonic Wars begin",type:"map",lat:48.86,lng:2.35,chapter:"13",phase:"post-horde"},{year:1812,title:"Napoleon invades Russia",type:"map",lat:55.75,lng:37.62,chapter:"13",phase:"post-horde"},{year:1840,title:"Ecliptic pathway of the Absu last seen",type:"map",lat:55.75,lng:37.62,chapter:"13",phase:"post-horde"},{year:1848,title:"Battle for Communism's Soul: Marx vs Kinkel",type:"map",lat:50.94,lng:6.96,chapter:"13",phase:"post-horde"},{year:1883,title:"Hijacking of Communism",type:"map",lat:51.51,lng:-.13,chapter:"13",phase:"post-horde"},{year:1917,title:"Bolshevik Revolution",type:"map",lat:59.93,lng:30.32,chapter:"14",phase:"modern"}],ee=[{id:"pre-empire",label:"No Empires / No Borders",yearStart:1053,yearEnd:1149,color:"#888888",opacity:.1},{id:"empire-formation",label:"Rus-Horde Formation",yearStart:1150,yearEnd:1299,color:"#c62828",opacity:.3},{id:"peak-empire",label:"Great Tartary — Peak Expansion",yearStart:1300,yearEnd:1399,color:"#b71c1c",opacity:.45},{id:"fragmentation",label:"Regional Fragmentation — Ottoman/Spain/Habsburg",yearStart:1400,yearEnd:1499,color:"#e65100",opacity:.35},{id:"religious-schism",label:"Protestant vs Orthodox Schism",yearStart:1500,yearEnd:1599,color:"#f57f17",opacity:.35},{id:"romanov-split",label:"Romanov Takeover — Empire Fractures",yearStart:1600,yearEnd:1699,color:"#ff6f00",opacity:.3},{id:"collapse",label:"Final Collapse — Pugachev / MudFlood",yearStart:1700,yearEnd:1799,color:"#4e342e",opacity:.3},{id:"post-horde",label:"Post-Horde — Nation-States Emerge",yearStart:1800,yearEnd:1899,color:"#37474f",opacity:.2},{id:"modern",label:"Modern Borders",yearStart:1900,yearEnd:2026,color:"#263238",opacity:.15}],le=[{id:"before-creation",yearStart:-5e3,yearEnd:-4077,label:"Before Creation",description:"Chaotic plasma environment. Saturn coalescing. Proto-configuration forming.",saturn:{glow:.3,rings:!1,position:[0,2,0]},venus:null,mars:null,earth:null,skyColor:"#1a0a2e"},{id:"golden-age",yearStart:-4077,yearEnd:-3147,label:"Golden Age — Collinear Configuration",description:"Saturn-Venus-Mars-Earth aligned. Tree of Life visible. Northern: Wheel of Heaven. Southern: Petroglyph figures.",saturn:{glow:1,rings:!1,position:[0,4,0],color:"#ffcc00"},venus:{type:"plasmoid",points:8,position:[0,2,0],color:"#ffffff"},mars:{type:"solid",position:[0,.5,0],color:"#cc3300"},earth:{position:[0,-1.5,0],color:"#3366cc"},skyColor:"#0d1b4a",yearLength:225},{id:"breakup",yearStart:-3147,yearEnd:-3067,label:"Collinear Configuration Breaks Apart",description:"All 9 planets break from configuration. Exit Saturn's plasma sheath.",saturn:{glow:.6,rings:!1,position:[0,5,0]},venus:{type:"plasmoid",points:6,position:[2,3,1],color:"#ffffff"},mars:{type:"solid",position:[-1,1,2],color:"#cc3300"},earth:{position:[-3,-1,-2],color:"#3366cc"},skyColor:"#2d0a0a",chaotic:!0},{id:"round-table",yearStart:-3067,yearEnd:-2349,label:"Non-Linear 'Round Table' — Jupiter Dominates",description:"Saturn has fled to the outer solar system. Jupiter, Venus, Mars & Earth orbit an empty barycenter (no planet at center). This rotating circle orbits the Sun. Jupiter eclipses Sun once per orbit.",saturn:{glow:.3,rings:!1,position:[3,2,0]},venus:{type:"comet",position:[-2,1,3],color:"#ffeeaa"},mars:{type:"solid",position:[1,0,-2],color:"#cc3300"},earth:{position:[-1,-1,1],color:"#3366cc"},jupiter:{type:"dominant",position:[0,3,0],color:"#cc9944"},skyColor:"#1a0505",yearLength:273},{id:"deluge",yearStart:-2349,yearEnd:-2193,label:"The Deluge — Jupiter Disappears, Venus Attacks",description:"Jupiter disappears. Venus attacks Earth. Catastrophic flooding.",saturn:{glow:.2,rings:!1,position:[5,3,0]},venus:{type:"comet",position:[.5,.5,0],color:"#ff4444",threatening:!0},mars:{type:"solid",position:[2,-1,3],color:"#cc3300"},earth:{position:[0,0,0],color:"#3366cc",flooding:!0},skyColor:"#330000",yearLength:273},{id:"post-deluge",yearStart:-2193,yearEnd:-1492,label:"Post-Deluge — Destabilization Continues",description:"Jupiter consumes Venus. Sodom & Gomorrah. Configuration widening.",saturn:{glow:.15,rings:!1,position:[6,4,0]},venus:{type:"consumed",position:[3,3,0]},mars:{type:"solid",position:[.5,0,-1],color:"#cc3300",closeApproach:!0},earth:{position:[0,0,0],color:"#3366cc"},skyColor:"#1a0505",yearLength:273},{id:"venus-returns",yearStart:-1492,yearEnd:-806,label:"Venus Returns as Comet — Exodus",description:"Passover of Comet Venus. Venus and Mars tethered as 'the dragon'.",saturn:{glow:.1,rings:!1,position:[8,5,0]},venus:{type:"comet",position:[-1,1,0],color:"#ffaa00"},mars:{type:"solid",position:[-.5,.8,0],color:"#cc3300",tetheredToVenus:!0},earth:{position:[0,0,0],color:"#3366cc"},skyColor:"#0a0a1a",yearLength:290},{id:"stabilization",yearStart:-806,yearEnd:-670,label:"Orbits Finalize — Mars Loses Outer Shell",description:"Mars, Earth, Mercury move to final orbits. Iron Age begins.",saturn:{glow:.08,rings:!0,position:[10,6,0]},venus:{type:"planet",position:[-3,0,0],color:"#ffcc88"},mars:{type:"solid",position:[2,0,0],color:"#cc3300",shedding:!0},earth:{position:[0,0,0],color:"#3366cc"},skyColor:"#0a1a2a",yearLength:350},{id:"modern-solar",yearStart:-670,yearEnd:1053,label:"Modern Solar System — Phantom Period (The Blip)",description:"Solar system stable. 7th c. BCE to 10th c. CE is phantom time per Fomenko.",saturn:{glow:.05,rings:!0,position:[12,7,0],color:"#ccaa66"},venus:{type:"planet",position:[-4,0,0],color:"#ffcc88"},mars:{type:"planet",position:[3,0,0],color:"#cc3300"},earth:{position:[0,0,0],color:"#3366cc"},skyColor:"#0a1a3a",yearLength:365}];function U(i){return i<0?`${Math.abs(i)} BCE`:`${i} CE`}function Le(i,a,e,r=25){return i.filter(t=>e==="map"?t.type==="map":t.type==="planetary"||t.type==="blip").filter(t=>Math.abs(t.year-a)<=r).sort((t,s)=>t.year-s.year)}let _=null;const Ae="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png";async function Be(i,a){_||(_=(await me(async()=>{const{default:d}=await import("./leaflet-src-CzM8vlq-.js").then(c=>c.l);return{default:d}},[])).default);const e=_.map(i,{center:[48,40],zoom:4,minZoom:2,maxZoom:10,zoomControl:!0,attributionControl:!1});_.tileLayer(Ae,{subdomains:"abcd",maxZoom:19}).addTo(e);const r=JSON.parse(a),t={},s=[];let n=1053;r.features.forEach(d=>{const c=d.properties,g=_.geoJSON(d,{style:()=>({color:pe(c.phase),weight:2,opacity:0,fillColor:pe(c.phase),fillOpacity:0,dashArray:c.subRegion?"5,5":null})});g.bindTooltip(c.label||c.name,{className:"empire-tooltip",direction:"center",permanent:!1}),g.addTo(e),t[c.name]={layer:g,props:c}}),ye.filter(d=>d.type==="map"&&d.lat).forEach(d=>{const c=_.divIcon({className:"pulse-marker",iconSize:[12,12]}),g=_.marker([d.lat,d.lng],{icon:c,opacity:0});g.bindPopup(`<div class="event-popup">
        <h3>${d.title}</h3>
        <p class="year">${U(d.year)}</p>
      </div>`,{maxWidth:250}),g.addTo(e),s.push({marker:g,evt:d})});function o(d){n=d,Object.values(t).forEach(({layer:c,props:g})=>{const P=d>=g.yearStart&&d<=g.yearEnd,I=ee.find(G=>G.id===g.phase);let D=0;if(P){const G=g.yearEnd-g.yearStart,W=d-g.yearStart,R=g.yearEnd-d,q=Math.min(50,G*.1),T=Math.min(1,W/q),E=Math.min(1,R/q);D=Math.min(T,E)*(I?I.opacity:.3)}c.setStyle({opacity:P?.7:0,fillOpacity:D})}),s.forEach(({marker:c,evt:g})=>{const P=Math.abs(g.year-d)<=10,I=g.year<=d;c.setOpacity(I?P?1:.3:0)})}function y(){const d=ee.find(c=>n>=c.yearStart&&n<=c.yearEnd);return d?d.label:""}function M(){e.remove()}return{map:e,setYear:o,getPhaseLabel:y,destroy:M}}function pe(i){const a=ee.find(e=>e.id===i);return a?a.color:"#888"}let u=null;const N=-3147,H=.8,k={R:10,period:1,jupiter:{dist:1.5},saturn:{dist:3.5},venus:{dist:5.5},mars:{dist:7},earth:{dist:8.5},mercury:{dist:10},neptune:{dist:11.5},uranus:{dist:13}},x={sunDist:12,internalPeriod:1,solarPeriod:1,jupiter:{r:4.5},venus:{r:2.5},earth:{r:4.5},mars:{r:3.5},saturnFarPos:[25,2,-15]},S={mercury:{r:2,period:.24},venus:{r:3.5,period:.615},earth:{r:5,period:1},mars:{r:7,period:1.88},jupiter:{r:10,period:11.86},saturn:{r:13,period:29.46},uranus:{r:16,period:84},neptune:{r:19,period:164}};async function Oe(i){u||(u=await me(()=>import("./three.module-BtCAaDxU.js"),[]));const a=new u.Scene,e=new u.PerspectiveCamera(60,i.clientWidth/i.clientHeight,.1,1e3);e.position.set(0,10,25),e.lookAt(0,2,0);const r=new u.WebGLRenderer({canvas:i,antialias:!0,alpha:!0});r.setSize(i.clientWidth,i.clientHeight),r.setPixelRatio(Math.min(window.devicePixelRatio,2)),r.toneMapping=u.ACESFilmicToneMapping,r.toneMappingExposure=1.4,a.add(new u.AmbientLight(8952251,1.4));const t=new u.PointLight(16777164,3,120);t.position.set(0,0,0),a.add(t);const s=new u.DirectionalLight(11189196,.6);s.position.set(0,5,15),a.add(s);const n={};ze(a,n,u),Ne(a,n,u),De(a,n,u),Ve(a,n,u),_e(a,n,u),Je(a,n,u),$e(a,n,u),Ye(a,n,u),Ue(a,n,u),We(a,n,u);const m=qe(a,u);Ze(a,u);const o={};o.sun=A("SUN","#ffffaa",u),o.saturn=A("SATURN","#ff8833",u),o.venus=A("VENUS","#33ff77",u),o.mars=A("MARS","#ff6644",u),o.earth=A("EARTH","#66aaff",u),o.jupiter=A("JUPITER","#ffaa44",u),o.mercury=A("MERCURY","#bbaa88",u),o.neptune=A("NEPTUNE","#4466ff",u),o.uranus=A("URANUS","#66dddd",u),o.moon=A("MOON","#cccccc",u),Object.values(o).forEach(l=>a.add(l));const y={};y.collinear=je(a,u),y.roundTable=Fe(a,u),y.modern=Ge(a,u),$(y.collinear,!1),$(y.roundTable,!1),$(y.modern,!1);let M=-5e3,d="",c={},g=null,P=new u.Vector3(0,10,25),I=new u.Vector3(0,2,0);const D=()=>{const l=i.clientWidth,p=i.clientHeight;!l||!p||(e.aspect=l/p,e.updateProjectionMatrix(),r.setSize(l,p,!1))};let G=null;typeof ResizeObserver<"u"&&(G=new ResizeObserver(D),G.observe(i)),window.addEventListener("resize",D);function W(){var l,p,v,h,f,b,w,L;g=requestAnimationFrame(W),n.sun&&(n.sun.rotation.y+=.001),(l=n.saturn)!=null&&l.visible&&(n.saturn.rotation.y+=.002),(p=n.venus)!=null&&p.visible&&(n.venus.rotation.y+=.005),(v=n.mars)!=null&&v.visible&&(n.mars.rotation.y+=.004),(h=n.earth)!=null&&h.visible&&(n.earth.rotation.y+=.003),(f=n.jupiter)!=null&&f.visible&&(n.jupiter.rotation.y+=.001),(b=n.mercury)!=null&&b.visible&&(n.mercury.rotation.y+=.006),(w=n.neptune)!=null&&w.visible&&(n.neptune.rotation.y+=.001),(L=n.uranus)!=null&&L.visible&&(n.uranus.rotation.y+=.001),m!=null&&m.visible&&(m.rotation.y+=5e-4,m.rotation.x=Math.sin(performance.now()*1e-4)*.05),e.position.lerp(P,.03),e.lookAt(I),B(o.sun,n.sun,1.4,e),B(o.saturn,n.saturn,1.8,e),B(o.venus,n.venus,.8,e),B(o.mars,n.mars,.7,e),B(o.earth,n.earth,.8,e),B(o.jupiter,n.jupiter,1.4,e),B(o.mercury,n.mercury,.5,e),B(o.neptune,n.neptune,.7,e),B(o.uranus,n.uranus,.7,e),B(o.moon,n.moon,.4,e),r.render(a,e)}W();function R(l){M=l;const p=le.find(b=>l>=b.yearStart&&l<=b.yearEnd);if(!p)return;a.background=new u.Color(p.skyColor);const v=p.yearLength||365,h=l-p.yearStart;let f="none";if(p.id==="golden-age"?f="collinear":p.id==="round-table"?f="roundTable":(p.id==="stabilization"||p.id==="modern-solar")&&(f="modern"),f!==d&&($(y.collinear,f==="collinear"),$(y.roundTable,f==="roundTable"),$(y.modern,f==="modern"),d=f,f==="collinear"?(P.set(0,18,22),I.set(0,0,0)):f==="roundTable"?(P.set(0,22,22),I.set(0,0,0)):f==="modern"?(P.set(0,30,30),I.set(0,0,0)):(P.set(0,8,22),I.set(0,1,0))),n.sun.visible=!0,o.sun.visible=!0,f==="collinear"?q(h,p):f==="roundTable"?T(h,p):f==="modern"?E(h,p):ve(p),l>=N&&n.earth.visible){n.moon.visible=!0,o.moon.visible=!0;const b=Math.min(1,(l-N)/(-670-N)),w=10+(27.3-10)*b,F=(l-N)*v/w*Math.PI*2;n.moon.position.set(n.earth.position.x+H*Math.cos(F),n.earth.position.y+H*Math.sin(F)*.25,n.earth.position.z+H*Math.sin(F))}else n.moon.visible=!1,o.moon.visible=!1;if(m.visible=l<-806,m.visible&&(m.material.opacity=Math.max(0,Math.min(1,(-l-670)/2477))*.6),c={},f==="collinear"?(c.column=Math.abs(h),c.earth=Math.abs(h)):f==="roundTable"?(c["solar orbit"]=Math.abs(h/x.solarPeriod),c["internal rot"]=Math.abs(h/x.internalPeriod)):f==="modern"&&(c.mercury=Math.abs(h/.24),c.venus=Math.abs(h/.615),c.earth=Math.abs(h),c.mars=Math.abs(h/1.88),c.jupiter=Math.abs(h/11.86),c.saturn=Math.abs(h/29.46)),l>=N){const b=Math.min(1,(l-N)/(-670-N)),w=10+(27.3-10)*b;c.moon=Math.abs((l-N)*v/w)}}function q(l,p){var w,L;const v=l/k.period*Math.PI*2,h=Math.cos(v),f=Math.sin(v);n.sun.position.set(0,0,0),t.position.set(0,0,0);const b=(F,z,V,Z)=>{Z?(F.visible=!0,z&&(z.visible=!0),F.position.set(h*V,0,f*V)):(F.visible=!1,z&&(z.visible=!1))};b(n.jupiter,o.jupiter,k.jupiter.dist,!0),b(n.saturn,o.saturn,k.saturn.dist,!0),n.saturnGlow.material.opacity=(((w=p.saturn)==null?void 0:w.glow)||.5)*.6,n.saturnRings.material.opacity=(L=p.saturn)!=null&&L.rings?.5:0,b(n.venus,o.venus,k.venus.dist,!!p.venus),b(n.mars,o.mars,k.mars.dist,!!p.mars),b(n.earth,o.earth,k.earth.dist,!!p.earth),b(n.mercury,o.mercury,k.mercury.dist,!0),b(n.neptune,o.neptune,k.neptune.dist,!0),b(n.uranus,o.uranus,k.uranus.dist,!0)}function T(l,p){const v=l/x.solarPeriod*Math.PI*2,h=-(l/x.internalPeriod)*Math.PI*2,f=x.sunDist*Math.cos(v),b=x.sunDist*Math.sin(v);n.sun.position.set(0,0,0),t.position.set(0,0,0);const w=(z,V,Z,Pe,Ce)=>{if(!Ce){z.visible=!1,V&&(V.visible=!1);return}z.visible=!0,V&&(V.visible=!0);const oe=h+Pe;z.position.set(f+Z*Math.cos(oe),0,b+Z*Math.sin(oe))};w(n.jupiter,o.jupiter,x.jupiter.r,Math.PI,!0),w(n.venus,o.venus,x.venus.r,.3,!!p.venus);const F=Math.min(1,Math.abs(l)/700)*.8*Math.sin(l*.15);w(n.mars,o.mars,x.mars.r,-.25+F,!!p.mars),w(n.earth,o.earth,x.earth.r,-.5,!!p.earth),n.saturn.visible=!0,o.saturn.visible=!0,n.saturn.position.set(...x.saturnFarPos),n.saturnGlow.material.opacity=.1,n.saturnRings.material.opacity=0,n.mercury.visible=!1,o.mercury.visible=!1,n.neptune.visible=!1,o.neptune.visible=!1,n.uranus.visible=!1,o.uranus.visible=!1}function E(l,p){n.sun.position.set(0,0,0),t.position.set(0,0,0);const v=(h,f,b,w)=>{if(!w){h.visible=!1,f&&(f.visible=!1);return}h.visible=!0,f&&(f.visible=!0);const L=l/b.period*Math.PI*2;h.position.set(b.r*Math.cos(L),0,b.r*Math.sin(L))};v(n.mercury,o.mercury,S.mercury,!0),v(n.venus,o.venus,S.venus,!!p.venus),v(n.earth,o.earth,S.earth,!!p.earth),v(n.mars,o.mars,S.mars,!!p.mars),v(n.jupiter,o.jupiter,S.jupiter,!!p.jupiter),v(n.saturn,o.saturn,S.saturn,!!p.saturn),p.saturn&&(n.saturnGlow.material.opacity=(p.saturn.glow||.05)*.6,n.saturnRings.material.opacity=p.saturn.rings?.5:0),v(n.uranus,o.uranus,S.uranus,!0),v(n.neptune,o.neptune,S.neptune,!0)}function ve(l){n.sun.position.set(0,-3,-5),t.position.set(0,-3,-5);const p=(v,h)=>{h&&v.position.lerp(new u.Vector3(h[0],h[1],h[2]),.05)};l.saturn&&(n.saturn.visible=!0,o.saturn.visible=!0,p(n.saturn,l.saturn.position),n.saturnGlow.material.opacity=(l.saturn.glow||.3)*.6,n.saturnRings.material.opacity=l.saturn.rings?.5:0),l.venus?(n.venus.visible=!0,o.venus.visible=!0,p(n.venus,l.venus.position)):(n.venus.visible=!1,o.venus.visible=!1),l.mars?(n.mars.visible=!0,o.mars.visible=!0,p(n.mars,l.mars.position)):(n.mars.visible=!1,o.mars.visible=!1),l.earth?(n.earth.visible=!0,o.earth.visible=!0,p(n.earth,l.earth.position)):(n.earth.visible=!1,o.earth.visible=!1),l.jupiter?(n.jupiter.visible=!0,o.jupiter.visible=!0,p(n.jupiter,l.jupiter.position)):(n.jupiter.visible=!1,o.jupiter.visible=!1),n.mercury.visible=!1,o.mercury.visible=!1,n.neptune.visible=!1,o.neptune.visible=!1,n.uranus.visible=!1,o.uranus.visible=!1}function Me(){const l=le.find(p=>M>=p.yearStart&&M<=p.yearEnd);return l?{label:l.label,description:l.description}:{label:"",description:""}}function we(){return{...c}}function Se(){D()}function xe(){g&&cancelAnimationFrame(g),window.removeEventListener("resize",D),G&&G.disconnect(),r.dispose()}return{setYear:R,getPhaseInfo:Me,getOrbitInfo:we,resize:Se,destroy:xe}}function A(i,a,e){const r=document.createElement("canvas"),t=r.getContext("2d");r.width=256,r.height=64,t.clearRect(0,0,r.width,r.height),t.font="bold 48px Arial, sans-serif",t.textAlign="center",t.textBaseline="middle",t.shadowColor="rgba(0,0,0,0.8)",t.shadowBlur=6,t.fillStyle=a,t.fillText(i,r.width/2,r.height/2);const s=new e.CanvasTexture(r);s.minFilter=e.LinearFilter;const n=new e.Sprite(new e.SpriteMaterial({map:s,transparent:!0,depthTest:!1}));return n.scale.set(2.5,.6,1),n.visible=!1,n}function B(i,a,e,r){!(i!=null&&i.visible)||!(a!=null&&a.visible)||(i.position.set(a.position.x,a.position.y+e,a.position.z),i.quaternion.copy(r.quaternion))}function ae(i,a,e,r){const t=new r.BufferGeometry().setFromPoints(i),s=new r.LineBasicMaterial({color:a,transparent:!0,opacity:e,depthWrite:!1});return new r.Line(t,s)}function $(i,a){Array.isArray(i)?i.forEach(e=>{e.visible=a}):i&&(i.visible=a)}function je(i,a){const e=[];for(let t=0;t<=96;t++){const s=t/96*Math.PI*2;e.push(new a.Vector3(k.R*Math.cos(s),0,k.R*Math.sin(s)))}const r=ae(e,16746547,.3,a);return i.add(r),[r]}function Fe(i,a){const e=[],r=[];for(let s=0;s<=96;s++){const n=s/96*Math.PI*2;r.push(new a.Vector3(x.sunDist*Math.cos(n),0,x.sunDist*Math.sin(n)))}const t=ae(r,16755268,.25,a);return i.add(t),e.push(t),e}function Ge(i,a){const e=[],r=[{r:S.mercury.r,color:12298888},{r:S.venus.r,color:3407735},{r:S.earth.r,color:6728447},{r:S.mars.r,color:16737860},{r:S.jupiter.r,color:16755268},{r:S.saturn.r,color:16746547},{r:S.uranus.r,color:6741469},{r:S.neptune.r,color:4482815}];for(const t of r){const s=[];for(let m=0;m<=96;m++){const o=m/96*Math.PI*2;s.push(new a.Vector3(t.r*Math.cos(o),0,t.r*Math.sin(o)))}const n=ae(s,t.color,.25,a);i.add(n),e.push(n)}return e}function j(i,a){const r=document.createElement("canvas");r.width=128,r.height=128;const t=r.getContext("2d"),s=new a.Color(i),n=Math.round(s.r*255),m=Math.round(s.g*255),o=Math.round(s.b*255),y=t.createRadialGradient(128/2,128/2,0,128/2,128/2,128/2);return y.addColorStop(0,`rgba(${n},${m},${o},1)`),y.addColorStop(.3,`rgba(${n},${m},${o},0.5)`),y.addColorStop(1,`rgba(${n},${m},${o},0)`),t.fillStyle=y,t.fillRect(0,0,128,128),new a.CanvasTexture(r)}function ze(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.8,32,32),new e.MeshStandardMaterial({color:16777164,emissive:16768324,emissiveIntensity:1.5,roughness:0}));i.add(r),a.sun=r;const t=new e.Sprite(new e.SpriteMaterial({map:j(16768324,e),color:16768324,transparent:!0,opacity:.7,blending:e.AdditiveBlending}));t.scale.set(5,5,1),r.add(t)}function Ne(i,a,e){const r=new e.Mesh(new e.SphereGeometry(1.2,32,32),new e.MeshStandardMaterial({color:16746547,emissive:13395490,emissiveIntensity:.8,roughness:.3}));i.add(r),a.saturn=r;const t=new e.Sprite(new e.SpriteMaterial({map:j(16746547,e),color:16746547,transparent:!0,opacity:.6,blending:e.AdditiveBlending}));t.scale.set(5,5,1),r.add(t),a.saturnGlow=t;const s=new e.Mesh(new e.RingGeometry(1.6,2.4,64),new e.MeshBasicMaterial({color:13412966,side:e.DoubleSide,transparent:!0,opacity:0}));s.rotation.x=Math.PI/2.3,r.add(s),a.saturnRings=s}function De(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.4,16,16),new e.MeshStandardMaterial({color:3407735,emissive:2280533,emissiveIntensity:1,roughness:0}));i.add(r),a.venus=r;const t=new e.Sprite(new e.SpriteMaterial({map:j(3407735,e),color:3407735,transparent:!0,opacity:.5,blending:e.AdditiveBlending}));t.scale.set(3,3,1),r.add(t),a.venusGlow=t}function Ve(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.35,16,16),new e.MeshStandardMaterial({color:16729122,emissive:13382400,emissiveIntensity:.6,roughness:.6,metalness:.2}));i.add(r),a.mars=r;const t=new e.Sprite(new e.SpriteMaterial({map:j(16729122,e),color:16729122,transparent:!0,opacity:.25,blending:e.AdditiveBlending}));t.scale.set(1.5,1.5,1),r.add(t)}function _e(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.45,24,24),new e.MeshStandardMaterial({color:4491519,emissive:2245802,emissiveIntensity:.5,roughness:.4,metalness:.1}));i.add(r),a.earth=r;const t=new e.Sprite(new e.SpriteMaterial({map:j(4491519,e),color:4491519,transparent:!0,opacity:.2,blending:e.AdditiveBlending}));t.scale.set(1.8,1.8,1),r.add(t)}function Je(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.9,24,24),new e.MeshStandardMaterial({color:14527044,emissive:8939042,emissiveIntensity:.5,roughness:.5}));r.visible=!1,i.add(r),a.jupiter=r;const t=new e.Sprite(new e.SpriteMaterial({map:j(14527044,e),color:14527044,transparent:!0,opacity:.3,blending:e.AdditiveBlending}));t.scale.set(3,3,1),r.add(t)}function $e(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.2,16,16),new e.MeshStandardMaterial({color:12298888,emissive:8943445,emissiveIntensity:.4,roughness:.7}));r.visible=!1,i.add(r),a.mercury=r;const t=new e.Sprite(new e.SpriteMaterial({map:j(12298888,e),color:12298888,transparent:!0,opacity:.2,blending:e.AdditiveBlending}));t.scale.set(1,1,1),r.add(t)}function Ye(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.5,20,20),new e.MeshStandardMaterial({color:4482815,emissive:2241450,emissiveIntensity:.5,roughness:.4}));r.visible=!1,i.add(r),a.neptune=r;const t=new e.Sprite(new e.SpriteMaterial({map:j(4482815,e),color:4482815,transparent:!0,opacity:.25,blending:e.AdditiveBlending}));t.scale.set(2,2,1),r.add(t)}function Ue(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.5,20,20),new e.MeshStandardMaterial({color:6741469,emissive:4500138,emissiveIntensity:.5,roughness:.4}));r.visible=!1,i.add(r),a.uranus=r;const t=new e.Sprite(new e.SpriteMaterial({map:j(6741469,e),color:6741469,transparent:!0,opacity:.25,blending:e.AdditiveBlending}));t.scale.set(2,2,1),r.add(t)}function We(i,a,e){const r=new e.Mesh(new e.SphereGeometry(.15,16,16),new e.MeshStandardMaterial({color:12303291,emissive:6710886,emissiveIntensity:.3,roughness:.8}));r.visible=!1,i.add(r),a.moon=r;const t=new e.Sprite(new e.SpriteMaterial({map:j(11184810,e),color:11184810,transparent:!0,opacity:.15,blending:e.AdditiveBlending}));t.scale.set(.6,.6,1),r.add(t)}function qe(i,a){const r=new Float32Array(6e3),t=new Float32Array(2e3*3);for(let o=0;o<2e3;o++){const y=Math.random()*Math.PI*2,M=Math.random()*Math.PI,d=6+Math.random()*3;r[o*3]=d*Math.sin(M)*Math.cos(y),r[o*3+1]=d*Math.cos(M),r[o*3+2]=d*Math.sin(M)*Math.sin(y),t[o*3]=.3+Math.random()*.3,t[o*3+1]=.1+Math.random()*.2,t[o*3+2]=.5+Math.random()*.5}const s=new a.BufferGeometry;s.setAttribute("position",new a.BufferAttribute(r,3)),s.setAttribute("color",new a.BufferAttribute(t,3));const n=new a.PointsMaterial({size:.08,vertexColors:!0,transparent:!0,opacity:.6,blending:a.AdditiveBlending,depthWrite:!1}),m=new a.Points(s,n);return i.add(m),m}function Ze(i,a){const r=new Float32Array(15e3);for(let s=0;s<5e3;s++)r[s*3]=(Math.random()-.5)*200,r[s*3+1]=(Math.random()-.5)*200,r[s*3+2]=(Math.random()-.5)*200;const t=new a.BufferGeometry;t.setAttribute("position",new a.BufferAttribute(r,3)),i.add(new a.Points(t,new a.PointsMaterial({size:.1,color:16777215,transparent:!0,opacity:.6})))}const Ke=`{
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
}`;let J=1053,C="map",Q=!1,K=null,he=80,ne=null,te=null;const O=document.getElementById("timeline-slider"),fe=document.getElementById("btn-map"),ge=document.getElementById("btn-3d"),re=document.getElementById("btn-play"),ie=document.getElementById("btn-pause"),Xe=document.getElementById("btn-reset"),ce=document.getElementById("speed-select"),Qe=document.getElementById("map-view"),Re=document.getElementById("planet-view"),Te=document.getElementById("map-year-display"),Ee=document.getElementById("map-phase-label"),He=document.getElementById("planet-year-display"),en=document.getElementById("planet-phase-label"),nn=document.getElementById("planet-description"),tn=document.getElementById("event-feed"),an=document.getElementById("timeline-markers");document.addEventListener("DOMContentLoaded",async()=>{ne=await Be(document.getElementById("map"),Ke),te=await Oe(document.getElementById("planet-canvas")),be(),Y(J),rn()});function rn(){fe.addEventListener("click",()=>ue("map")),ge.addEventListener("click",()=>ue("3d")),O.addEventListener("input",()=>{Y(parseInt(O.value,10))}),re.addEventListener("click",de),ie.addEventListener("click",X),Xe.addEventListener("click",()=>{X(),Y(C==="map"?1053:-5e3)}),ce.addEventListener("change",()=>{he=parseInt(ce.value,10),Q&&(X(),de())})}function ue(i){C=i,fe.classList.toggle("active",C==="map"),ge.classList.toggle("active",C==="3d"),Qe.classList.toggle("active",C==="map"),Re.classList.toggle("active",C==="3d"),C==="map"?(O.min=1053,O.max=2026,J<1053&&Y(1053)):(O.min=-5e3,O.max=1053,J>1053&&Y(-4077)),O.value=J,be()}function Y(i){if(J=i,O.value=i,C==="map")ne.setYear(i),Te.textContent=U(i),Ee.textContent=ne.getPhaseLabel();else{te.setYear(i);const a=te.getPhaseInfo();He.textContent=U(i),en.textContent=a.label,nn.textContent=a.description}on(i)}function de(){if(Q)return;Q=!0,re.style.display="none",ie.style.display="";const i=C==="map"?1:J<-3e3?10:5,a=C==="map"?2026:1053;K=setInterval(()=>{const e=J+i;if(e>a){X();return}Y(e)},he)}function X(){Q=!1,re.style.display="",ie.style.display="none",K&&(clearInterval(K),K=null)}function on(i){const a=Le(ye,i,C);tn.innerHTML=a.map(e=>`<div class="event-item ${Math.abs(e.year-i)<=5?"active":""}">${U(e.year)} — ${e.title}</div>`).join("")}function be(){const i=parseInt(O.min,10),a=parseInt(O.max,10),e=C==="map"?100:500,r=[];for(let t=i;t<=a;t+=e)r.push(`<span>${U(t)}</span>`);an.innerHTML=r.join("")}
