(() => {
'use strict';
const hero = document.getElementById('hero');
function showFallback() {
  document.getElementById('artwork').hidden = true;
  document.getElementById('fallback').hidden = false;
}
hero.addEventListener('error', showFallback);
if (hero.complete && hero.naturalWidth === 0) showFallback();
document.getElementById('search-button').addEventListener('click', () => {
  document.getElementById('search-result').textContent = 'Search action reached. This is a local fixture.';
});
// Exact, reviewed local SVG; this is not a parser for arbitrary user assets.
fetch('search.svg').then(response => {
  if (!response.ok) throw new Error('Icon source unavailable');
  return response.text();
}).then(text => {
  const svg = new DOMParser().parseFromString(text, 'image/svg+xml').documentElement;
  if (svg.localName !== 'svg' || svg.querySelector('script, foreignObject, image')) throw new Error('Unexpected fixture source');
  svg.setAttribute('aria-hidden', 'true');
  svg.setAttribute('focusable', 'false');
  for (const size of [16, 24, 32, 48]) {
    const cell = document.createElement('div'); cell.className = 'icon-specimen';
    const copy = svg.cloneNode(true); copy.setAttribute('width', size); copy.setAttribute('height', size);
    const label = document.createElement('span'); label.textContent = `${size}px`;
    cell.append(copy, label); document.getElementById('icon-sizes').append(cell);
  }
  document.getElementById('action-icon').append(svg.cloneNode(true));
  document.documentElement.dataset.iconsReady = 'true';
}).catch(error => { document.getElementById('search-result').textContent = error.message; });
const stage = document.getElementById('motion-stage');
const button = document.getElementById('motion-toggle');
const preference = matchMedia('(prefers-reduced-motion: reduce)');
let userPaused = false;
let inView = false;
function updateMotion() {
  const running = !userPaused && inView && !document.hidden && !preference.matches;
  stage.dataset.running = String(running);
  button.setAttribute('aria-pressed', String(userPaused));
  button.textContent = userPaused ? 'Resume motion' : 'Pause motion';
  button.disabled = preference.matches;
  document.getElementById('motion-status').textContent = preference.matches ? 'Static equivalent · reduced-motion preference' : running ? 'Motion running' : 'Motion paused';
}
button.addEventListener('click', () => { userPaused = !userPaused; updateMotion(); });
preference.addEventListener('change', updateMotion);
document.addEventListener('visibilitychange', updateMotion);
new IntersectionObserver(entries => { inView = entries[0].isIntersecting; updateMotion(); }).observe(stage);
updateMotion();

})();
