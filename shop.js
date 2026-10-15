(function(){
  /* phone menu (same as the home page) */
  document.querySelectorAll('.menu-btn').forEach(function(b){var t=b.closest('.top');b.setAttribute('aria-expanded','false');
    function set(o){t.classList.toggle('open',o);b.setAttribute('aria-expanded',String(o));b.textContent=o?'Close':'Menu'}
    b.addEventListener('click',function(){set(!t.classList.contains('open'))});
    t.querySelectorAll('.tnav a').forEach(function(a){a.addEventListener('click',function(){set(false)})})});
})();
