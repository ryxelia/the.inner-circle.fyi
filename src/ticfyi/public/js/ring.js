const base = "https://the.inner-circle.fyi";
// `currentScript` remains reliable when this file is served with a hashed URL.
const script =
    document.currentScript ?? document.querySelector('script[src*="/ring"]');
// `data-` is the conventional form; accept the legacy `domain` attribute too.
const domain =
    script?.getAttribute("data-domain") ||
    script?.getAttribute("domain") ||
    window.location.hostname;

function loadWebRing(domain) {
    let container = document.getElementById("innerCircleWebRing");
    if (!container) {
        const parent = script?.parentElement;
        if (!parent) return;
        container = document.createElement("div");
        container.id = "innerCircleWebRing";
        parent.appendChild(container);
    }
    if (container.dataset.loaded === "true") return;
    container.classList.add("innerCircleWebRing");
    container.dataset.loaded = "true";

    const from = encodeURIComponent(domain);

    // Keep the icon inline so embedding the ring does not require a CORS-enabled fetch.
    const button = `
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
            <path
                d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5
                   2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09
                   C13.09 3.81 14.76 3 16.5 3
                   19.58 3 22 5.42 22 8.5
                   c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
                fill="currentColor"
            />
        </svg>`;

    container.innerHTML = `
        <style>
            #innerCircleWebRing a {text-decoration: none;}
            #innerCircleWebRingNavHome {transition: transform 0.4s; vertical-align: middle;}
            #innerCircleWebRingNavHome:hover {transform: scale(1.05) translateY(-2px);}
            #innerCircleWebRingNavBackwards {rotate: 90deg; color: #ffa9fc;}
            #innerCircleWebRingNavForwards {rotate: -90deg; color: #a8eefe;}
            #innerCircleWebRingNavBackwards, #innerCircleWebRingNavForwards {transition: transform 0.4s; display: inline-block; aspect-ratio: 1; vertical-align: middle; transform: scale(0.8);}
            #innerCircleWebRingNavBackwards:hover, #innerCircleWebRingNavForwards:hover {transform: scale(0.84) translateY(10px);}
        </style>
        <a href="${base}/ring/back?from_url=${from}"
            rel="noopener noreferrer"
            id="innerCircleWebRingNavBackwards"
        >
            ${button}
        </a>
        <a href="${base}/" target="_blank" rel="noopener noreferrer">
            <img
                src="${base}/static/images/inner-button.avif"
                width="88"
                height="31"
                loading="lazy"
                style="image-rendering:pixelated"
                alt="the.inner-circle.fyi 88x31px web button"
                id="innerCircleWebRingNavHome"
            >
        </a>
        <a href="${base}/ring/next?from_url=${from}" rel="noopener noreferrer"
            aria-label="Navigate to the next site in the inner circle web ring"
            id="innerCircleWebRingNavForwards"
        >
            ${button}
        </a>
    `;
}

// Run when page layout is done loading, including scripts loaded after DOMContentLoaded.
const initialize = () => loadWebRing(domain);
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
} else {
    initialize();
}
