
const artworkVideo = document.getElementById('artwork-video');
const lectureVideo = document.getElementById('lecture-video');

if (!artworkVideo || !lectureVideo) {
  console.warn('[two-channel] Missing video element(s), sync disabled');
} else {
  init();
}

function init() {

function syncPlayPause(source, target) {
  source.addEventListener('play', () => {
    if (target.paused) target.play().catch(function() {});
  });
  source.addEventListener('pause', () => {
    if (!target.paused) target.pause();
  });
}

function syncTimeUpdate(source, target) {
  let seeking = false;

  source.addEventListener('seeking', () => {
    seeking = true;
    target.currentTime = source.currentTime;
  });

  source.addEventListener('seeked', () => {
    lastSeeked = Date.now();
    seeking = false;
  });

  let lastSync = 0;
  let lastSeeked = 0;
  const POST_SEEK_COOLDOWN = 2000;

  source.addEventListener('timeupdate', () => {
    requestAnimationFrame(() => {
      const now = Date.now();
      if (seeking) return;
      if (now - lastSeeked < POST_SEEK_COOLDOWN) return;
      if (Math.abs(target.currentTime - source.currentTime) > 1 && (now - lastSync > 300)) {
        target.currentTime = source.currentTime;
        lastSync = now;
      }
    });
  });
}

// Sync both ways
syncPlayPause(artworkVideo, lectureVideo);
syncTimeUpdate(artworkVideo, lectureVideo);

} // end init
