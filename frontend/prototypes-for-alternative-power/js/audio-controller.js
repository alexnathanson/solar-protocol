
(() => {
  const artworkContainer = document.getElementById('artwork-container');
  const playedFiles = new WeakSet(); // Track which audio files have been played

  // Format time in MM:SS
  function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }

  // Update time display for an audio element
  function updateTimeDisplay(audio, timeDisplay, showElapsed) {
    const duration = formatTime(audio.duration);
    if (showElapsed) {
      const currentTime = formatTime(audio.currentTime);
      timeDisplay.textContent = `${currentTime} / ${duration}`;
    } else {
      timeDisplay.textContent = duration;
    }
  }

  // Initialize duration display and timeupdate listeners for all audio files on load
  document.querySelectorAll('#artwork-container figure').forEach((figure) => {
    const audio = figure.querySelector('audio');
    const timeDisplay = figure.querySelector('.time-display');

    if (audio && timeDisplay) {
      audio.addEventListener('loadedmetadata', () => {
        updateTimeDisplay(audio, timeDisplay, false);
      });
      // Trigger load if already loaded
      if (audio.readyState >= 1) {
        updateTimeDisplay(audio, timeDisplay, false);
      }
      // Single timeupdate listener per audio (avoids leak from repeated click handler)
      audio.addEventListener('timeupdate', () => {
        if (!audio.paused || playedFiles.has(audio)) {
          updateTimeDisplay(audio, timeDisplay, true);
        }
      });
    }
  });

  if (!artworkContainer) return;
  artworkContainer.addEventListener('click', (e) => {
    if (e.target && e.target.closest('button.media-toggle')) {
      const figure = e.target.closest('figure');
      const audio = figure.querySelector('audio');
      const button = figure.querySelector('button.media-toggle');
      const img = button.querySelector('img');
      const timeDisplay = figure.querySelector('.time-display');

      if (audio.paused) {
        // Pause all other audio elements and keep their elapsed time visible
        document.querySelectorAll('#artwork-container audio').forEach((otherAudio) => {
          if (otherAudio !== audio) {
            otherAudio.pause();
            const otherFigure = otherAudio.closest('figure');
            const otherButton = otherFigure.querySelector('button.media-toggle');
            const otherTimeDisplay = otherFigure.querySelector('.time-display');
            if (otherButton) {
              const otherImg = otherButton.querySelector('img');
              otherImg.src = 'https://solarprotocol.net/prototypes-for-alternative-power/basic_img/play.svg';
              otherImg.alt = 'Play';
            }
            if (otherTimeDisplay) {
              // Keep elapsed time visible if this file has been played
              updateTimeDisplay(otherAudio, otherTimeDisplay, playedFiles.has(otherAudio));
            }
          }
        });

        audio.play().catch(function(e) { console.warn('Audio play failed:', e); });
        playedFiles.add(audio); // Mark this audio as played
        img.src = 'https://solarprotocol.net/prototypes-for-alternative-power/basic_img/pause.svg';
        img.alt = 'Pause';

        audio.addEventListener('ended', () => {
          img.src = 'https://solarprotocol.net/prototypes-for-alternative-power/basic_img/play.svg';
          img.alt = 'Play';
          updateTimeDisplay(audio, timeDisplay, true);
        }, { once: true });
      } else {
        audio.pause();
        img.src = 'https://solarprotocol.net/prototypes-for-alternative-power/basic_img/play.svg';
        img.alt = 'Play';
        // Keep elapsed time visible since file has been played
        updateTimeDisplay(audio, timeDisplay, true);
      }
    }
  })
})();