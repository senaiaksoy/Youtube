const SKINS = {
  tr: {
    title: "Tüp Bebekte Doğru Bilgi",
    identity: "Dr. Senai Aksoy | Üreme Sağlığı",
    site: "tupbebek.com",
    lang: "tr"
  },
  fr: {
    title: "Comprendre la FIV avec clarté",
    identity: "Dr. Senai Aksoy | FIV à Istanbul",
    site: "draksoyivf.com",
    lang: "fr"
  }
};

const BEATS = [
  { start: 0, end: 3, label: "Brand Field" },
  { start: 3, end: 8, label: "Main Title" },
  { start: 8, end: 12, label: "Identity Line" },
  { start: 12, end: 15, label: "Transition Out" }
];

const body = document.body;
const title = document.querySelector("[data-title]");
const identity = document.querySelector("[data-identity]");
const site = document.querySelector("[data-site]");
const stage = document.querySelector("[data-stage]");
const timeLabel = document.querySelector("[data-time-label]");
const skinButtons = [...document.querySelectorAll("[data-skin-button]")];
const replayButton = document.querySelector("[data-replay]");

let animationStartedAt = performance.now();
let timeLabelFrame = 0;

function applySkin(skinName) {
  const skin = SKINS[skinName] || SKINS.tr;

  body.dataset.skin = skinName in SKINS ? skinName : "tr";
  document.documentElement.lang = skin.lang;
  title.textContent = skin.title;
  identity.textContent = skin.identity;
  site.textContent = skin.site;

  skinButtons.forEach((button) => {
    const isActive = button.dataset.skinButton === body.dataset.skin;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });

  replay();
}

function replay() {
  animationStartedAt = performance.now();
  window.cancelAnimationFrame(timeLabelFrame);
  stage.classList.add("is-replaying");
  void stage.offsetWidth;

  window.requestAnimationFrame(() => {
    stage.classList.remove("is-replaying");
    updateTimeLabel();
  });
}

function updateTimeLabel() {
  const elapsedSeconds = Math.min((performance.now() - animationStartedAt) / 1000, 14.999);
  const beat = BEATS.find((item) => elapsedSeconds >= item.start && elapsedSeconds < item.end) || BEATS[BEATS.length - 1];

  timeLabel.textContent = `${beat.start.toFixed(1)}s-${beat.end.toFixed(1)}s ${beat.label}`;

  if (elapsedSeconds < 14.999) {
    timeLabelFrame = window.requestAnimationFrame(updateTimeLabel);
  }
}

skinButtons.forEach((button) => {
  button.addEventListener("click", () => applySkin(button.dataset.skinButton));
});

replayButton.addEventListener("click", replay);

applySkin("tr");
