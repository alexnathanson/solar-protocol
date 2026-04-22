
(function() {

// --- Mobile detection (runs immediately) ---
var isMobile = false;
function addMobileClass() {
  if (/Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
    document.body.classList.add('mobile');
    document.body.classList.add('turnOn');
    isMobile = true;
  } else {
    document.body.classList.remove('mobile');
  }
}
addMobileClass();
window.addEventListener('resize', addMobileClass);

// --- Utilities ---
var tick_init = true;

function easeInOutSine(x) {
  return x === 0 ? 0 : Math.pow(2, 10 * x - 10);
}

function map(value, start1, stop1, start2, stop2) {
  return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1));
}

// --- Oval animation dimensions (recomputed on resize) ---
var centerX, centerY, radiusX, radiusY;
var degToRad = function(deg) { return deg * Math.PI / 180; };

function updateOvalDimensions() {
  centerX = window.innerWidth / 2;
  centerY = window.innerHeight * 0.25;
  radiusX = window.innerHeight * 0.5;
  radiusY = window.innerHeight * 0.5;
  var ovalRoute = document.getElementById('ovalRoute');
  if (ovalRoute) {
    ovalRoute.style.width = radiusX * 2 + 'px';
    ovalRoute.style.height = radiusY * 2 + 'px';
    ovalRoute.style.left = centerX + 'px';
    ovalRoute.style.top = centerY + 'px';
  }
}

function animate(angle, elem) {
  var x = centerX + radiusX * Math.cos(degToRad(angle));
  var y = centerY + radiusY * Math.sin(degToRad(angle));
  elem.style.left = x + 'px';
  elem.style.top = y + 'px';
}

// --- Solar Protocol ---
function setTextAll(cls, text) {
  var els = document.getElementsByClassName(cls);
  for (var i = 0; i < els.length; i++) els[i].textContent = text;
}

var V2 = 'https://solarprotocol.net/api/v2/opendata.php';
var V1 = 'https://solarprotocol.net/api/v1/opendata.php';

