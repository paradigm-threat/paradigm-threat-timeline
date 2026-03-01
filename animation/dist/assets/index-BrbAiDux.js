(function(){const i=document.createElement("link").relList;if(i&&i.supports&&i.supports("modulepreload"))return;for(const n of document.querySelectorAll('link[rel="modulepreload"]'))a(n);new MutationObserver(n=>{for(const l of n)if(l.type==="childList")for(const t of l.addedNodes)t.tagName==="LINK"&&t.rel==="modulepreload"&&a(t)}).observe(document,{childList:!0,subtree:!0});function e(n){const l={};return n.integrity&&(l.integrity=n.integrity),n.referrerPolicy&&(l.referrerPolicy=n.referrerPolicy),n.crossOrigin==="use-credentials"?l.credentials="include":n.crossOrigin==="anonymous"?l.credentials="omit":l.credentials="same-origin",l}function a(n){if(n.ep)return;n.ep=!0;const l=e(n);fetch(n.href,l)}})();const Ne="modulepreload",Ye=function(r){return"/"+r},me={},ge=function(i,e,a){let n=Promise.resolve();if(e&&e.length>0){let t=function(c){return Promise.all(c.map(f=>Promise.resolve(f).then(m=>({status:"fulfilled",value:m}),m=>({status:"rejected",reason:m}))))};document.getElementsByTagName("link");const p=document.querySelector("meta[property=csp-nonce]"),o=(p==null?void 0:p.nonce)||(p==null?void 0:p.getAttribute("nonce"));n=t(e.map(c=>{if(c=Ye(c),c in me)return;me[c]=!0;const f=c.endsWith(".css"),m=f?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${c}"]${m}`))return;const d=document.createElement("link");if(d.rel=f?"stylesheet":Ne,f||(d.as="script"),d.crossOrigin="",d.href=c,o&&d.setAttribute("nonce",o),document.head.appendChild(d),f)return new Promise((b,S)=>{d.addEventListener("load",b),d.addEventListener("error",()=>S(new Error(`Unable to preload CSS for ${c}`)))})}))}function l(t){const p=new Event("vite:preloadError",{cancelable:!0});if(p.payload=t,window.dispatchEvent(p),!p.defaultPrevented)throw t}return n.then(t=>{for(const p of t||[])p.status==="rejected"&&l(p.reason);return i().catch(l)})},we=[{year:-5e3,title:"Before Creation",type:"planetary",phase:"before-creation"},{year:-4077,title:"Proto-Saturn joins Sun's orbit — Golden Age begins",type:"planetary",phase:"golden-age"},{year:-3147,title:"Golden Age ends violently — collinear configuration breaks",type:"planetary",phase:"dark-age"},{year:-3067,title:"Planets are at war — Jupiter assaults Saturn",type:"planetary",phase:"dark-age"},{year:-2860,title:"Non-linear 'Round Table' orbit stabilizes",type:"planetary",phase:"dark-age"},{year:-2349,title:"Jupiter disappears — Venus attacks Earth (Deluge)",type:"planetary",phase:"dark-age"},{year:-2193,title:"Earth leaves last Absu layer — Jupiter consumes Venus",type:"planetary",phase:"dark-age"},{year:-1936,title:"Sodom & Gomorrah destroyed by Mars",type:"planetary",phase:"dark-age"},{year:-1492,title:"Passover of Comet Venus — Exodus",type:"planetary",phase:"dark-age"},{year:-1442,title:"Sun stands still for Joshua",type:"planetary",phase:"dark-age"},{year:-806,title:"Mars, Earth, Mercury finalize orbits",type:"planetary",phase:"dark-age"},{year:-670,title:"Priori-Mars loses outer shell — Iron Age begins",type:"planetary",phase:"dark-age"},{year:-684,title:"Solar system becomes stable",type:"planetary",phase:"stability"},{year:-670,endYear:1053,title:"The Blip: 7th c. BCE to 10th c. CE never occurred (Fomenko)",type:"blip",phase:"blip"},{year:1053,title:"'Year of our Lord' Deception — 1053-year shift",type:"map",lat:41.01,lng:28.98,chapter:"05",phase:"empire-formation"},{year:1053,title:"Deep State centralizes world religion at Jerusalem",type:"map",lat:31.77,lng:35.23,chapter:"05",phase:"empire-formation"},{year:1152,title:"Historical Christ born in Crimea",type:"map",lat:44.95,lng:34.1,chapter:"06",phase:"empire-formation"},{year:1185,title:"Historical Christ crucified in Istanbul",type:"map",lat:41.01,lng:28.98,chapter:"06",phase:"empire-formation"},{year:1196,title:"First Crusade / Trojan War (revenge for Christ)",type:"map",lat:39.96,lng:26.24,chapter:"06",phase:"empire-formation"},{year:1200,title:"Russian Horde 'Tartarian' Empire emerges",type:"map",lat:55.75,lng:37.62,chapter:"07",phase:"empire-formation"},{year:1258,title:"Historical Christ dies",type:"map",lat:41.01,lng:28.98,chapter:"07",phase:"empire-formation"},{year:1285,title:"First Olympic Games",type:"map",lat:37.64,lng:21.63,chapter:"07",phase:"empire-formation"},{year:1300,title:"Great Expansion of Mongol-Slavic Horde",type:"map",lat:55.75,lng:37.62,chapter:"08",phase:"peak-empire"},{year:1380,title:"Battle of Kulikovo — Giants defeated",type:"map",lat:53.67,lng:38.67,chapter:"08",phase:"peak-empire"},{year:1421,title:"Meteorite falls on Yaroslavl",type:"map",lat:57.63,lng:39.87,chapter:"09",phase:"fragmentation"},{year:1431,title:"Jeanne d'Arc executed (Fomenko: ~1580)",type:"map",lat:49.44,lng:1.1,chapter:"09",phase:"fragmentation"},{year:1453,title:"Fall of Czar-Grad (Constantinople)",type:"map",lat:41.01,lng:28.98,chapter:"09",phase:"fragmentation"},{year:1455,title:"Gutenberg Bible translated into Latin",type:"map",lat:49.99,lng:8.27,chapter:"09",phase:"fragmentation"},{year:1486,title:"Revelation of the coming Apocalypse",type:"map",lat:41.9,lng:12.5,chapter:"09",phase:"fragmentation"},{year:1492,title:"The Apocalypse Crusade",type:"map",lat:37.39,lng:-5.98,chapter:"09",phase:"fragmentation"},{year:1517,title:"Protestant Reformation begins",type:"map",lat:51.87,lng:12.64,chapter:"10",phase:"religious-schism"},{year:1523,title:"Jesuits 'Pilgrimage' to Palestine",type:"map",lat:31.77,lng:35.23,chapter:"10",phase:"religious-schism"},{year:1542,title:"The Holy Inquisition",type:"map",lat:41.9,lng:12.5,chapter:"10",phase:"religious-schism"},{year:1548,title:"Jesuits reach Africa",type:"map",lat:9.03,lng:38.74,chapter:"10",phase:"religious-schism"},{year:1552,title:"Khazar Rebellion in Rus-Horde Empire",type:"map",lat:55.79,lng:49.11,chapter:"10",phase:"religious-schism"},{year:1565,title:"Oprichnina coup (Romanov dynasty)",type:"map",lat:55.75,lng:37.62,chapter:"10",phase:"religious-schism"},{year:1582,title:"Gregorian Calendar introduced",type:"map",lat:41.9,lng:12.5,chapter:"10",phase:"religious-schism"},{year:1611,title:"King James Bible published",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1613,title:"Romanov dynasty takes the throne",type:"map",lat:55.75,lng:37.62,chapter:"11",phase:"romanov-split"},{year:1618,title:"Thirty Years War begins (Horde provinces vs Vatican)",type:"map",lat:50.08,lng:14.44,chapter:"11",phase:"romanov-split"},{year:1627,title:"Deep State erases Russian Empire from chronology",type:"map",lat:55.75,lng:37.62,chapter:"11",phase:"romanov-split"},{year:1642,title:"English Civil War begins",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1648,title:"Cossack-Polish War — ethnic cleansing in Ukraine",type:"map",lat:50.45,lng:30.52,chapter:"11",phase:"romanov-split"},{year:1664,title:"Great Comet of 1664",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1666,title:"London burns / Sabbatean crisis / Apocalypse of 1666",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1694,title:"Bank of England — central banking solidified",type:"map",lat:51.51,lng:-.13,chapter:"11",phase:"romanov-split"},{year:1718,title:"Secret Society of Jesus goes public",type:"map",lat:51.51,lng:-.13,chapter:"12",phase:"collapse"},{year:1773,title:"Pugachev Rebellion — Final Tartary vs Romanov war",type:"map",lat:51.67,lng:55.1,chapter:"12",phase:"collapse"},{year:1774,title:"Carbon-14 spike / MudFlood begins",type:"map",lat:55.75,lng:37.62,chapter:"12",phase:"collapse"},{year:1803,title:"Napoleonic Wars begin",type:"map",lat:48.86,lng:2.35,chapter:"13",phase:"post-horde"},{year:1812,title:"Napoleon invades Russia",type:"map",lat:55.75,lng:37.62,chapter:"13",phase:"post-horde"},{year:1840,title:"Ecliptic pathway of the Absu last seen",type:"map",lat:55.75,lng:37.62,chapter:"13",phase:"post-horde"},{year:1848,title:"Battle for Communism's Soul: Marx vs Kinkel",type:"map",lat:50.94,lng:6.96,chapter:"13",phase:"post-horde"},{year:1883,title:"Hijacking of Communism",type:"map",lat:51.51,lng:-.13,chapter:"13",phase:"post-horde"},{year:1917,title:"Bolshevik Revolution",type:"map",lat:59.93,lng:30.32,chapter:"14",phase:"modern"}],re=[{id:"pre-empire",label:"No Empires / No Borders",yearStart:1053,yearEnd:1149,color:"#888888",opacity:.1},{id:"empire-formation",label:"Rus-Horde Formation",yearStart:1150,yearEnd:1299,color:"#c62828",opacity:.3},{id:"peak-empire",label:"Great Tartary — Peak Expansion",yearStart:1300,yearEnd:1399,color:"#b71c1c",opacity:.45},{id:"fragmentation",label:"Regional Fragmentation — Ottoman/Spain/Habsburg",yearStart:1400,yearEnd:1499,color:"#e65100",opacity:.35},{id:"religious-schism",label:"Protestant vs Orthodox Schism",yearStart:1500,yearEnd:1599,color:"#f57f17",opacity:.35},{id:"romanov-split",label:"Romanov Takeover — Empire Fractures",yearStart:1600,yearEnd:1699,color:"#ff6f00",opacity:.3},{id:"collapse",label:"Final Collapse — Pugachev / MudFlood",yearStart:1700,yearEnd:1799,color:"#4e342e",opacity:.3},{id:"post-horde",label:"Post-Horde — Nation-States Emerge",yearStart:1800,yearEnd:1899,color:"#37474f",opacity:.2},{id:"modern",label:"Modern Borders",yearStart:1900,yearEnd:2026,color:"#263238",opacity:.15}],he=[{id:"before-creation",yearStart:-5e3,yearEnd:-4077,label:"Before Creation",description:"Chaotic plasma environment. Saturn coalescing. Proto-configuration forming.",saturn:{glow:.3,rings:!1,position:[0,2,0]},venus:null,mars:null,earth:null,skyColor:"#1a0a2e"},{id:"golden-age",yearStart:-4077,yearEnd:-3147,label:"Golden Age — Collinear Configuration",description:"Saturn-Venus-Mars-Earth aligned. Tree of Life visible. Northern: Wheel of Heaven. Southern: Petroglyph figures.",saturn:{glow:1,rings:!1,position:[0,4,0],color:"#ffcc00"},venus:{type:"plasmoid",points:8,position:[0,2,0],color:"#ffffff"},mars:{type:"solid",position:[0,.5,0],color:"#cc3300"},earth:{position:[0,-1.5,0],color:"#3366cc"},skyColor:"#0d1b4a",yearLength:225},{id:"breakup",yearStart:-3147,yearEnd:-3067,label:"Collinear Configuration Breaks Apart",description:"All 9 planets break from configuration. Exit Saturn's plasma sheath.",saturn:{glow:.6,rings:!1,position:[0,5,0]},venus:{type:"plasmoid",points:6,position:[2,3,1],color:"#ffffff"},mars:{type:"solid",position:[-1,1,2],color:"#cc3300"},earth:{position:[-3,-1,-2],color:"#3366cc"},skyColor:"#2d0a0a",chaotic:!0},{id:"round-table",yearStart:-3067,yearEnd:-2349,label:"Non-Linear 'Round Table' — Jupiter Dominates",description:"Saturn has fled to the outer solar system. Jupiter, Venus, Mars & Earth orbit an empty barycenter (no planet at center). This rotating circle orbits the Sun. Jupiter eclipses Sun once per orbit.",saturn:{glow:.3,rings:!1,position:[3,2,0]},venus:{type:"comet",position:[-2,1,3],color:"#ffeeaa"},mars:{type:"solid",position:[1,0,-2],color:"#cc3300"},earth:{position:[-1,-1,1],color:"#3366cc"},jupiter:{type:"dominant",position:[0,3,0],color:"#cc9944"},skyColor:"#1a0505",yearLength:273},{id:"deluge",yearStart:-2349,yearEnd:-2193,label:"The Deluge — Jupiter Disappears, Venus Attacks",description:"Jupiter disappears. Venus attacks Earth. Catastrophic flooding.",saturn:{glow:.2,rings:!1,position:[5,3,0]},venus:{type:"comet",position:[.5,.5,0],color:"#ff4444",threatening:!0},mars:{type:"solid",position:[2,-1,3],color:"#cc3300"},earth:{position:[0,0,0],color:"#3366cc",flooding:!0},skyColor:"#330000",yearLength:273},{id:"post-deluge",yearStart:-2193,yearEnd:-1492,label:"Post-Deluge — Destabilization Continues",description:"Jupiter consumes Venus. Sodom & Gomorrah. Configuration widening.",saturn:{glow:.15,rings:!1,position:[6,4,0]},venus:{type:"consumed",position:[3,3,0]},mars:{type:"solid",position:[.5,0,-1],color:"#cc3300",closeApproach:!0},earth:{position:[0,0,0],color:"#3366cc"},skyColor:"#1a0505",yearLength:273},{id:"venus-returns",yearStart:-1492,yearEnd:-806,label:"Venus Returns as Comet — Exodus",description:"Passover of Comet Venus. Venus and Mars tethered as 'the dragon'.",saturn:{glow:.1,rings:!1,position:[8,5,0]},venus:{type:"comet",position:[-1,1,0],color:"#ffaa00"},mars:{type:"solid",position:[-.5,.8,0],color:"#cc3300",tetheredToVenus:!0},earth:{position:[0,0,0],color:"#3366cc"},skyColor:"#0a0a1a",yearLength:290},{id:"stabilization",yearStart:-806,yearEnd:-670,label:"Orbits Finalize — Mars Loses Outer Shell",description:"Mars, Earth, Mercury move to final orbits. Iron Age begins.",saturn:{glow:.08,rings:!0,position:[10,6,0]},venus:{type:"planet",position:[-3,0,0],color:"#ffcc88"},mars:{type:"solid",position:[2,0,0],color:"#cc3300",shedding:!0},earth:{position:[0,0,0],color:"#3366cc"},skyColor:"#0a1a2a",yearLength:350},{id:"modern-solar",yearStart:-670,yearEnd:1053,label:"Modern Solar System — Phantom Period (The Blip)",description:"Solar system stable. 7th c. BCE to 10th c. CE is phantom time per Fomenko.",saturn:{glow:.05,rings:!0,position:[12,7,0],color:"#ccaa66"},venus:{type:"planet",position:[-4,0,0],color:"#ffcc88"},mars:{type:"planet",position:[3,0,0],color:"#cc3300"},earth:{position:[0,0,0],color:"#3366cc"},skyColor:"#0a1a3a",yearLength:365}];function K(r){return r<0?`${Math.abs(r)} BCE`:`${r} CE`}function _e(r,i,e,a=25){return r.filter(n=>e==="map"?n.type==="map":n.type==="planetary"||n.type==="blip").filter(n=>Math.abs(n.year-i)<=a).sort((n,l)=>n.year-l.year)}let U=null;const We="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png";async function Je(r,i){U||(U=(await ge(async()=>{const{default:m}=await import("./leaflet-src-CzM8vlq-.js").then(d=>d.l);return{default:m}},[])).default);const e=U.map(r,{center:[48,40],zoom:4,minZoom:2,maxZoom:10,zoomControl:!0,attributionControl:!1});U.tileLayer(We,{subdomains:"abcd",maxZoom:19}).addTo(e);const a=JSON.parse(i),n={},l=[];let t=1053;a.features.forEach(m=>{const d=m.properties,b=U.geoJSON(m,{style:()=>({color:fe(d.phase),weight:2,opacity:0,fillColor:fe(d.phase),fillOpacity:0,dashArray:d.subRegion?"5,5":null})});b.bindTooltip(d.label||d.name,{className:"empire-tooltip",direction:"center",permanent:!1}),b.addTo(e),n[d.name]={layer:b,props:d}}),we.filter(m=>m.type==="map"&&m.lat).forEach(m=>{const d=U.divIcon({className:"pulse-marker",iconSize:[12,12]}),b=U.marker([m.lat,m.lng],{icon:d,opacity:0});b.bindPopup(`<div class="event-popup">
        <h3>${m.title}</h3>
        <p class="year">${K(m.year)}</p>
      </div>`,{maxWidth:250}),b.addTo(e),l.push({marker:b,evt:m})});function o(m){t=m,Object.values(n).forEach(({layer:d,props:b})=>{const S=m>=b.yearStart&&m<=b.yearEnd,P=re.find(O=>O.id===b.phase);let G=0;if(S){const O=b.yearEnd-b.yearStart,_=m-b.yearStart,ee=b.yearEnd-m,Q=Math.min(50,O*.1),te=Math.min(1,_/Q),ne=Math.min(1,ee/Q);G=Math.min(te,ne)*(P?P.opacity:.3)}d.setStyle({opacity:S?.7:0,fillOpacity:G})}),l.forEach(({marker:d,evt:b})=>{const S=Math.abs(b.year-m)<=10,P=b.year<=m;d.setOpacity(P?S?1:.3:0)})}function c(){const m=re.find(d=>t>=d.yearStart&&t<=d.yearEnd);return m?m.label:""}function f(){e.remove()}return{map:e,setYear:o,getPhaseLabel:c,destroy:f}}function fe(r){const i=re.find(e=>e.id===r);return i?i.color:"#888"}let h=null;const W=-3147,se=.8,I={R:10,period:1,jupiter:{dist:1.5},saturn:{dist:3.5},venus:{dist:5.5},mars:{dist:7},earth:{dist:8.5},mercury:{dist:10},neptune:{dist:11.5},uranus:{dist:13}},L={sunDist:12,internalPeriod:1,solarPeriod:1,jupiter:{r:4.5},venus:{r:2.5},earth:{r:4.5},mars:{r:3.5},saturnFarPos:[25,2,-15]},B={mercury:{r:2,period:.24},venus:{r:3.5,period:.615},earth:{r:5,period:1},mars:{r:7,period:1.88},jupiter:{r:10,period:11.86},saturn:{r:13,period:29.46},uranus:{r:16,period:84},neptune:{r:19,period:164}};async function Ue(r){h||(h=await ge(()=>import("./three.module-BtCAaDxU.js"),[]));const i=new h.Scene,e=new h.PerspectiveCamera(60,r.clientWidth/r.clientHeight,.1,1e3);e.position.set(0,10,25),e.lookAt(0,2,0);const a=new h.WebGLRenderer({canvas:r,antialias:!0,alpha:!0});a.setSize(r.clientWidth,r.clientHeight),a.setPixelRatio(Math.min(window.devicePixelRatio,2)),a.toneMapping=h.ACESFilmicToneMapping,a.toneMappingExposure=1.4,i.add(new h.AmbientLight(8952251,1.4));const n=new h.PointLight(16777164,3,120);n.position.set(0,0,0),i.add(n);const l=new h.DirectionalLight(11189196,.6);l.position.set(0,5,15),i.add(l);const t={};qe(i,t,h),Ke(i,t,h),Qe(i,t,h),Te(i,t,h),Re(i,t,h),He(i,t,h),Ee(i,t,h),et(i,t,h),tt(i,t,h),nt(i,t,h);const p=at(i,h);st(i,h),rt(i,t,h),ot(i,t,h),ct(i,t,h),ut(i,t,h),dt(i,t,h),ht(i,t,h),yt(i,t,h);const o={};o.sun=j("SUN","#ffffaa",h),o.saturn=j("SATURN","#ff8833",h),o.venus=j("VENUS","#33ff77",h),o.mars=j("MARS","#ff6644",h),o.earth=j("EARTH","#66aaff",h),o.jupiter=j("JUPITER","#ffaa44",h),o.mercury=j("MERCURY","#bbaa88",h),o.neptune=j("NEPTUNE","#4466ff",h),o.uranus=j("URANUS","#66dddd",h),o.moon=j("MOON","#cccccc",h),Object.values(o).forEach(s=>i.add(s));const c={};c.collinear=$e(i,h),c.roundTable=Ze(i,h),c.modern=Xe(i,h),X(c.collinear,!1),X(c.roundTable,!1),X(c.modern,!1);let f=-5e3,m="",d={},b=null,S=new h.Vector3(0,10,25),P=new h.Vector3(0,2,0);const G=()=>{const s=r.clientWidth,u=r.clientHeight;!s||!u||(e.aspect=s/u,e.updateProjectionMatrix(),a.setSize(s,u,!1))};let O=null;typeof ResizeObserver<"u"&&(O=new ResizeObserver(G),O.observe(r)),window.addEventListener("resize",G);function _(){var u,w,v,y,g,M,C,x,A,k,D,Y,Z,J,pe,de;b=requestAnimationFrame(_);const s=performance.now()*.001;if(t.sun&&(t.sun.rotation.y+=.001),(u=t.saturn)!=null&&u.visible&&(t.saturn.rotation.y+=.002),(w=t.venus)!=null&&w.visible&&(t.venus.rotation.y+=.005),(v=t.mars)!=null&&v.visible&&(t.mars.rotation.y+=.004),(y=t.earth)!=null&&y.visible&&(t.earth.rotation.y+=.003),(g=t.jupiter)!=null&&g.visible&&(t.jupiter.rotation.y+=.001),(M=t.mercury)!=null&&M.visible&&(t.mercury.rotation.y+=.006),(C=t.neptune)!=null&&C.visible&&(t.neptune.rotation.y+=.001),(x=t.uranus)!=null&&x.visible&&(t.uranus.rotation.y+=.001),p!=null&&p.visible&&(p.rotation.y+=5e-4,p.rotation.x=Math.sin(s*.1)*.05),(A=t.venusStar)!=null&&A.visible){const ae=s%20/20,je=4+4*(ae<.5?ae*2:2-ae*2);it(t.venusStar,je,h);const Ve=1+.15*Math.sin(s*2.5);t.venusStar.scale.setScalar(Ve),(k=t.venusStarGlow)!=null&&k.visible&&(t.venusStarGlow.material.opacity=.4+.2*Math.sin(s*3.7))}if((D=t.cometTail)!=null&&D.visible&&lt(t,s,h),(Y=t.marsShell)!=null&&Y.visible){const T=1+.05*Math.sin(s*1.3);t.marsShell.scale.setScalar(T),t.marsShell.userData.stressed&&(t.marsShell.material.emissiveIntensity=.3+.3*Math.abs(Math.sin(s*4)))}if((Z=t.marsFragments)!=null&&Z.visible&&pt(t.marsFragments,s,h),(J=t.dragonTether)!=null&&J.visible&&mt(t,s),(pe=t.birkelandCurrents)!=null&&pe.visible&&ft(t,s),(de=t.wheelOfHeaven)!=null&&de.visible){t.wheelOfHeaven.rotation.z+=.003;const T=.9+.1*Math.sin(s*.5);t.wheelOfHeaven.scale.setScalar(T)}e.position.lerp(S,.03),e.lookAt(P),V(o.sun,t.sun,1.4,e),V(o.saturn,t.saturn,1.8,e),V(o.venus,t.venus,.8,e),V(o.mars,t.mars,.7,e),V(o.earth,t.earth,.8,e),V(o.jupiter,t.jupiter,1.4,e),V(o.mercury,t.mercury,.5,e),V(o.neptune,t.neptune,.7,e),V(o.uranus,t.uranus,.7,e),V(o.moon,t.moon,.4,e),a.render(i,e)}_();function ee(s){f=s;const u=he.find(g=>s>=g.yearStart&&s<=g.yearEnd);if(!u)return;i.background=new h.Color(u.skyColor);const w=u.yearLength||365,v=s-u.yearStart;let y="none";if(u.id==="golden-age"?y="collinear":u.id==="round-table"?y="roundTable":(u.id==="stabilization"||u.id==="modern-solar")&&(y="modern"),y!==m&&(X(c.collinear,y==="collinear"),X(c.roundTable,y==="roundTable"),X(c.modern,y==="modern"),m=y,y==="collinear"?(S.set(0,18,22),P.set(0,0,0)):y==="roundTable"?(S.set(0,22,22),P.set(0,0,0)):y==="modern"?(S.set(0,30,30),P.set(0,0,0)):(S.set(0,8,22),P.set(0,1,0))),t.sun.visible=!0,o.sun.visible=!0,y==="collinear"?ke(v,u):y==="roundTable"?Ie(v,u):y==="modern"?Le(v,u):Ge(u),Q(t,u,s,v),te(t,u,s,v),ne(t,u,s,v),Ae(t,u),Be(t,u,y),s>=W&&t.earth.visible){t.moon.visible=!0,o.moon.visible=!0;const g=Math.min(1,(s-W)/(-670-W)),M=10+(27.3-10)*g,x=(s-W)*w/M*Math.PI*2;t.moon.position.set(t.earth.position.x+se*Math.cos(x),t.earth.position.y+se*Math.sin(x)*.25,t.earth.position.z+se*Math.sin(x))}else t.moon.visible=!1,o.moon.visible=!1;if(p.visible=s<-806,p.visible&&(p.material.opacity=Math.max(0,Math.min(1,(-s-670)/2477))*.6),d={},y==="collinear"?(d.column=Math.abs(v),d.earth=Math.abs(v)):y==="roundTable"?(d["solar orbit"]=Math.abs(v/L.solarPeriod),d["internal rot"]=Math.abs(v/L.internalPeriod)):y==="modern"&&(d.mercury=Math.abs(v/.24),d.venus=Math.abs(v/.615),d.earth=Math.abs(v),d.mars=Math.abs(v/1.88),d.jupiter=Math.abs(v/11.86),d.saturn=Math.abs(v/29.46)),s>=W){const g=Math.min(1,(s-W)/(-670-W)),M=10+(27.3-10)*g;d.moon=Math.abs((s-W)*w/M)}}function Q(s,u,w,v){if(s.wheelOfHeaven.visible=u.id==="golden-age",s.wheelOfHeaven.visible&&(s.wheelOfHeaven.position.copy(s.saturn.position),s.wheelOfHeaven.position.y+=.1),u.id==="stabilization"){const y=u.yearEnd-u.yearStart,g=Math.min(1,v/y);s.saturnRings.material.opacity=g*.5;const M=new h.Color(16746547).lerp(new h.Color(13412966),g);s.saturn.material.color.copy(M),s.saturn.material.emissive.copy(M)}else u.id==="modern-solar"&&(s.saturnRings.material.opacity=.5);u.saturn&&(s.saturnGlow.material.opacity=(u.saturn.glow||.05)*.6)}function te(s,u,w,v){var Y;const y=u.id,g=y==="golden-age",M=y==="breakup",C=y==="round-table"||y==="deluge",x=y==="venus-returns",A=y==="stabilization",k=y==="modern-solar",D=y==="post-deluge";if(s.venusStar.visible=g||M,s.venusStarGlow&&(s.venusStarGlow.visible=g||M),g?(s.venusStar.material.color.set(16777215),s.venusStar.material.emissive.set(16777215),s.venusStar.material.emissiveIntensity=1):M&&(s.venusStar.material.color.set(16772744),s.venusStar.material.emissive.set(16772744),s.venusStar.material.emissiveIntensity=.5+.5*Math.random()),s.cometTail.visible=C||x||A,C)s.cometTail.material.color.set(y==="deluge"?16729156:11206536),s.cometTail.material.opacity=.5;else if(x)s.cometTail.material.color.set(4521864),s.cometTail.material.opacity=.6;else if(A){const Z=u.yearEnd-u.yearStart,J=Math.min(1,v/Z);s.cometTail.material.opacity=.5*(1-J)}g||M?(s.venus.visible=!1,s.venusGlow.visible=!1):D?(s.venus.visible=!0,s.venusGlow.visible=!1,s.venus.material.emissiveIntensity=.1,s.venus.material.color.set(8947780)):k?(s.venus.visible=!!u.venus,s.venusGlow.visible=!!u.venus,s.venus.material.color.set(16764040),s.venus.material.emissive.set(11176004),s.venus.material.emissiveIntensity=.3):u.venus&&(s.venus.visible=!0,s.venusGlow.visible=!0,s.venus.material.color.set(u.venus.color||3407735),s.venus.material.emissive.set(u.venus.color||2280533),s.venus.material.emissiveIntensity=x?.8:.6),s.venusStar.visible&&(s.venusStar.position.copy(s.venus.visible?s.venus.position:new h.Vector3(0,2,0)),!s.venus.visible&&((Y=u.venus)!=null&&Y.position)&&s.venusStar.position.set(u.venus.position[0],u.venus.position[1],u.venus.position[2]))}function ne(s,u,w,v){const y=u.id,M=["round-table","deluge","post-deluge","venus-returns"].includes(y);s.marsShell.visible=M,M&&(s.marsShell.position.copy(s.mars.position),y==="venus-returns"?(s.marsShell.userData.stressed=!0,s.marsShell.material.emissive.set(16729088),s.marsShell.material.opacity=.25):y==="deluge"?(s.marsShell.userData.stressed=!1,s.marsShell.material.emissive.set(13378048),s.marsShell.material.emissiveIntensity=.5,s.marsShell.material.opacity=.2):(s.marsShell.userData.stressed=!1,s.marsShell.material.emissive.set(8925952),s.marsShell.material.emissiveIntensity=.15,s.marsShell.material.opacity=.15));const C=y==="stabilization";if(s.marsFragments.visible=C,C){s.marsFragments.userData.origin=s.mars.position.clone();const x=u.yearEnd-u.yearStart;s.marsFragments.userData.progress=Math.min(1,v/x);const A=Math.min(1,v/x);s.mars.scale.setScalar(1-A*.3),s.mars.material.color.set(new h.Color(16729122).lerp(new h.Color(10040081),A))}else y==="modern-solar"?(s.mars.scale.setScalar(.7),s.mars.material.color.set(10040081)):s.mars.scale.setScalar(1)}function Ae(s,u,w){const v=u.id==="venus-returns";s.dragonTether.visible=v,v&&s.venus.visible&&s.mars.visible&&(s.dragonTether.userData.venusPos=s.venus.position.clone(),s.dragonTether.userData.marsPos=s.mars.position.clone())}function Be(s,u,w){s.birkelandCurrents.visible=w==="collinear"}function ke(s,u){var M,C,x;const w=s/I.period*Math.PI*2,v=Math.cos(w),y=Math.sin(w);t.sun.position.set(0,0,0),n.position.set(0,0,0);const g=(A,k,D,Y)=>{Y?(A.visible=!0,k&&(k.visible=!0),A.position.set(v*D,0,y*D)):(A.visible=!1,k&&(k.visible=!1))};g(t.jupiter,o.jupiter,I.jupiter.dist,!0),g(t.saturn,o.saturn,I.saturn.dist,!0),t.saturnGlow.material.opacity=(((M=u.saturn)==null?void 0:M.glow)||.5)*.6,t.saturnRings.material.opacity=(C=u.saturn)!=null&&C.rings?.5:0,g(t.venus,o.venus,I.venus.dist,!!u.venus),(x=t.venusStar)!=null&&x.visible&&t.venusStar.position.set(v*I.venus.dist,0,y*I.venus.dist),g(t.mars,o.mars,I.mars.dist,!!u.mars),g(t.earth,o.earth,I.earth.dist,!!u.earth),g(t.mercury,o.mercury,I.mercury.dist,!0),g(t.neptune,o.neptune,I.neptune.dist,!0),g(t.uranus,o.uranus,I.uranus.dist,!0)}function Ie(s,u){const w=s/L.solarPeriod*Math.PI*2,v=-(s/L.internalPeriod)*Math.PI*2,y=L.sunDist*Math.cos(w),g=L.sunDist*Math.sin(w);t.sun.position.set(0,0,0),n.position.set(0,0,0);const M=(A,k,D,Y,Z)=>{if(!Z){A.visible=!1,k&&(k.visible=!1);return}A.visible=!0,k&&(k.visible=!0);const J=v+Y;A.position.set(y+D*Math.cos(J),0,g+D*Math.sin(J))};M(t.jupiter,o.jupiter,L.jupiter.r,Math.PI,!0),M(t.venus,o.venus,L.venus.r,.3,!!u.venus);const x=Math.min(1,Math.abs(s)/700)*.8*Math.sin(s*.15);M(t.mars,o.mars,L.mars.r,-.25+x,!!u.mars),M(t.earth,o.earth,L.earth.r,-.5,!!u.earth),t.saturn.visible=!0,o.saturn.visible=!0,t.saturn.position.set(...L.saturnFarPos),t.saturnGlow.material.opacity=.1,t.saturnRings.material.opacity=0,t.mercury.visible=!1,o.mercury.visible=!1,t.neptune.visible=!1,o.neptune.visible=!1,t.uranus.visible=!1,o.uranus.visible=!1}function Le(s,u){t.sun.position.set(0,0,0),n.position.set(0,0,0);const w=(v,y,g,M)=>{if(!M){v.visible=!1,y&&(y.visible=!1);return}v.visible=!0,y&&(y.visible=!0);const C=s/g.period*Math.PI*2;v.position.set(g.r*Math.cos(C),0,g.r*Math.sin(C))};w(t.mercury,o.mercury,B.mercury,!0),w(t.venus,o.venus,B.venus,!!u.venus),w(t.earth,o.earth,B.earth,!!u.earth),w(t.mars,o.mars,B.mars,!!u.mars),w(t.jupiter,o.jupiter,B.jupiter,!!u.jupiter),w(t.saturn,o.saturn,B.saturn,!!u.saturn),u.saturn&&(t.saturnGlow.material.opacity=(u.saturn.glow||.05)*.6,t.saturnRings.material.opacity=u.saturn.rings?.5:0),w(t.uranus,o.uranus,B.uranus,!0),w(t.neptune,o.neptune,B.neptune,!0)}function Ge(s){t.sun.position.set(0,-3,-5),n.position.set(0,-3,-5);const u=(w,v)=>{v&&w.position.lerp(new h.Vector3(v[0],v[1],v[2]),.05)};s.saturn&&(t.saturn.visible=!0,o.saturn.visible=!0,u(t.saturn,s.saturn.position),t.saturnGlow.material.opacity=(s.saturn.glow||.3)*.6,t.saturnRings.material.opacity=s.saturn.rings?.5:0),s.venus?(t.venus.visible=!0,o.venus.visible=!0,u(t.venus,s.venus.position)):(t.venus.visible=!1,o.venus.visible=!1),s.mars?(t.mars.visible=!0,o.mars.visible=!0,u(t.mars,s.mars.position)):(t.mars.visible=!1,o.mars.visible=!1),s.earth?(t.earth.visible=!0,o.earth.visible=!0,u(t.earth,s.earth.position)):(t.earth.visible=!1,o.earth.visible=!1),s.jupiter?(t.jupiter.visible=!0,o.jupiter.visible=!0,u(t.jupiter,s.jupiter.position)):(t.jupiter.visible=!1,o.jupiter.visible=!1),t.mercury.visible=!1,o.mercury.visible=!1,t.neptune.visible=!1,o.neptune.visible=!1,t.uranus.visible=!1,o.uranus.visible=!1}function ze(){const s=he.find(u=>f>=u.yearStart&&f<=u.yearEnd);return s?{label:s.label,description:s.description}:{label:"",description:""}}function Fe(){return{...d}}function Oe(){G()}function De(){b&&cancelAnimationFrame(b),window.removeEventListener("resize",G),O&&O.disconnect(),a.dispose()}return{setYear:ee,getPhaseInfo:ze,getOrbitInfo:Fe,resize:Oe,destroy:De}}function j(r,i,e){const a=document.createElement("canvas"),n=a.getContext("2d");a.width=256,a.height=64,n.clearRect(0,0,a.width,a.height),n.font="bold 48px Arial, sans-serif",n.textAlign="center",n.textBaseline="middle",n.shadowColor="rgba(0,0,0,0.8)",n.shadowBlur=6,n.fillStyle=i,n.fillText(r,a.width/2,a.height/2);const l=new e.CanvasTexture(a);l.minFilter=e.LinearFilter;const t=new e.Sprite(new e.SpriteMaterial({map:l,transparent:!0,depthTest:!1}));return t.scale.set(2.5,.6,1),t.visible=!1,t}function V(r,i,e,a){!(r!=null&&r.visible)||!(i!=null&&i.visible)||(r.position.set(i.position.x,i.position.y+e,i.position.z),r.quaternion.copy(a.quaternion))}function le(r,i,e,a){const n=new a.BufferGeometry().setFromPoints(r),l=new a.LineBasicMaterial({color:i,transparent:!0,opacity:e,depthWrite:!1});return new a.Line(n,l)}function X(r,i){Array.isArray(r)?r.forEach(e=>{e.visible=i}):r&&(r.visible=i)}function $e(r,i){const e=[];for(let n=0;n<=96;n++){const l=n/96*Math.PI*2;e.push(new i.Vector3(I.R*Math.cos(l),0,I.R*Math.sin(l)))}const a=le(e,16746547,.3,i);return r.add(a),[a]}function Ze(r,i){const e=[],a=[];for(let l=0;l<=96;l++){const t=l/96*Math.PI*2;a.push(new i.Vector3(L.sunDist*Math.cos(t),0,L.sunDist*Math.sin(t)))}const n=le(a,16755268,.25,i);return r.add(n),e.push(n),e}function Xe(r,i){const e=[],a=[{r:B.mercury.r,color:12298888},{r:B.venus.r,color:3407735},{r:B.earth.r,color:6728447},{r:B.mars.r,color:16737860},{r:B.jupiter.r,color:16755268},{r:B.saturn.r,color:16746547},{r:B.uranus.r,color:6741469},{r:B.neptune.r,color:4482815}];for(const n of a){const l=[];for(let p=0;p<=96;p++){const o=p/96*Math.PI*2;l.push(new i.Vector3(n.r*Math.cos(o),0,n.r*Math.sin(o)))}const t=le(l,n.color,.25,i);r.add(t),e.push(t)}return e}function F(r,i){const a=document.createElement("canvas");a.width=128,a.height=128;const n=a.getContext("2d"),l=new i.Color(r),t=Math.round(l.r*255),p=Math.round(l.g*255),o=Math.round(l.b*255),c=n.createRadialGradient(128/2,128/2,0,128/2,128/2,128/2);return c.addColorStop(0,`rgba(${t},${p},${o},1)`),c.addColorStop(.3,`rgba(${t},${p},${o},0.5)`),c.addColorStop(1,`rgba(${t},${p},${o},0)`),n.fillStyle=c,n.fillRect(0,0,128,128),new i.CanvasTexture(a)}function qe(r,i,e){const a=new e.Mesh(new e.SphereGeometry(.8,32,32),new e.MeshStandardMaterial({color:16777164,emissive:16768324,emissiveIntensity:1.5,roughness:0}));r.add(a),i.sun=a;const n=new e.Sprite(new e.SpriteMaterial({map:F(16768324,e),color:16768324,transparent:!0,opacity:.7,blending:e.AdditiveBlending}));n.scale.set(5,5,1),a.add(n)}function Ke(r,i,e){const a=new e.Mesh(new e.SphereGeometry(1.2,32,32),new e.MeshStandardMaterial({color:16746547,emissive:13395490,emissiveIntensity:.8,roughness:.3}));r.add(a),i.saturn=a;const n=new e.Sprite(new e.SpriteMaterial({map:F(16746547,e),color:16746547,transparent:!0,opacity:.6,blending:e.AdditiveBlending}));n.scale.set(5,5,1),a.add(n),i.saturnGlow=n;const l=new e.Mesh(new e.RingGeometry(1.6,2.4,64),new e.MeshBasicMaterial({color:13412966,side:e.DoubleSide,transparent:!0,opacity:0}));l.rotation.x=Math.PI/2.3,a.add(l),i.saturnRings=l}function Qe(r,i,e){const a=new e.Mesh(new e.SphereGeometry(.4,16,16),new e.MeshStandardMaterial({color:3407735,emissive:2280533,emissiveIntensity:1,roughness:0}));r.add(a),i.venus=a;const n=new e.Sprite(new e.SpriteMaterial({map:F(3407735,e),color:3407735,transparent:!0,opacity:.5,blending:e.AdditiveBlending}));n.scale.set(3,3,1),a.add(n),i.venusGlow=n}function Te(r,i,e){const a=new e.Mesh(new e.SphereGeometry(.35,16,16),new e.MeshStandardMaterial({color:16729122,emissive:13382400,emissiveIntensity:.6,roughness:.6,metalness:.2}));r.add(a),i.mars=a;const n=new e.Sprite(new e.SpriteMaterial({map:F(16729122,e),color:16729122,transparent:!0,opacity:.25,blending:e.AdditiveBlending}));n.scale.set(1.5,1.5,1),a.add(n)}function Re(r,i,e){const a=new e.Mesh(new e.SphereGeometry(.45,24,24),new e.MeshStandardMaterial({color:4491519,emissive:2245802,emissiveIntensity:.5,roughness:.4,metalness:.1}));r.add(a),i.earth=a;const n=new e.Sprite(new e.SpriteMaterial({map:F(4491519,e),color:4491519,transparent:!0,opacity:.2,blending:e.AdditiveBlending}));n.scale.set(1.8,1.8,1),a.add(n)}function He(r,i,e){const a=new e.Mesh(new e.SphereGeometry(.9,24,24),new e.MeshStandardMaterial({color:14527044,emissive:8939042,emissiveIntensity:.5,roughness:.5}));a.visible=!1,r.add(a),i.jupiter=a;const n=new e.Sprite(new e.SpriteMaterial({map:F(14527044,e),color:14527044,transparent:!0,opacity:.3,blending:e.AdditiveBlending}));n.scale.set(3,3,1),a.add(n)}function Ee(r,i,e){const a=new e.Mesh(new e.SphereGeometry(.2,16,16),new e.MeshStandardMaterial({color:12298888,emissive:8943445,emissiveIntensity:.4,roughness:.7}));a.visible=!1,r.add(a),i.mercury=a;const n=new e.Sprite(new e.SpriteMaterial({map:F(12298888,e),color:12298888,transparent:!0,opacity:.2,blending:e.AdditiveBlending}));n.scale.set(1,1,1),a.add(n)}function et(r,i,e){const a=new e.Mesh(new e.SphereGeometry(.5,20,20),new e.MeshStandardMaterial({color:4482815,emissive:2241450,emissiveIntensity:.5,roughness:.4}));a.visible=!1,r.add(a),i.neptune=a;const n=new e.Sprite(new e.SpriteMaterial({map:F(4482815,e),color:4482815,transparent:!0,opacity:.25,blending:e.AdditiveBlending}));n.scale.set(2,2,1),a.add(n)}function tt(r,i,e){const a=new e.Mesh(new e.SphereGeometry(.5,20,20),new e.MeshStandardMaterial({color:6741469,emissive:4500138,emissiveIntensity:.5,roughness:.4}));a.visible=!1,r.add(a),i.uranus=a;const n=new e.Sprite(new e.SpriteMaterial({map:F(6741469,e),color:6741469,transparent:!0,opacity:.25,blending:e.AdditiveBlending}));n.scale.set(2,2,1),a.add(n)}function nt(r,i,e){const a=new e.Mesh(new e.SphereGeometry(.15,16,16),new e.MeshStandardMaterial({color:12303291,emissive:6710886,emissiveIntensity:.3,roughness:.8}));a.visible=!1,r.add(a),i.moon=a;const n=new e.Sprite(new e.SpriteMaterial({map:F(11184810,e),color:11184810,transparent:!0,opacity:.15,blending:e.AdditiveBlending}));n.scale.set(.6,.6,1),a.add(n)}function at(r,i){const a=new Float32Array(6e3),n=new Float32Array(2e3*3);for(let o=0;o<2e3;o++){const c=Math.random()*Math.PI*2,f=Math.random()*Math.PI,m=6+Math.random()*3;a[o*3]=m*Math.sin(f)*Math.cos(c),a[o*3+1]=m*Math.cos(f),a[o*3+2]=m*Math.sin(f)*Math.sin(c),n[o*3]=.3+Math.random()*.3,n[o*3+1]=.1+Math.random()*.2,n[o*3+2]=.5+Math.random()*.5}const l=new i.BufferGeometry;l.setAttribute("position",new i.BufferAttribute(a,3)),l.setAttribute("color",new i.BufferAttribute(n,3));const t=new i.PointsMaterial({size:.08,vertexColors:!0,transparent:!0,opacity:.6,blending:i.AdditiveBlending,depthWrite:!1}),p=new i.Points(l,t);return r.add(p),p}function st(r,i){const a=new Float32Array(15e3);for(let l=0;l<5e3;l++)a[l*3]=(Math.random()-.5)*200,a[l*3+1]=(Math.random()-.5)*200,a[l*3+2]=(Math.random()-.5)*200;const n=new i.BufferGeometry;n.setAttribute("position",new i.BufferAttribute(a,3)),r.add(new i.Points(n,new i.PointsMaterial({size:.1,color:16777215,transparent:!0,opacity:.6})))}function rt(r,i,e){const a=Me(8,.5,.2,e),n=new e.MeshStandardMaterial({color:16777215,emissive:15663086,emissiveIntensity:1,roughness:0,transparent:!0,opacity:.95,side:e.DoubleSide}),l=new e.Mesh(a,n);l.visible=!1,r.add(l),i.venusStar=l;const t=new e.Sprite(new e.SpriteMaterial({map:F(11206604,e),color:11206604,transparent:!0,opacity:.5,blending:e.AdditiveBlending}));t.scale.set(3.5,3.5,1),t.visible=!1,l.add(t),i.venusStarGlow=t}function Me(r,i,e,a){const n=new a.Shape,l=Math.round(r);for(let p=0;p<=l*2;p++){const o=p/(l*2)*Math.PI*2-Math.PI/2,c=p%2===0?i:e,f=c*Math.cos(o),m=c*Math.sin(o);p===0?n.moveTo(f,m):n.lineTo(f,m)}return new a.ShapeGeometry(n)}function it(r,i,e){const a=Me(i,.5,.2,e);r.geometry.dispose(),r.geometry=a}function ot(r,i,e){const n=new Float32Array(1500),l=new Float32Array(500*3);for(let c=0;c<500;c++)n[c*3]=(Math.random()-.5)*.5,n[c*3+1]=(Math.random()-.5)*.5,n[c*3+2]=Math.random()*3+.5,l[c*3]=(Math.random()-.5)*.02,l[c*3+1]=(Math.random()-.5)*.02,l[c*3+2]=Math.random()*.05+.02;const t=new e.BufferGeometry;t.setAttribute("position",new e.BufferAttribute(n,3)),t.setAttribute("velocity",new e.BufferAttribute(l,3));const p=new e.PointsMaterial({size:.06,color:11206536,transparent:!0,opacity:.5,blending:e.AdditiveBlending,depthWrite:!1}),o=new e.Points(t,p);o.visible=!1,r.add(o),i.cometTail=o}function lt(r,i,e){var t,p,o;if(!((t=r.cometTail)!=null&&t.visible)||!((p=r.venus)!=null&&p.visible))return;const a=r.cometTail.geometry.attributes.position,n=r.cometTail.geometry.attributes.velocity,l=r.venus.position;for(let c=0;c<a.count;c++){let f=a.getX(c),m=a.getY(c),d=a.getZ(c);const b=n.getX(c),S=n.getY(c),P=n.getZ(c);f+=b+Math.sin(i*3+c*.1)*.01,m+=S+Math.cos(i*2.7+c*.13)*.01,d+=P,(d>5||Math.abs(f)>3||Math.abs(m)>3)&&(f=(Math.random()-.5)*.3,m=(Math.random()-.5)*.3,d=0),a.setXYZ(c,f,m,d)}if(a.needsUpdate=!0,r.cometTail.position.copy(l),(o=r.sun)!=null&&o.visible){const c=new e.Vector3().subVectors(l,r.sun.position).normalize();r.cometTail.lookAt(l.x+c.x,l.y+c.y,l.z+c.z)}}function ct(r,i,e){const a=new e.SphereGeometry(.55,24,24),n=new e.MeshStandardMaterial({color:13395524,emissive:8925952,emissiveIntensity:.15,roughness:.4,transparent:!0,opacity:.15,side:e.DoubleSide,wireframe:!1}),l=new e.Mesh(a,n);l.visible=!1,l.userData={stressed:!1},r.add(l),i.marsShell=l;const t=new e.SphereGeometry(.56,12,10),p=new e.MeshBasicMaterial({color:13386752,wireframe:!0,transparent:!0,opacity:.12}),o=new e.Mesh(t,p);l.add(o)}function ut(r,i,e){const n=new Float32Array(900),l=new Float32Array(300*3),t=new Float32Array(300);for(let f=0;f<300;f++){n[f*3]=0,n[f*3+1]=0,n[f*3+2]=0;const m=Math.random()*Math.PI*2,d=Math.acos(2*Math.random()-1);l[f*3]=Math.sin(d)*Math.cos(m),l[f*3+1]=Math.sin(d)*Math.sin(m),l[f*3+2]=Math.cos(d),t[f]=.03+Math.random()*.08}const p=new e.BufferGeometry;p.setAttribute("position",new e.BufferAttribute(n,3)),p.setAttribute("direction",new e.BufferAttribute(l,3)),p.setAttribute("size",new e.BufferAttribute(t,1));const o=new e.PointsMaterial({size:.1,color:13391155,transparent:!0,opacity:.8,blending:e.AdditiveBlending,depthWrite:!1}),c=new e.Points(p,o);c.visible=!1,c.userData={origin:new e.Vector3,progress:0},r.add(c),i.marsFragments=c}function pt(r,i,e){if(!(r!=null&&r.visible))return;const a=r.geometry.attributes.position,n=r.geometry.attributes.direction,l=r.userData.origin||new e.Vector3,t=r.userData.progress||0,p=t*8;for(let o=0;o<a.count;o++){const c=n.getX(o),f=n.getY(o),m=n.getZ(o),d=Math.sin(i*2+o*.5)*.05;a.setXYZ(o,l.x+c*p+d,l.y+f*p*.7+d,l.z+m*p+d)}a.needsUpdate=!0,r.material.opacity=Math.max(.1,.8*(1-t*.5))}function dt(r,i,e){const n=new Float32Array(180),l=new Float32Array(180);for(let c=0;c<60;c++){n[c*3]=0,n[c*3+1]=0,n[c*3+2]=0;const f=c/60,m=.3+.7*(1-f),d=.2+.6*f,b=.1;l[c*3]=m,l[c*3+1]=d,l[c*3+2]=b}const t=new e.BufferGeometry;t.setAttribute("position",new e.BufferAttribute(n,3)),t.setAttribute("color",new e.BufferAttribute(l,3));const p=new e.LineBasicMaterial({vertexColors:!0,transparent:!0,opacity:.7,blending:e.AdditiveBlending,depthWrite:!1,linewidth:2}),o=new e.Line(t,p);o.visible=!1,o.userData={venusPos:new e.Vector3,marsPos:new e.Vector3},r.add(o),i.dragonTether=o}function mt(r,i,e){var p;if(!((p=r.dragonTether)!=null&&p.visible))return;const a=r.dragonTether.geometry.attributes.position,n=r.dragonTether.userData.venusPos,l=r.dragonTether.userData.marsPos;if(!n||!l)return;const t=a.count;for(let o=0;o<t;o++){const c=o/(t-1),f=l.x+(n.x-l.x)*c,m=l.y+(n.y-l.y)*c,d=l.z+(n.z-l.z)*c,b=.3*Math.sin(c*Math.PI),S=b*Math.sin(i*5+c*12),P=b*.6*Math.cos(i*3.7+c*8),G=b*.3*Math.sin(i*7.3+c*20);a.setXYZ(o,f+S*.7+G*.3,m+P+G*.2,d+S*.3+P*.5)}a.needsUpdate=!0}function ht(r,i,e){const n=new Float32Array(90),l=new e.BufferGeometry;l.setAttribute("position",new e.BufferAttribute(n,3));const t=new e.LineBasicMaterial({color:8956671,transparent:!0,opacity:.5,blending:e.AdditiveBlending,depthWrite:!1}),p=new e.Line(l,t);p.visible=!1,r.add(p),i.birkelandCurrents=p}function ft(r,i,e){var p;if(!((p=r.birkelandCurrents)!=null&&p.visible))return;const a=r.birkelandCurrents.geometry.attributes.position,n=[r.sun,r.jupiter,r.saturn,r.venus,r.mars,r.earth,r.mercury,r.neptune,r.uranus].filter(o=>o==null?void 0:o.visible);if(n.length<2)return;const l=n.length-1,t=a.count;for(let o=0;o<t;o++){const c=o/(t-1),f=c*l,m=Math.floor(f),d=f-m,b=n[Math.min(m,n.length-1)],S=n[Math.min(m+1,n.length-1)],P=b.position.x+(S.position.x-b.position.x)*d,G=b.position.y+(S.position.y-b.position.y)*d,O=b.position.z+(S.position.z-b.position.z)*d,_=.08*Math.sin(i*4+c*15);a.setXYZ(o,P+_,G+_*.5,O+_*.3)}a.needsUpdate=!0}function yt(r,i,e){const a=new e.Group,n=new e.RingGeometry(2,2.2,64),l=new e.MeshBasicMaterial({color:16763972,side:e.DoubleSide,transparent:!0,opacity:.3,blending:e.AdditiveBlending});a.add(new e.Mesh(n,l));const t=new e.RingGeometry(.8,1,64);a.add(new e.Mesh(t,l));const p=new e.LineBasicMaterial({color:16768358,transparent:!0,opacity:.4,blending:e.AdditiveBlending});for(let c=0;c<8;c++){const f=c/8*Math.PI*2,m=[new e.Vector3(.9*Math.cos(f),.9*Math.sin(f),0),new e.Vector3(2.1*Math.cos(f),2.1*Math.sin(f),0)],d=new e.BufferGeometry().setFromPoints(m);a.add(new e.Line(d,p))}const o=new e.Sprite(new e.SpriteMaterial({map:F(16763972,e),color:16763972,transparent:!0,opacity:.4,blending:e.AdditiveBlending}));o.scale.set(4,4,1),a.add(o),a.visible=!1,r.add(a),i.wheelOfHeaven=a}const vt=`{
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
}`;let $=1053,z="map",E=!1,R=null,Se=80,ie=null,oe=null;const N=document.getElementById("timeline-slider"),xe=document.getElementById("btn-map"),Pe=document.getElementById("btn-3d"),ce=document.getElementById("btn-play"),ue=document.getElementById("btn-pause"),bt=document.getElementById("btn-reset"),ye=document.getElementById("speed-select"),gt=document.getElementById("map-view"),wt=document.getElementById("planet-view"),Mt=document.getElementById("map-year-display"),St=document.getElementById("map-phase-label"),xt=document.getElementById("planet-year-display"),Pt=document.getElementById("planet-phase-label"),Ct=document.getElementById("planet-description"),At=document.getElementById("event-feed"),Bt=document.getElementById("timeline-markers");document.addEventListener("DOMContentLoaded",async()=>{ie=await Je(document.getElementById("map"),vt),oe=await Ue(document.getElementById("planet-canvas")),Ce(),q($),kt()});function kt(){xe.addEventListener("click",()=>ve("map")),Pe.addEventListener("click",()=>ve("3d")),N.addEventListener("input",()=>{q(parseInt(N.value,10))}),ce.addEventListener("click",be),ue.addEventListener("click",H),bt.addEventListener("click",()=>{H(),q(z==="map"?1053:-5e3)}),ye.addEventListener("change",()=>{Se=parseInt(ye.value,10),E&&(H(),be())})}function ve(r){z=r,xe.classList.toggle("active",z==="map"),Pe.classList.toggle("active",z==="3d"),gt.classList.toggle("active",z==="map"),wt.classList.toggle("active",z==="3d"),z==="map"?(N.min=1053,N.max=2026,$<1053&&q(1053)):(N.min=-5e3,N.max=1053,$>1053&&q(-4077)),N.value=$,Ce()}function q(r){if($=r,N.value=r,z==="map")ie.setYear(r),Mt.textContent=K(r),St.textContent=ie.getPhaseLabel();else{oe.setYear(r);const i=oe.getPhaseInfo();xt.textContent=K(r),Pt.textContent=i.label,Ct.textContent=i.description}It(r)}function be(){if(E)return;E=!0,ce.style.display="none",ue.style.display="";const r=z==="map"?1:$<-3e3?10:5,i=z==="map"?2026:1053;R=setInterval(()=>{const e=$+r;if(e>i){H();return}q(e)},Se)}function H(){E=!1,ce.style.display="",ue.style.display="none",R&&(clearInterval(R),R=null)}function It(r){const i=_e(we,r,z);At.innerHTML=i.map(e=>`<div class="event-item ${Math.abs(e.year-r)<=5?"active":""}">${K(e.year)} — ${e.title}</div>`).join("")}function Ce(){const r=parseInt(N.min,10),i=parseInt(N.max,10),e=z==="map"?100:500,a=[];for(let n=r;n<=i;n+=e)a.push(`<span>${K(n)}</span>`);Bt.innerHTML=a.join("")}
