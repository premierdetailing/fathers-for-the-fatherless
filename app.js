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


  /* the gold thread: finds every two-column section, runs down the gap between the columns, then flows out in a wide rounded loop through the empty space between sections and back in; ends on the logo */
  var run=document.getElementById('run1'),svg=run.querySelector('.thread'),base=svg.querySelector('.base'),fill=svg.querySelector('.fill'),ng=svg.querySelector('.nodes'),L=0,dots=[],tick=false,NS='http://www.w3.org/2000/svg';
  var STOPS=['.kids-in','.mission-in','.found-in','.lead-in','.ch-in','.song-in'],BOX='img,video,.three li';
  (function(){var d=document.createElementNS(NS,'defs');d.innerHTML='<linearGradient id="fftf-tg" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="760" spreadMethod="reflect"><stop offset="0" stop-color="#D38D2C"/><stop offset=".4" stop-color="#F2C266"/><stop offset=".7" stop-color="#E8A33B"/><stop offset="1" stop-color="#C98428"/></linearGradient><filter id="fftf-tb" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3.2"/></filter>';svg.insertBefore(d,svg.firstChild);
    var g=document.createElementNS(NS,'path');g.setAttribute('class','glow');svg.insertBefore(g,fill)})();
  var glow=svg.querySelector('.glow');
  function R(el){return el.getBoundingClientRect()}
  function Q(s){return run.querySelector(s)}
  function bgOf(el){while(el&&el!==document.documentElement){var c=getComputedStyle(el).backgroundColor;if(c&&c!=='transparent'&&!/,\s*0\)$/.test(c))return c;el=el.parentElement}return '#F6F1E6'}
  function f(n){return n.toFixed(1)}
  function ext(el){var b={l:1e9,r:-1e9,t:1e9,b:-1e9};function add(q){if(q.width<1||q.height<1)return;b.l=Math.min(b.l,q.left);b.r=Math.max(b.r,q.right);b.t=Math.min(b.t,q.top);b.b=Math.max(b.b,q.bottom)}
    var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),n,rg=document.createRange();while(n=w.nextNode()){if(!n.nodeValue.trim())continue;rg.selectNodeContents(n);[].forEach.call(rg.getClientRects(),add)}
    [].forEach.call(el.querySelectorAll(BOX),function(e){add(R(e))});if(el.matches(BOX))add(R(el));return b}
  function geo(rr){
    /* one steady wave: x = centre(y) + A*sin(2*pi*y/wavelength). The centre holds in each column gap and eases (smootherstep) to the next gap between sections, so the wave never crosses text. */
    var W=rr.width,mob=innerWidth<=860,K=[],marks=[],A,lam,endY;
    function hold(y0,y1,x){K.push({y0:y0-rr.top,y1:y1-rr.top,x:x-rr.left})}
    function mark(y,el){marks.push({y:y-rr.top,el:el})}
    var grids=STOPS.map(Q).filter(Boolean);
    if(mob){
      var w=Q('.kids .wrap'),x=R(w).left+parseFloat(getComputedStyle(w).paddingLeft)-22;A=6;lam=230;
      grids.concat([Q('.tab .frame'),Q('.shop-in')]).forEach(function(el){var b=R(el);hold(b.top,b.bottom,x);mark(b.top+14,el)});
      var sb=R(Q('.give .seal'));hold(sb.top,sb.top,x);mark(sb.top+sb.height/2,Q('.give'));endY=sb.top+sb.height/2-rr.top;
    }else{
      var half=1e9;lam=320;
      grids.forEach(function(g){var k=g.children,a=ext(k[0]),b=ext(k[1]),gb=R(g),top=Math.max(a.t,b.t),bot=Math.min(a.b,b.b);
        half=Math.min(half,(b.l-a.r)/2);hold(gb.top,gb.bottom,(a.r+b.l)/2);mark(bot>top?(top+bot)/2:gb.top+gb.height/2,g)});
      var fr=R(Q('.tab .frame')),ts=R(Q('.tab')),ty=fr.top-(fr.top-ts.top)*.42;hold(ty,ty,rr.left+W/2);mark(ty,Q('.tab'));
      var rp=R(Q('.tab .row p')),ry=rp.top+rp.height/2;hold(ry,ry,Math.min(rr.left+W-40,Math.max(rp.right+70,rr.left+W*.74)));
      var card=Q('.shop-in'),cb=R(card);hold(cb.top+24,cb.bottom-24,(R(card.querySelector('p:not(.kick)')).right+cb.right)/2);mark(cb.top+cb.height/2,card);
      var seal=R(Q('.give .seal')),gy=seal.top-10;hold(gy,gy,seal.left+seal.width/2);mark(gy,Q('.give'));endY=gy-rr.top;
      A=Math.max(10,Math.min(26,half-14));
    }
    function cx(y){if(y<=K[0].y1)return K[0].x;for(var i=0;i<K.length-1;i++){var a=K[i],b=K[i+1];if(y<=b.y0){if(y<=a.y1)return a.x;var t=(y-a.y1)/Math.max(1,b.y0-a.y1),s=t*t*t*(t*(t*6-15)+10);return a.x+(b.x-a.x)*s}}return K[K.length-1].x}
    function xAt(y){var fade=Math.max(0,Math.min(1,(endY-y)/160));return cx(y)+A*fade*Math.sin(2*Math.PI*y/lam)}
    var d='',step=4;for(var y=0;y<endY;y+=step){d+=(y?' L':'M')+f(xAt(y))+','+f(y)}d+=' L'+f(xAt(endY))+','+f(endY);
    var nodes=marks.map(function(m){return {x:xAt(m.y),y:m.y,bg:bgOf(m.el),dot:true}});
    return {d:d,nodes:nodes};
  }
  function build(){
    var rr=R(run),W=rr.width,H=run.scrollHeight;svg.setAttribute('width',W);svg.setAttribute('height',H);svg.setAttribute('viewBox','0 0 '+W+' '+H);
    var g=geo(rr);base.setAttribute('d',g.d);fill.setAttribute('d',g.d);glow.setAttribute('d',g.d);L=fill.getTotalLength();fill.style.strokeDasharray=L;glow.style.strokeDasharray=L;LUT=[];
    while(ng.firstChild)ng.removeChild(ng.firstChild);dots=[];
    g.nodes.forEach(function(p){function C(cls,r){var c=document.createElementNS(NS,'circle');c.setAttribute('class',cls);c.setAttribute('cx',p.x);c.setAttribute('cy',p.y);c.setAttribute('r',r);ng.appendChild(c);return c}
      var h=C('halo',18),ri=C('ring',12),c=C('nd',6);c.style.fill=p.bg;dots.push({y:p.y,h:h,c:c,r:ri})});
    thread();
  }
  var LUT=[];
  function lut(){LUT=[];var n=600;for(var i=0;i<=n;i++){var q=fill.getPointAtLength(L*i/n);LUT.push(q.y)}}
  function thread(){
    if(!L)return;
    if(LUT.length!==601)lut();
    var r=R(run),line=innerHeight*.6,y=line-r.top,p;
    if(reduce)p=1;else{var lo=0;for(var i=0;i<=600;i++){if(LUT[i]<=y)lo=i;else break}p=lo/600}
    if(scrollY+innerHeight>=document.documentElement.scrollHeight-4)p=1;
    tgt=p;if(reduce){cur=p;fill.style.strokeDashoffset=0;glow.style.strokeDashoffset=0}else if(!anim){anim=requestAnimationFrame(glide)}
    dots.forEach(function(d){var on=reduce||(r.top+d.y)<line+1;d.c.classList.toggle('on',on);d.h.classList.toggle('on',on);d.r.classList.toggle('on',on)});
  }
  var cur=0,tgt=0,anim=0;
  function glide(){var dlt=tgt-cur;cur=Math.abs(dlt)<.0004?tgt:cur+dlt*.08;var o=L*(1-cur);fill.style.strokeDashoffset=o;glow.style.strokeDashoffset=o;anim=cur===tgt?0:requestAnimationFrame(glide)}
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
  /* header bar: sticks once you scroll, shows how far down the page you are, marks the section you're in */
  (function(){var top=document.querySelector('.t1 .top');if(!top)return;var wrap=top.parentElement,pr=document.createElement('i');pr.className='prog';pr.setAttribute('aria-hidden','true');top.appendChild(pr);
    var home=top.querySelector('.tnav a[href="#"]'),on=false,limit=0;
    function measure(){if(!on)limit=top.offsetTop+top.offsetHeight+60}
    function upd(){var y=scrollY,s=y>limit;if(s!==on){on=s;if(s){wrap.style.paddingTop=(parseFloat(getComputedStyle(wrap).paddingTop)||0)+top.offsetHeight+'px';top.classList.add('stuck')}else{top.classList.remove('stuck');wrap.style.paddingTop=''}}
      var h=document.documentElement.scrollHeight-innerHeight;top.style.setProperty('--sp',h>0?Math.min(1,y/h).toFixed(4):0)}
    measure();addEventListener('resize',measure);var tk=false;addEventListener('scroll',function(){if(tk)return;tk=true;requestAnimationFrame(function(){tk=false;upd()})},{passive:true});upd();
    var links=[].slice.call(top.querySelectorAll('.tnav a[href^="#"]')).filter(function(a){var h=a.getAttribute('href');return h.length>1&&document.querySelector(h)});
    if(links.length&&'IntersectionObserver' in window){var seen=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;links.forEach(function(a){if(a.getAttribute('href')==='#'+e.target.id)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')});if(home)home.removeAttribute('aria-current')})},{rootMargin:'-45% 0px -50% 0px'});
      links.forEach(function(a){seen.observe(document.querySelector(a.getAttribute('href')))});
      addEventListener('scroll',function(){if(scrollY<limit&&home){home.setAttribute('aria-current','page');links.forEach(function(a){a.removeAttribute('aria-current')})}},{passive:true})}
  })();
})();