async function sys(key) {
  var urls = [V2 + '?systemInfo=' + encodeURIComponent(key), V1 + '?systemInfo=' + encodeURIComponent(key)];
  for (var idx = 0; idx < urls.length; idx++) {
    var u = urls[idx];
    try {
      var r = await fetch(u, { cache: 'no-store' });
      if (!r.ok) continue;
      if (u.indexOf('/v2/') !== -1) {
        var j = await r.json();
        var val = (j && (j[key] !== undefined && j[key] !== null ? j[key] : j.value)) || '';
        if (String(val).trim() !== '') return String(val).trim();
      } else {
        var t = (await r.text()).replace(/["\n\r]/g, '').trim();
        if (t) return t;
      }
    } catch (_) {}
  }
  return '';
}

async function fetchVal(key) {
  var urls = [V2 + '?value=' + encodeURIComponent(key), V1 + '?value=' + encodeURIComponent(key)];
  for (var idx = 0; idx < urls.length; idx++) {
    var u = urls[idx];
    try {
      var r = await fetch(u, { cache: 'no-store' });
      if (!r.ok) continue;
      var j = await r.json();
      var v = j[key] !== undefined && j[key] !== null ? j[key] : (j.value !== undefined ? j.value : null);
      if (v != null) return v;
    } catch (_) {}
  }
  return null;
}

var tz = '';

async function boot() {
  var results = await Promise.all([
    sys('name'), sys('location'), sys('city'), sys('country'), fetchVal('battery-percentage')
  ]);
  var name = results[0], location = results[1], city = results[2], country = results[3], bat = results[4];

  var locText = (location && location.trim()) || (city && country ? city + ', ' + country : '');

  setTextAll('sp-name', name || '\u2014');
  setTextAll('sp-loc',  locText || '\u2014');
  if (bat != null) setTextAll('sp-bat', bat*100 + '%');

  tz = await sys('tz') || 'UTC';
  tick();
  setInterval(tick, 1000);

  var ovalImgs = document.getElementsByClassName('ovalDiv_img');
  for (var i = 0; i < ovalImgs.length; i++) ovalImgs[i].classList.add('sp-loaded');

  setInterval(async function() {
    try {
      var r2 = await Promise.all([sys('name'), sys('location'), sys('city'), sys('country')]);
      var n2 = r2[0], l2 = r2[1], c2 = r2[2], co2 = r2[3];
      var loc2 = (l2 && l2.trim()) || (c2 && co2 ? c2 + ', ' + co2 : '');
      setTextAll('sp-name', n2 || '\u2014');
      setTextAll('sp-loc',  loc2 || '\u2014');
      var tz2 = await sys('tz');
      if (tz2) tz = tz2;
    } catch (e) {
      console.warn('[SP] refresh failed', e);
    }
  }, 5 * 60 * 1000);

  window.SP_DEBUG = { name: name, location: locText, battery: bat, tz: tz };
}

function tick() {
  if (!tz) return;

  var parts = new Intl.DateTimeFormat(undefined, {
    timeZone: tz, hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23'
  }).formatToParts(new Date());

  var h = 0, m = 0, s = 0;
  for (var pi = 0; pi < parts.length; pi++) {
    var p = parts[pi];
    if (p.type === 'hour')   h = parseInt(p.value, 10);
    if (p.type === 'minute') m = parseInt(p.value, 10);
    if (p.type === 'second') s = parseInt(p.value, 10);
  }

  setTextAll('sp-time', String(h).padStart(2,'0') + ':' + String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0'));

  var secs  = h * 3600 + m * 60 + s;
  var angle = map(secs, 0, 86400, 0, 360) - 90;

  var sun      = document.getElementsByClassName('ovalDiv_sun')[0];
  var moon     = document.getElementsByClassName('ovalDiv_moon')[0];
  var sun_img  = document.getElementsByClassName('ovalDiv_sun_img')[0];
  var moon_img = document.getElementsByClassName('ovalDiv_moon_img')[0];

  if (secs > 21600 && secs < 64800) {
    var sel = Math.round(map(angle, 0, 180, 20/2, (11-2)*20 - 20/2))+20;
    if((sel>180 || sel<40)){
      sel = sel +20;
    }else if((sel>140 || sel<80)){
      sel = sel +8;
    }
    for (var i = sel; i >= 1; i--) {
      var sml =  ((easeInOutSine((sel - i) / sel)) / 2) * 100/8;
      var barEl = document.querySelector('.bar_' + (sel - i));
      if (barEl) barEl.style.background = 'linear-gradient(0deg, transparent ' + (50 - sml - 5) + '%, black ' + (50 - sml) + '%, black ' + (50 + sml) + '%, transparent ' + (50 + sml + 5) + '%)';
    }
    for (var j = 1; j >= 0; j--) {
      var sml2 = ((easeInOutSine((j) / 20)) / 2) * 100/8/2;
      var barEl2 = document.querySelector('.bar_' + (sel + sel - j));
      if (barEl2) barEl2.style.background = 'linear-gradient(0deg, transparent ' + (50 - sml2 - 5) + '%, black ' + (50 - sml2) + '%, black ' + (50 + sml2) + '%, transparent ' + (50 + sml2 + 5) + '%)';
    }
  }
  if (tick_init) {
    var sunEl = document.querySelector('.ovalDiv_sun');
    var moonEl = document.querySelector('.ovalDiv_moon');
    if ((angle+3600)%360 < 180) { if (sunEl) sunEl.classList.add('shadow'); }
    else { if (moonEl) moonEl.classList.add('shadow'); }
    setTimeout(function() { document.body.classList.add('turnOn'); }, 1000);
    tick_init = false;

    if (sun)      { animate(angle, sun);           sun.classList.add('sp-loaded'); }
    if (moon)     { animate(angle - 180, moon);     moon.classList.add('sp-loaded'); }
    if (sun_img)  { animate(angle, sun_img);        sun_img.classList.add('sp-loaded'); }
    if (moon_img) { animate(angle - 180, moon_img); moon_img.classList.add('sp-loaded'); }
    return;
  }

  if (sun)      animate(angle, sun);
  if (moon)     animate(angle - 180, moon);
  if (sun_img)  animate(angle, sun_img);
  if (moon_img) animate(angle - 180, moon_img);
}

// --- DOMContentLoaded: all DOM-dependent setup ---
document.addEventListener('DOMContentLoaded', function() {

  // Compute oval dimensions after layout
  updateOvalDimensions();
  window.addEventListener('resize', updateOvalDimensions);

  // Boot Solar Protocol
  boot();

  // Generate gradient bars
  for (var i = 11; i >= 1; i--) {
    for (var k = 20; k >= 0; k--) {
      var bar = document.createElement('div');
      bar.className = 'bar bar_' + (k + ((11 - i) * 20));
      var barWrap = document.querySelector('.side_' + i + ' .bar_wrap');
      if (barWrap) barWrap.appendChild(bar);
    }
  }

  // Inactivity timer (hide UI after 30s of no mouse movement)
  var inactivityTimer;

  function startInactivityTimer() {
    inactivityTimer = setTimeout(function() {
      if (!isMobile) {
        document.body.classList.remove('turnOn');
      }
    }, 30000);
  }

  function resetTimer() {
    clearTimeout(inactivityTimer);
    document.body.classList.add('turnOn');
    startInactivityTimer();
  }

  document.addEventListener('mousemove', resetTimer);
  startInactivityTimer();

  // --- Homepage carousel setup ---


  document.querySelectorAll('.side').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_1"><div class="background_image background_image_rimbawan-gerilya"></div></div>');
  });

  document.querySelectorAll('.side').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_2"><div class="background_image background_image_american-artist"></div></div>');
  });

  document.querySelectorAll('.side').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_3"><div class="background_image background_image_ryan-kuo"></div></div>');
  });

  document.querySelectorAll('.side').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_4"><div class="background_image background_image_or-zubalsky"></div></div>');
  });

  document.querySelectorAll('.side').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_5"><div class="background_image background_image_ryan-clarke"></div></div>');
  });

  document.querySelectorAll('.side').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_6"><div class="background_image background_image_morakana"></div></div>');
  });

  document.querySelectorAll('.side').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_7"><div class="background_image background_image_jen-liu"></div></div>');
  });

  document.querySelectorAll('.side').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_8"><div class="background_image background_image_alice-yuan-zhang"></div></div>');
  });

  document.querySelectorAll('.side').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_9"><div class="background_image background_image_herdimas-anggara"></div></div>');
  });

  document.querySelectorAll('.side').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_10"><div class="background_image background_image_chia-amisola"></div></div>');
  });

  document.querySelectorAll('.side').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_11"><div class="background_image background_image_ho-rui-an"></div></div>');
  });

  document.querySelectorAll('.side').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_12"><div class="background_image background_image_bani-haykal"></div></div>');
  });

  document.querySelectorAll('.side').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_13"><div class="background_image background_image_samson-young"></div></div>');
  });

  document.querySelectorAll('.side').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_14"><div class="background_image background_image_solar-protocol"></div></div>');
  });


  document.querySelectorAll('.sidebottom .perspective_wrap').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_1"><div class="background_image background_image_rimbawan-gerilya"></div></div>');
  });

  document.querySelectorAll('.sidebottom .perspective_wrap').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_2"><div class="background_image background_image_american-artist"></div></div>');
  });

  document.querySelectorAll('.sidebottom .perspective_wrap').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_3"><div class="background_image background_image_ryan-kuo"></div></div>');
  });

  document.querySelectorAll('.sidebottom .perspective_wrap').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_4"><div class="background_image background_image_or-zubalsky"></div></div>');
  });

  document.querySelectorAll('.sidebottom .perspective_wrap').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_5"><div class="background_image background_image_ryan-clarke"></div></div>');
  });

  document.querySelectorAll('.sidebottom .perspective_wrap').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_6"><div class="background_image background_image_morakana"></div></div>');
  });

  document.querySelectorAll('.sidebottom .perspective_wrap').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_7"><div class="background_image background_image_jen-liu"></div></div>');
  });

  document.querySelectorAll('.sidebottom .perspective_wrap').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_8"><div class="background_image background_image_alice-yuan-zhang"></div></div>');
  });

  document.querySelectorAll('.sidebottom .perspective_wrap').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_9"><div class="background_image background_image_herdimas-anggara"></div></div>');
  });

  document.querySelectorAll('.sidebottom .perspective_wrap').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_10"><div class="background_image background_image_chia-amisola"></div></div>');
  });

  document.querySelectorAll('.sidebottom .perspective_wrap').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_11"><div class="background_image background_image_ho-rui-an"></div></div>');
  });

  document.querySelectorAll('.sidebottom .perspective_wrap').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_12"><div class="background_image background_image_bani-haykal"></div></div>');
  });

  document.querySelectorAll('.sidebottom .perspective_wrap').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_13"><div class="background_image background_image_samson-young"></div></div>');
  });

  document.querySelectorAll('.sidebottom .perspective_wrap').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '<div class="background_image_wrap background_image_wrap_14"><div class="background_image background_image_solar-protocol"></div></div>');
  });


  function updateBgPosition() {
    var sideEl = document.querySelector('.side');
    if (!sideEl) return;
    var h = sideEl.offsetHeight;
    document.querySelectorAll('.sidebottom .background_image').forEach(function(el) {
      el.style.backgroundPosition = 'center calc(50% - ' + h + 'px)';
    });
  }
  updateBgPosition();
  window.addEventListener('resize', updateBgPosition);

  var scroll_counter = 0;

  function scroll(selected) {
    document.querySelectorAll('.artistname_wrap').forEach(function(el) {
      el.style.transform = 'translateX(' + (7.1428 * selected) + '%)';
    });
  }

  function scroll_img(selected) {
    document.querySelectorAll('.background_image_wrap').forEach(function(el) {
      el.style.transform = 'translateX(' + (7.1428 * (selected - 5)) + '%) translateY(' + (100 * (selected - 5)) + '%)';
    });
  }

  scroll(scroll_counter);
  scroll_img(scroll_counter);

  document.querySelectorAll('.sidetop').forEach(function(el) {
    el.insertAdjacentHTML('beforeend', '\
    <div class="artistname_wrap">\
        <div class="artistname artistname_1">Rimbawan Gerilya</div>\
        <div class="artistname artistname_2">American Artist</div>\
        <div class="artistname artistname_3">Ryan Kuo</div>\
        <div class="artistname artistname_4">Or Zubalsky</div>\
        <div class="artistname artistname_5">Ryan Clarke</div>\
        <div class="artistname artistname_6">MORAKANA</div>\
        <div class="artistname artistname_7">Jen Liu</div>\
        <div class="artistname artistname_8">Alice Yuan Zhang</div>\
        <div class="artistname artistname_9">Herdimas Anggara</div>\
        <div class="artistname artistname_10">Chia Amisola</div>\
        <div class="artistname artistname_11">Ho Rui An</div>\
        <div class="artistname artistname_12">Bani Haykal</div>\
        <div class="artistname artistname_13">Samson Young</div>\
        <div class="artistname artistname_14">Solar Protocol</div>\
        \
    </div>\
    ');
  });

  document.querySelectorAll('.barhide').forEach(function(el) {
    el.addEventListener('mouseenter', function(){
      document.querySelectorAll('.bar').forEach(function(b){ b.style.opacity = '0'; });
    });
    el.addEventListener('mouseleave', function(){
      document.querySelectorAll('.bar').forEach(function(b){ b.style.opacity = '1'; });
    });
  });

  document.querySelectorAll('.sidetop').forEach(function(el) {
    el.addEventListener('mouseenter', function(){
      document.querySelectorAll('.sidetop').forEach(function(st){ st.classList.remove('sidetop_hovered'); });
      this.classList.add('sidetop_hovered');
      var selected = parseInt(this.className.split('side_')[1].split(' ')[0]);
      scroll_img(6 - selected + scroll_counter);
    });
    el.addEventListener('mouseleave', function(){
      this.classList.remove('sidetop_hovered');
      var side6 = document.querySelector('.sidetop.side_6');
      if (side6) side6.classList.add('sidetop_hovered');
      scroll_img(scroll_counter);
    });
  });


  (function(){
    var els = document.querySelectorAll('.side_1 .background_image_wrap');
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.setAttribute('aria-label', 'Rimbawan Gerilya');
      el.addEventListener('click', function() { window.location.href = 'detail/rimbawan-gerilya.html'; });
    });
  })();

  (function(){
    var els = document.querySelectorAll('.side_2 .background_image_wrap');
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.setAttribute('aria-label', 'American Artist');
      el.addEventListener('click', function() { window.location.href = 'detail/american-artist.html'; });
    });
  })();

  (function(){
    var els = document.querySelectorAll('.side_3 .background_image_wrap');
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.setAttribute('aria-label', 'Ryan Kuo');
      el.addEventListener('click', function() { window.location.href = 'detail/ryan-kuo.html'; });
    });
  })();

  (function(){
    var els = document.querySelectorAll('.side_4 .background_image_wrap');
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.setAttribute('aria-label', 'Or Zubalsky');
      el.addEventListener('click', function() { window.location.href = 'detail/or-zubalsky.html'; });
    });
  })();

  (function(){
    var els = document.querySelectorAll('.side_5 .background_image_wrap');
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.setAttribute('aria-label', 'Ryan Clarke');
      el.addEventListener('click', function() { window.location.href = 'detail/ryan-clarke.html'; });
    });
  })();

  (function(){
    var els = document.querySelectorAll('.side_6 .background_image_wrap');
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.setAttribute('aria-label', 'MORAKANA');
      el.addEventListener('click', function() { window.location.href = 'detail/morakana.html'; });
    });
  })();

  (function(){
    var els = document.querySelectorAll('.side_7 .background_image_wrap');
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.setAttribute('aria-label', 'Jen Liu');
      el.addEventListener('click', function() { window.location.href = 'detail/jen-liu.html'; });
    });
  })();

  (function(){
    var els = document.querySelectorAll('.side_8 .background_image_wrap');
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.setAttribute('aria-label', 'Alice Yuan Zhang');
      el.addEventListener('click', function() { window.location.href = 'detail/alice-yuan-zhang.html'; });
    });
  })();

  (function(){
    var els = document.querySelectorAll('.side_9 .background_image_wrap');
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.setAttribute('aria-label', 'Herdimas Anggara');
      el.addEventListener('click', function() { window.location.href = 'detail/herdimas-anggara.html'; });
    });
  })();

  (function(){
    var els = document.querySelectorAll('.side_10 .background_image_wrap');
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.setAttribute('aria-label', 'Chia Amisola');
      el.addEventListener('click', function() { window.location.href = 'detail/chia-amisola.html'; });
    });
  })();

  (function(){
    var els = document.querySelectorAll('.side_11 .background_image_wrap');
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.setAttribute('aria-label', 'Ho Rui An');
      el.addEventListener('click', function() { window.location.href = 'detail/ho-rui-an.html'; });
    });
  })();

  (function(){
    var els = document.querySelectorAll('.side_12 .background_image_wrap');
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.setAttribute('aria-label', 'Bani Haykal');
      el.addEventListener('click', function() { window.location.href = 'detail/bani-haykal.html'; });
    });
  })();

  (function(){
    var els = document.querySelectorAll('.side_13 .background_image_wrap');
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.setAttribute('aria-label', 'Samson Young');
      el.addEventListener('click', function() { window.location.href = 'detail/samson-young.html'; });
    });
  })();

  (function(){
    var els = document.querySelectorAll('.side_14 .background_image_wrap');
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.setAttribute('aria-label', 'Solar Protocol');
      el.addEventListener('click', function() { window.location.href = 'detail/solar-protocol.html'; });
    });
  })();



  (function(){
    var idx = 1;
    var els = document.querySelectorAll('.artistname_' + idx);
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.addEventListener('click', function() { window.location.href = 'detail/rimbawan-gerilya.html'; });
      el.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    });
    // Only make the center panel (side_6) artist names tabbable
    var primary = document.querySelector('.sidetop.side_6 .artistname_' + idx);
    if (primary) {
      primary.setAttribute('tabindex', '' + (idx + 3));
      primary.addEventListener('focus', function() {
        // Reset browser auto-scroll on the container — we position via transforms
        var parent = this.closest('.sidetop');
        if (parent) parent.scrollLeft = 0;
        var wrap = this.closest('.artistname_wrap');
        if (wrap) wrap.scrollLeft = 0;
        scroll_counter = applyScroll(6 - idx);
      });
    }
  })();

  (function(){
    var idx = 2;
    var els = document.querySelectorAll('.artistname_' + idx);
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.addEventListener('click', function() { window.location.href = 'detail/american-artist.html'; });
      el.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    });
    // Only make the center panel (side_6) artist names tabbable
    var primary = document.querySelector('.sidetop.side_6 .artistname_' + idx);
    if (primary) {
      primary.setAttribute('tabindex', '' + (idx + 3));
      primary.addEventListener('focus', function() {
        // Reset browser auto-scroll on the container — we position via transforms
        var parent = this.closest('.sidetop');
        if (parent) parent.scrollLeft = 0;
        var wrap = this.closest('.artistname_wrap');
        if (wrap) wrap.scrollLeft = 0;
        scroll_counter = applyScroll(6 - idx);
      });
    }
  })();

  (function(){
    var idx = 3;
    var els = document.querySelectorAll('.artistname_' + idx);
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.addEventListener('click', function() { window.location.href = 'detail/ryan-kuo.html'; });
      el.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    });
    // Only make the center panel (side_6) artist names tabbable
    var primary = document.querySelector('.sidetop.side_6 .artistname_' + idx);
    if (primary) {
      primary.setAttribute('tabindex', '' + (idx + 3));
      primary.addEventListener('focus', function() {
        // Reset browser auto-scroll on the container — we position via transforms
        var parent = this.closest('.sidetop');
        if (parent) parent.scrollLeft = 0;
        var wrap = this.closest('.artistname_wrap');
        if (wrap) wrap.scrollLeft = 0;
        scroll_counter = applyScroll(6 - idx);
      });
    }
  })();

  (function(){
    var idx = 4;
    var els = document.querySelectorAll('.artistname_' + idx);
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.addEventListener('click', function() { window.location.href = 'detail/or-zubalsky.html'; });
      el.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    });
    // Only make the center panel (side_6) artist names tabbable
    var primary = document.querySelector('.sidetop.side_6 .artistname_' + idx);
    if (primary) {
      primary.setAttribute('tabindex', '' + (idx + 3));
      primary.addEventListener('focus', function() {
        // Reset browser auto-scroll on the container — we position via transforms
        var parent = this.closest('.sidetop');
        if (parent) parent.scrollLeft = 0;
        var wrap = this.closest('.artistname_wrap');
        if (wrap) wrap.scrollLeft = 0;
        scroll_counter = applyScroll(6 - idx);
      });
    }
  })();

  (function(){
    var idx = 5;
    var els = document.querySelectorAll('.artistname_' + idx);
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.addEventListener('click', function() { window.location.href = 'detail/ryan-clarke.html'; });
      el.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    });
    // Only make the center panel (side_6) artist names tabbable
    var primary = document.querySelector('.sidetop.side_6 .artistname_' + idx);
    if (primary) {
      primary.setAttribute('tabindex', '' + (idx + 3));
      primary.addEventListener('focus', function() {
        // Reset browser auto-scroll on the container — we position via transforms
        var parent = this.closest('.sidetop');
        if (parent) parent.scrollLeft = 0;
        var wrap = this.closest('.artistname_wrap');
        if (wrap) wrap.scrollLeft = 0;
        scroll_counter = applyScroll(6 - idx);
      });
    }
  })();

  (function(){
    var idx = 6;
    var els = document.querySelectorAll('.artistname_' + idx);
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.addEventListener('click', function() { window.location.href = 'detail/morakana.html'; });
      el.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    });
    // Only make the center panel (side_6) artist names tabbable
    var primary = document.querySelector('.sidetop.side_6 .artistname_' + idx);
    if (primary) {
      primary.setAttribute('tabindex', '' + (idx + 3));
      primary.addEventListener('focus', function() {
        // Reset browser auto-scroll on the container — we position via transforms
        var parent = this.closest('.sidetop');
        if (parent) parent.scrollLeft = 0;
        var wrap = this.closest('.artistname_wrap');
        if (wrap) wrap.scrollLeft = 0;
        scroll_counter = applyScroll(6 - idx);
      });
    }
  })();

  (function(){
    var idx = 7;
    var els = document.querySelectorAll('.artistname_' + idx);
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.addEventListener('click', function() { window.location.href = 'detail/jen-liu.html'; });
      el.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    });
    // Only make the center panel (side_6) artist names tabbable
    var primary = document.querySelector('.sidetop.side_6 .artistname_' + idx);
    if (primary) {
      primary.setAttribute('tabindex', '' + (idx + 3));
      primary.addEventListener('focus', function() {
        // Reset browser auto-scroll on the container — we position via transforms
        var parent = this.closest('.sidetop');
        if (parent) parent.scrollLeft = 0;
        var wrap = this.closest('.artistname_wrap');
        if (wrap) wrap.scrollLeft = 0;
        scroll_counter = applyScroll(6 - idx);
      });
    }
  })();

  (function(){
    var idx = 8;
    var els = document.querySelectorAll('.artistname_' + idx);
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.addEventListener('click', function() { window.location.href = 'detail/alice-yuan-zhang.html'; });
      el.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    });
    // Only make the center panel (side_6) artist names tabbable
    var primary = document.querySelector('.sidetop.side_6 .artistname_' + idx);
    if (primary) {
      primary.setAttribute('tabindex', '' + (idx + 3));
      primary.addEventListener('focus', function() {
        // Reset browser auto-scroll on the container — we position via transforms
        var parent = this.closest('.sidetop');
        if (parent) parent.scrollLeft = 0;
        var wrap = this.closest('.artistname_wrap');
        if (wrap) wrap.scrollLeft = 0;
        scroll_counter = applyScroll(6 - idx);
      });
    }
  })();

  (function(){
    var idx = 9;
    var els = document.querySelectorAll('.artistname_' + idx);
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.addEventListener('click', function() { window.location.href = 'detail/herdimas-anggara.html'; });
      el.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    });
    // Only make the center panel (side_6) artist names tabbable
    var primary = document.querySelector('.sidetop.side_6 .artistname_' + idx);
    if (primary) {
      primary.setAttribute('tabindex', '' + (idx + 3));
      primary.addEventListener('focus', function() {
        // Reset browser auto-scroll on the container — we position via transforms
        var parent = this.closest('.sidetop');
        if (parent) parent.scrollLeft = 0;
        var wrap = this.closest('.artistname_wrap');
        if (wrap) wrap.scrollLeft = 0;
        scroll_counter = applyScroll(6 - idx);
      });
    }
  })();

  (function(){
    var idx = 10;
    var els = document.querySelectorAll('.artistname_' + idx);
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.addEventListener('click', function() { window.location.href = 'detail/chia-amisola.html'; });
      el.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    });
    // Only make the center panel (side_6) artist names tabbable
    var primary = document.querySelector('.sidetop.side_6 .artistname_' + idx);
    if (primary) {
      primary.setAttribute('tabindex', '' + (idx + 3));
      primary.addEventListener('focus', function() {
        // Reset browser auto-scroll on the container — we position via transforms
        var parent = this.closest('.sidetop');
        if (parent) parent.scrollLeft = 0;
        var wrap = this.closest('.artistname_wrap');
        if (wrap) wrap.scrollLeft = 0;
        scroll_counter = applyScroll(6 - idx);
      });
    }
  })();

  (function(){
    var idx = 11;
    var els = document.querySelectorAll('.artistname_' + idx);
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.addEventListener('click', function() { window.location.href = 'detail/ho-rui-an.html'; });
      el.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    });
    // Only make the center panel (side_6) artist names tabbable
    var primary = document.querySelector('.sidetop.side_6 .artistname_' + idx);
    if (primary) {
      primary.setAttribute('tabindex', '' + (idx + 3));
      primary.addEventListener('focus', function() {
        // Reset browser auto-scroll on the container — we position via transforms
        var parent = this.closest('.sidetop');
        if (parent) parent.scrollLeft = 0;
        var wrap = this.closest('.artistname_wrap');
        if (wrap) wrap.scrollLeft = 0;
        scroll_counter = applyScroll(6 - idx);
      });
    }
  })();

  (function(){
    var idx = 12;
    var els = document.querySelectorAll('.artistname_' + idx);
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.addEventListener('click', function() { window.location.href = 'detail/bani-haykal.html'; });
      el.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    });
    // Only make the center panel (side_6) artist names tabbable
    var primary = document.querySelector('.sidetop.side_6 .artistname_' + idx);
    if (primary) {
      primary.setAttribute('tabindex', '' + (idx + 3));
      primary.addEventListener('focus', function() {
        // Reset browser auto-scroll on the container — we position via transforms
        var parent = this.closest('.sidetop');
        if (parent) parent.scrollLeft = 0;
        var wrap = this.closest('.artistname_wrap');
        if (wrap) wrap.scrollLeft = 0;
        scroll_counter = applyScroll(6 - idx);
      });
    }
  })();

  (function(){
    var idx = 13;
    var els = document.querySelectorAll('.artistname_' + idx);
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.addEventListener('click', function() { window.location.href = 'detail/samson-young.html'; });
      el.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    });
    // Only make the center panel (side_6) artist names tabbable
    var primary = document.querySelector('.sidetop.side_6 .artistname_' + idx);
    if (primary) {
      primary.setAttribute('tabindex', '' + (idx + 3));
      primary.addEventListener('focus', function() {
        // Reset browser auto-scroll on the container — we position via transforms
        var parent = this.closest('.sidetop');
        if (parent) parent.scrollLeft = 0;
        var wrap = this.closest('.artistname_wrap');
        if (wrap) wrap.scrollLeft = 0;
        scroll_counter = applyScroll(6 - idx);
      });
    }
  })();

  (function(){
    var idx = 14;
    var els = document.querySelectorAll('.artistname_' + idx);
    els.forEach(function(el){
      el.setAttribute('role', 'link');
      el.addEventListener('click', function() { window.location.href = 'detail/solar-protocol.html'; });
      el.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    });
    // Only make the center panel (side_6) artist names tabbable
    var primary = document.querySelector('.sidetop.side_6 .artistname_' + idx);
    if (primary) {
      primary.setAttribute('tabindex', '' + (idx + 3));
      primary.addEventListener('focus', function() {
        // Reset browser auto-scroll on the container — we position via transforms
        var parent = this.closest('.sidetop');
        if (parent) parent.scrollLeft = 0;
        var wrap = this.closest('.artistname_wrap');
        if (wrap) wrap.scrollLeft = 0;
        scroll_counter = applyScroll(6 - idx);
      });
    }
  })();


  document.querySelectorAll('.artistname_3').forEach(function(el){
    el.addEventListener('click', function(){
      var popup = document.querySelector('.popup_3');
      if (popup) popup.style.display = 'block';
    });
  });
  document.querySelectorAll('.close').forEach(function(el){
    el.addEventListener('click', function(){
      this.parentElement.style.display = 'none';
    });
    el.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); this.click(); }
    });
  });
  document.querySelectorAll('.learn-more-link').forEach(function(el){
    el.addEventListener('click', function(e){
      e.preventDefault();
      var popup = document.querySelector('.popup_learnmore');
      if (popup) popup.style.display = 'block';
    });
  });

  // Scroll bounds
  var MIN_COUNTER = -8;
  var MAX_COUNTER = 5;

  function applyScroll(counter) {
    if (counter < MIN_COUNTER) counter = MIN_COUNTER;
    if (counter > MAX_COUNTER) counter = MAX_COUNTER;
    scroll(counter);
    scroll_img(counter);
    return counter;
  }

  document.querySelectorAll('.arrow_r').forEach(function(el){
    el.addEventListener('click', function(){
      scroll_counter--;
      scroll_counter = applyScroll(scroll_counter);
    });
    el.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
    });
  });
  document.querySelectorAll('.arrow_l').forEach(function(el){
    el.addEventListener('click', function(){
      scroll_counter++;
      scroll_counter = applyScroll(scroll_counter);
    });
    el.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
    });
  });

  // Keyboard navigation for carousel
  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight') {
      scroll_counter--;
      scroll_counter = applyScroll(scroll_counter);
    } else if (e.key === 'ArrowLeft') {
      scroll_counter++;
      scroll_counter = applyScroll(scroll_counter);
    }
  });

  // Swipe support (mobile-friendly)
  (function attachSwipe(areaSelector){
    var area = document.querySelector(areaSelector);
    if (!area) return;
    var SWIPE_PX = 40;
    var SWIPE_MS = 600;

    var startX = 0, startY = 0, startT = 0, activeId = null;

    area.addEventListener('pointerdown', function(e){
      if (e.pointerType === 'mouse' && e.buttons !== 1) return;
      activeId = e.pointerId;
      startX = e.clientX;
      startY = e.clientY;
      startT = performance.now();
    });

    area.addEventListener('pointerup', handleEnd);
    area.addEventListener('pointercancel', handleEnd);

    function handleEnd(e) {
      if (e.pointerId !== activeId) return;
      activeId = null;

      var dt = performance.now() - startT;
      if (dt > SWIPE_MS) return;

      var dx = e.clientX - startX;
      var dy = e.clientY - startY;

      if (Math.abs(dx) < SWIPE_PX || Math.abs(dx) <= Math.abs(dy)) return;

      if (dx < 0) {
        scroll_counter--;
      } else {
        scroll_counter++;
      }
      scroll_counter = applyScroll(scroll_counter);
    }
  })('body');

});

})();
