(function(){
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=window.matchMedia&&matchMedia('(hover:hover) and (pointer:fine)').matches;

  /* counters */
  function counts(p){p.querySelectorAll('.count').forEach(function(el){var to=+el.dataset.to;if(reduce){el.textContent=to;return}var t0=null;function f(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/1400);k=1-Math.pow(1-k,3);el.textContent=Math.round(to*k);if(k<1)requestAnimationFrame(f)}requestAnimationFrame(f)})}

  /* the light follows the pointer */
  if(fine&&!reduce){document.querySelectorAll('.follow').forEach(function(el){el.addEventListener('pointermove',function(e){var r=el.getBoundingClientRect();el.style.setProperty('--mx',((e.clientX-r.left)/r.width*100).toFixed(1)+'%');el.style.setProperty('--my',((e.clientY-r.top)/r.height*100).toFixed(1)+'%')});el.addEventListener('pointerleave',function(){el.style.removeProperty('--mx');el.style.removeProperty('--my')})});
    var tilt=document.querySelector('.t1 .tilt');if(tilt){var hero=document.getElementById('hero1');hero.addEventListener('pointermove',function(e){var r=tilt.getBoundingClientRect(),dx=(e.clientX-(r.left+r.width/2))/r.width,dy=(e.clientY-(r.top+r.height/2))/r.height;tilt.style.setProperty('--ry',(dx*6).toFixed(2)+'deg');tilt.style.setProperty('--rx',(-dy*6).toFixed(2)+'deg')});hero.addEventListener('pointerleave',function(){tilt.style.removeProperty('--rx');tilt.style.removeProperty('--ry')})}}

  /* giving: one config, every widget routes through it. Empty url = preview. */
  var GIVE={url:'',amount_param:'',freq_param:'',freq_monthly:'',freq_once:''};
  var WHAT={25:'goes toward the books and materials fathers are trained from.',50:'goes toward training the pastors who disciple those fathers.',100:'goes toward planting a church and keeping it going.',250:'goes toward the cost of getting a team to the field.'};
  document.querySelectorAll('[data-give]').forEach(function(g){
    var f='m',a=50,custom=false,fb=[].slice.call(g.querySelectorAll('[data-f]')),ab=[].slice.call(g.querySelectorAll('[data-a]')),inp=g.querySelector('input'),lab=g.querySelector('.gv-custom'),what=g.querySelector('.gv-what'),go=g.querySelector('.gv-go'),note=g.querySelector('.gv-note');
    function amt(){return custom?(parseInt(inp.value,10)||0):a}
    function href(){var v=amt();if(!GIVE.url)return '#';var q=[];if(GIVE.amount_param&&v)q.push(GIVE.amount_param+'='+v);if(GIVE.freq_param)q.push(GIVE.freq_param+'='+(f==='m'?GIVE.freq_monthly:GIVE.freq_once));return GIVE.url+(q.length?(GIVE.url.indexOf('?')<0?'?':'&')+q.join('&'):'')}
    function render(){
      fb.forEach(function(b){b.setAttribute('aria-checked',String(b.dataset.f===f))});
      ab.forEach(function(b){b.setAttribute('aria-checked',String(!custom&&+b.dataset.a===a))});
      lab.classList.toggle('on',custom);
      var v=amt(),per=f==='m'?' a month':'';
      what.textContent=v?('$'+v+per+' '+(custom?'goes toward the work in Honduras.':WHAT[a])):'Type any amount.';
      go.textContent=v?('Give $'+v+per):(f==='m'?'Give monthly':'Give');
      go.setAttribute('href',href());
    }
    fb.forEach(function(b){b.addEventListener('click',function(){f=b.dataset.f;render()})});
    ab.forEach(function(b){b.addEventListener('click',function(){a=+b.dataset.a;custom=false;inp.value='';render()})});
    inp.addEventListener('focus',function(){custom=true;render()});
    inp.addEventListener('input',function(){inp.value=inp.value.replace(/\D/g,'').slice(0,5);custom=true;render()});
    go.addEventListener('click',function(e){if(!GIVE.url){e.preventDefault();note.hidden=false}});
    render();
  });

  /* floating Give button: shows once the opening is gone, hides at the give section */
  if('IntersectionObserver' in window){document.querySelectorAll('[data-fgive]').forEach(function(btn){
    var tpl=btn.closest('.tpl'),hero=tpl.querySelector('.glow, .letter'),give=tpl.querySelector(btn.getAttribute('href')),heroIn=true,giveIn=false;
    var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.target===hero)heroIn=e.isIntersecting;else giveIn=e.isIntersecting});btn.classList.toggle('on',!heroIn&&!giveIn)});
    o.observe(hero);o.observe(give);
  })}


  /* the gold thread: finds every two-column section, runs down the gap between the columns, swoops wide across the empty space between sections, ends on the logo */
  var run=document.getElementById('run1'),svg=run.querySelector('.thread'),base=svg.querySelector('.base'),fill=svg.querySelector('.fill'),ng=svg.querySelector('.nodes'),L=0,dots=[],tick=false,NS='http://www.w3.org/2000/svg';
  var STOPS=['.kids-in','.mission-in','.found-in','.lead-in','.ch-in','.song-in'],BOX='img,video,.three li';
  function R(el){return el.getBoundingClientRect()}
  function Q(s){return run.querySelector(s)}
  function bgOf(el){while(el&&el!==document.documentElement){var c=getComputedStyle(el).backgroundColor;if(c&&c!=='transparent'&&!/,\s*0\)$/.test(c))return c;el=el.parentElement}return '#F6F1E6'}
  function f(n){return n.toFixed(1)}
  /* where the visible stuff in a column actually is: text lines, photos, cards (not the empty width of a block) */
  function ext(el){var b={l:1e9,r:-1e9,t:1e9,b:-1e9};function add(q){if(q.width<1||q.height<1)return;b.l=Math.min(b.l,q.left);b.r=Math.max(b.r,q.right);b.t=Math.min(b.t,q.top);b.b=Math.max(b.b,q.bottom)}
    var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),n,rg=document.createRange();while(n=w.nextNode()){if(!n.nodeValue.trim())continue;rg.selectNodeContents(n);[].forEach.call(rg.getClientRects(),add)}
    [].forEach.call(el.querySelectorAll(BOX),function(e){add(R(e))});if(el.matches(BOX))add(R(el));return b}
  function geo(rr){
    var W=rr.width,nodes=[],d='';
    function pt(x,y,el,dot){var p={x:x-rr.left,y:y-rr.top,bg:el?bgOf(el):'',dot:dot!==false};if(p.dot)nodes.push(p);return p}
    function M(p){d+='M'+f(p.x)+','+f(p.y)}
    function Ln(p){d+=' L'+f(p.x)+','+f(p.y)}
    function S(a,b,k){var h=(b.y-a.y)*(k||.62);d+=' C'+f(a.x)+','+f(a.y+h)+' '+f(b.x)+','+f(b.y-h)+' '+f(b.x)+','+f(b.y)}
    var grids=STOPS.map(Q).filter(Boolean);
    if(innerWidth<=860){
      var w=Q('.kids .wrap'),x=R(w).left+parseFloat(getComputedStyle(w).paddingLeft)-22;
      grids.concat([Q('.tab .frame'),Q('.shop-in')]).forEach(function(el){pt(x,R(el).top+14,el)});
      var sb=R(Q('.give .seal'));pt(x,sb.top+sb.height/2,Q('.give'));
      M({x:nodes[0].x,y:0});nodes.forEach(Ln);return {d:d,nodes:nodes};
    }
    var N=[],B=[];
    grids.forEach(function(g){var k=g.children,a=ext(k[0]),b=ext(k[1]),gb=R(g),top=Math.max(a.t,b.t),bot=Math.min(a.b,b.b);
      N.push(pt((a.r+b.l)/2,bot>top?(top+bot)/2:gb.top+gb.height/2,g));B.push({top:gb.top-rr.top,bot:gb.bottom-rr.top})});
    var fr=R(Q('.tab .frame')),ts=R(Q('.tab'));var T=pt(rr.left+W/2,fr.top-(fr.top-ts.top)*.5,Q('.tab'));
    var rp=R(Q('.tab .row p'));var Tw=pt(Math.min(rr.left+W-40,Math.max(rp.right+70,rr.left+W*.74)),rp.top+rp.height/2,null,false);
    var card=Q('.shop-in'),cb=R(card);var Sh=pt((R(card.querySelector('p')).right+cb.right)/2,cb.top+cb.height/2,card);
    var seal=R(Q('.give .seal'));var G=pt(seal.left+seal.width/2,seal.top-10,Q('.give'));
    M({x:N[0].x,y:0});Ln(N[0]);
    for(var i=0;i<N.length;i++){
      var last=i===N.length-1,a={x:N[i].x,y:B[i].bot+14},end=last?T:N[i+1],b={x:end.x,y:last?T.y:B[i+1].top-14},mid={x:i%2?W*.08:W*.92,y:(a.y+b.y)/2};
      Ln(a);S(a,mid);S(mid,b);if(!last)Ln(N[i+1]);
    }
    S(T,Tw,.6);S(Tw,Sh,.6);S(Sh,G,.55);
    return {d:d,nodes:nodes};
  }
  function build(){
    var rr=R(run),W=rr.width,H=run.scrollHeight;svg.setAttribute('width',W);svg.setAttribute('height',H);svg.setAttribute('viewBox','0 0 '+W+' '+H);
    var g=geo(rr);base.setAttribute('d',g.d);fill.setAttribute('d',g.d);L=fill.getTotalLength();fill.style.strokeDasharray=L;LUT=[];
    while(ng.firstChild)ng.removeChild(ng.firstChild);dots=[];
    g.nodes.forEach(function(p){var h=document.createElementNS(NS,'circle'),c=document.createElementNS(NS,'circle');
      h.setAttribute('class','halo');h.setAttribute('cx',p.x);h.setAttribute('cy',p.y);h.setAttribute('r',16);
      c.setAttribute('class','nd');c.setAttribute('cx',p.x);c.setAttribute('cy',p.y);c.setAttribute('r',8);c.style.fill=p.bg;
      ng.appendChild(h);ng.appendChild(c);dots.push({y:p.y,h:h,c:c})});
    thread();
  }
  /* the line follows your scroll along its own length, so it travels sideways through each swoop */
  var LUT=[];
  function lut(){LUT=[];var n=400;for(var i=0;i<=n;i++){var q=fill.getPointAtLength(L*i/n);LUT.push(q.y)}}
  function thread(){
    if(!L)return;
    if(LUT.length!==401)lut();
    var r=R(run),line=innerHeight*.6,y=line-r.top,p;
    if(reduce)p=1;else{var lo=0;for(var i=0;i<=400;i++){if(LUT[i]<=y)lo=i;else break}p=lo/400}
    if(scrollY+innerHeight>=document.documentElement.scrollHeight-4)p=1;
    tgt=p;if(reduce){cur=p;fill.style.strokeDashoffset=0}else if(!anim){anim=requestAnimationFrame(glide)}
    dots.forEach(function(d){var on=reduce||(r.top+d.y)<line+1;d.c.classList.toggle('on',on);d.h.classList.toggle('on',on)});
  }
  /* the drawn line glides toward where the scroll says it should be, so it sweeps through each swoop instead of jumping */
  var cur=0,tgt=0,anim=0;
  function glide(){var dlt=tgt-cur;cur=Math.abs(dlt)<.0004?tgt:cur+dlt*.09;fill.style.strokeDashoffset=L*(1-cur);anim=cur===tgt?0:requestAnimationFrame(glide)}
  addEventListener('scroll',function(){if(tick)return;tick=true;requestAnimationFrame(function(){tick=false;thread()})},{passive:true});
  var rz;function rebuild(){clearTimeout(rz);rz=setTimeout(function(){LUT=[];build()},120)}
  addEventListener('resize',rebuild);
  if('ResizeObserver' in window){new ResizeObserver(rebuild).observe(run)}

  counts(document.getElementById('t1'));
  addEventListener('load',build);build();setTimeout(build,800);setTimeout(build,2500);
  /* phone menu */
  document.querySelectorAll('.menu-btn').forEach(function(b){var t=b.closest('.top');b.setAttribute('aria-expanded','false');
    function set(o){t.classList.toggle('open',o);b.setAttribute('aria-expanded',String(o));b.textContent=o?'Close':'Menu'}
    b.addEventListener('click',function(){set(!t.classList.contains('open'))});
    t.querySelectorAll('.tnav a').forEach(function(a){a.addEventListener('click',function(){set(false)})})});
})();
