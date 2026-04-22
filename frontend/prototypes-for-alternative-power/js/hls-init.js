/**
 * Shared HLS initialization for video/audio elements.
 * Requires hls.min.js to be loaded first.
 *
 * Usage:
 *   initHls(document.getElementById('my-video'));
 *   initHls(src, element).then(...);
 */
window.initHls = function initHls(srcOrEl, el) {
  // Support two calling conventions:
  //   initHls(element)       — reads src from <source> child
  //   initHls(src, element)  — explicit source URL
  var src, element;
  if (typeof srcOrEl === 'string') {
    src = srcOrEl;
    element = el;
  } else {
    element = srcOrEl;
    if (!element) return Promise.reject();
    var source = element.querySelector('source');
    if (!source) return Promise.reject();
    src = source.src;
  }

  if (!element) return Promise.reject();

  return new Promise(function(resolve, reject) {
    if (element.canPlayType('application/vnd.apple.mpegurl')) {
      element.src = src;
      element.addEventListener('loadedmetadata', function() { resolve(); }, { once: true });
      element.addEventListener('error', function() { reject(); }, { once: true });
    } else if (typeof Hls !== 'undefined' && Hls.isSupported()) {
      var hls = new Hls();
      hls.loadSource(src);
      hls.attachMedia(element);
      hls.on(Hls.Events.MANIFEST_PARSED, function() { resolve(hls); });
      hls.on(Hls.Events.ERROR, function(ev, data) {
        if (data.fatal) { hls.destroy(); reject(); }
      });
    } else {
      reject();
    }
  });
};
