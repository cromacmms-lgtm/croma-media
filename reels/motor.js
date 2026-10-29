const $ = id => document.getElementById(id);
const cl = (v,a=0,b=1) => Math.min(b, Math.max(a, v));
const P = (t,a,b) => cl((t-a)/(b-a));
const io = x => x<.5 ? 4*x*x*x : 1-Math.pow(-2*x+2,3)/2;
const oc = x => 1-Math.pow(1-x,3);
const ob = x => {const c1=1.7,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);};
const L = (a,b,x) => a+(b-a)*x;
const ELS = [...document.querySelectorAll('[data-a]')].filter(el=>!el.classList.contains('hlref')).map(el=>({el,
  a:+el.dataset.a, b: el.dataset.b!==undefined ? +el.dataset.b : null, fx: el.dataset.fx||'rise', din: +(el.dataset.in||.45)}));
const COUNTS = [...document.querySelectorAll('.count')];
const OPTS = [...document.querySelectorAll('.opt')];
const HOTS = [...document.querySelectorAll('[data-hot]')];
const HLS = [...document.querySelectorAll('.hlref')].map(e=>({id:e.dataset.id,a:+e.dataset.a,b:+e.dataset.b}));
const HLIDS = [...new Set(HLS.map(h=>h.id))];
const FLASH = [...document.querySelectorAll('[data-flash]')];
const SCANS = [...document.querySelectorAll('[data-scan]')];
const VIB = [...document.querySelectorAll('.eqw')].map(e=>({el:e, iv:JSON.parse(e.dataset.vib||'[]')}));
const ROTS = [...document.querySelectorAll('[data-rot]')];
const FLOWS = [...document.querySelectorAll('[data-flow]')];
const SLIDES = [...document.querySelectorAll('[data-slide]')];

function fx(o, t){
  const {el,a,b,fx,din} = o;
  const pin = fx==='pop' ? cl(P(t,a,a+.08)) : oc(P(t,a,a+din));
  const pout = b===null ? 0 : io(P(t,b,b+.3));
  let op = pin*(1-pout), tr = '';
  if(fx==='rise') tr = `translateY(${(1-pin)*40 - pout*24}px)`;
  else if(fx==='left') tr = `translateX(${(1-pin)*-50}px) translateY(${-pout*20}px)`;
  else if(fx==='right') tr = `translateX(${(1-pin)*90 - pout*90}px)`;
  else if(fx==='pop'){ const k=ob(P(t,a,a+.38)); tr = `scale(${Math.max(0,Math.min(1.25,k))})`; }
  else if(fx==='stamp'){ const k=oc(P(t,a,a+.28)); tr = `scale(${L(2.3,1,k)}) rotate(${L(-14,-6,k)}deg)`; op = cl(P(t,a,a+.1))*(1-pout); }
  else if(fx==='card'){ tr = `translateY(${(1-pin)*120 - pout*60}px) scale(${L(.95,1,pin)*L(1,.95,pout)})`; }
  else if(fx==='grow'){ const d=+(el.dataset.d||2); tr = `scaleY(${io(P(t,a,a+d))})`; op = cl(P(t,a,a+.2))*(1-pout); }
  el.style.opacity = op; el.style.transform = tr;
}
function fmt(v,dec){ return v.toFixed(dec).replace('.',','); }

function render(t){
  { const eh=$('endt').offsetHeight, top=640+eh+70; $('endlogo').style.top=top+'px'; $('endh').style.top=(top+150)+'px'; }
  // fondo
  $('b1').style.transform=`translate(${-180+Math.sin(t*.35)*60}px, ${420+Math.cos(t*.3)*50}px)`;
  $('b2').style.transform=`translate(${380+Math.cos(t*.25)*70}px, ${1050+Math.sin(t*.28)*60}px)`;
  $('b3').style.transform=`translate(${560+Math.sin(t*.4+1)*80}px, ${620+Math.cos(t*.33)*60}px)`;
  const rm=io(P(t,END-.6,END+.2));
  $('ring').style.transform=`translate(${L(-330,780,rm)+Math.sin(t*.2)*14}px, ${L(600,120,rm)}px) rotate(${t*6}deg)`;
  $('disc').style.transform=`translate(${-170+Math.cos(t*.3)*12}px, ${1660+Math.sin(t*.25)*14}px)`;
  for(const o of ELS) fx(o,t);
  for(const c of COUNTS){ const a=+c.dataset.a, d=+c.dataset.d; const v=L(+c.dataset.from, +c.dataset.to, oc(P(t,a,a+d))); c.textContent=fmt(v, +c.dataset.dec); }
  for(const o of OPTS){ const k=io(P(t,+o.dataset.ans,+o.dataset.ans+.35)); o.style.setProperty('--k',k);
    if(o.dataset.ok==='0') o.style.opacity = (+o.style.opacity)*(1-.55*k);
    else o.style.transform += ` scale(${1+.04*Math.sin(Math.PI*P(t,+o.dataset.ans,+o.dataset.ans+.4))})`; }
  for(const h of HOTS){ const a=+h.dataset.hot; h.style.setProperty('--k', io(P(t,a,a+.4))); }
  for(const id of HLIDS){ const el=$(id); if(!el) continue; let on=0;
    for(const h of HLS) if(h.id===id) on=Math.max(on, P(t,h.a,h.a+.25)*(1-P(t,h.b,h.b+.25)));
    el.setAttribute('opacity', on*(.6+.4*Math.sin(t*9))); }
  for(const f of FLASH){ const a=+f.dataset.flash; f.style.opacity = P(t,a,a+.05)*(1-P(t,a+.05,a+.35))*.85; }
  for(const s of SCANS){ const a=+s.dataset.scan; const p=P(t,a,a+.9); s.style.top=(p*100)+'%'; s.style.opacity = p>0 && p<1 ? 1 : 0; }
  for(const v of VIB){ let k=0; for(const [a,b] of v.iv) k=Math.max(k, P(t,a,a+.3)*(1-P(t,b-.3,b)));
    v.el.style.transform=`translate(${Math.sin(t*95)*3.5*k}px, ${Math.cos(t*120)*2.5*k}px)`; }
  for(const r of ROTS){ const [cx,cy,sp]=r.dataset.rot.split(',').map(Number); r.setAttribute('transform', `translate(${cx},${cy}) rotate(${t*sp})`); }
  for(const f of FLOWS){ f.style.strokeDashoffset = -(t*(+f.dataset.flow)); }
  for(const s of SLIDES){ const [sp,mod]=s.dataset.slide.split(',').map(Number); s.setAttribute('transform', `translate(${(t*sp)%mod},0)`); }
}
render(0);
