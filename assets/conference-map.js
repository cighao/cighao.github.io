(() => {
  const section = document.querySelector("#conference-map");
  if (!section) return;
  const { cities, meetings } = JSON.parse(section.querySelector("#conference-map-data").textContent);
  const stage = section.querySelector(".map-stage");
  const svg = section.querySelector(".conference-world");
  const { width: mapWidth, height: mapHeight } = svg.viewBox.baseVal;
  const pins = [...section.querySelectorAll("[data-city]")];
  const records = [...section.querySelectorAll("[data-meeting]")];
  const status = section.querySelector(".map-selection-status");
  let selectedCity = null;
  let selectedMeeting = null;
  let zoom = 1;
  let viewX = 0;
  let viewY = 0;
  let drag = null;
  let suppressClick = false;
  const clamp = (value, min, max) => Math.max(min, Math.min(max, value));

  const scrollTo = (element) => element?.scrollIntoView({
    block: "nearest",
    behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth",
  });

  function updateView() {
    const width = mapWidth / zoom;
    const height = mapHeight / zoom;
    viewX = clamp(viewX, 0, mapWidth - width);
    viewY = clamp(viewY, 0, mapHeight - height);
    svg.setAttribute("viewBox", `${viewX} ${viewY} ${width} ${height}`);
    stage.classList.toggle("is-draggable", zoom > 1);
    for (const pin of pins) {
      const city = cities.find((item) => item.id === pin.dataset.city);
      const left = (city.x - viewX) / width * 100;
      const top = (city.y - viewY) / height * 100;
      pin.style.left = `${left}%`;
      pin.style.top = `${top}%`;
      pin.hidden = left < 0 || left > 100 || top < 0 || top > 100;
      pin.classList.toggle("is-selected", city.id === selectedCity);
      pin.setAttribute("aria-pressed", String(city.id === selectedCity));
    }
    section.querySelector('[data-zoom="in"]').disabled = zoom >= 3;
    section.querySelector('[data-zoom="out"]').disabled = zoom <= 1;
    section.querySelector('[data-zoom="reset"]').disabled = zoom === 1;
  }

  function zoomAt(nextZoom, anchorX = 0.5, anchorY = 0.5) {
    nextZoom = clamp(nextZoom, 1, 3);
    if (Math.abs(nextZoom - zoom) < 0.000001) return;
    // Keep the geographic point under the mouse stationary while zooming.
    viewX += anchorX * (mapWidth / zoom - mapWidth / nextZoom);
    viewY += anchorY * (mapHeight / zoom - mapHeight / nextZoom);
    zoom = nextZoom;
    updateView();
  }

  stage.addEventListener("wheel", (event) => {
    if (event.ctrlKey || event.target.closest(".map-controls") || drag) return;
    // Scrolling out of the full-world view continues scrolling the page.
    if (zoom === 1 && event.deltaY >= 0) return;
    event.preventDefault();
    const rect = stage.getBoundingClientRect();
    const unit = event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? rect.height : 1;
    const delta = clamp(event.deltaY * unit, -300, 300);
    zoomAt(zoom * Math.exp(-delta * 0.002),
      clamp((event.clientX - rect.left) / rect.width, 0, 1),
      clamp((event.clientY - rect.top) / rect.height, 0, 1));
  }, { passive: false });

  stage.addEventListener("pointerdown", (event) => {
    suppressClick = false;
    if (!event.isPrimary || event.button !== 0 || zoom === 1 || event.target.closest(".map-controls")) return;
    drag = { id: event.pointerId, startX: event.clientX, startY: event.clientY, viewX, viewY, moved: false };
  });
  stage.addEventListener("pointermove", (event) => {
    if (!drag || event.pointerId !== drag.id) return;
    const dx = event.clientX - drag.startX;
    const dy = event.clientY - drag.startY;
    if (!drag.moved) {
      if (Math.hypot(dx, dy) < 4) return;
      drag.moved = true;
      stage.setPointerCapture(event.pointerId);
      stage.classList.add("is-dragging");
    }
    event.preventDefault();
    const rect = stage.getBoundingClientRect();
    viewX = drag.viewX - dx * mapWidth / zoom / rect.width;
    viewY = drag.viewY - dy * mapHeight / zoom / rect.height;
    updateView();
  });
  const endDrag = (event) => {
    if (!drag || event.pointerId !== drag.id) return;
    suppressClick = drag.moved && event.type !== "pointercancel";
    drag = null;
    stage.classList.remove("is-dragging");
    if (stage.hasPointerCapture(event.pointerId)) stage.releasePointerCapture(event.pointerId);
  };
  stage.addEventListener("pointerup", endDrag);
  stage.addEventListener("pointercancel", endDrag);
  stage.addEventListener("lostpointercapture", endDrag);
  stage.addEventListener("click", (event) => {
    if (!suppressClick || event.detail === 0) return;
    suppressClick = false;
    event.preventDefault();
    event.stopImmediatePropagation();
  }, true);
  stage.tabIndex = 0;
  stage.setAttribute("role", "group");
  stage.setAttribute("aria-label", "World map. Zoom with the mouse wheel or zoom buttons, then drag or use arrow keys to pan.");
  stage.addEventListener("keydown", (event) => {
    if (event.target !== stage || zoom === 1) return;
    const direction = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] }[event.key];
    if (!direction) return;
    event.preventDefault();
    viewX += direction[0] * mapWidth / zoom * 0.1;
    viewY += direction[1] * mapHeight / zoom * 0.1;
    updateView();
  });

  function render() {
    for (const record of records) {
      const meeting = meetings.find((item) => item.id === record.dataset.meeting);
      record.classList.toggle("is-active", Boolean(meeting &&
        (selectedMeeting ? meeting.id === selectedMeeting : meeting.city === selectedCity)));
    }
    const city = cities.find((item) => item.id === selectedCity);
    const count = records.filter((record) => record.classList.contains("is-active")).length;
    status.textContent = city && count ? `${count} ${count === 1 ? "talk" : "talks"} in ${city.name} highlighted below.` : "";
    updateView();
  }

  pins.forEach((pin) => pin.addEventListener("click", (event) => {
    // Nearby cities can have overlapping touch targets in the world view.
    // Resolve pointer clicks to the closest visible marker; keyboard clicks
    // continue to activate the focused button.
    const nearest = event.detail > 0 ? pins.filter((item) => !item.hidden).reduce((best, item) => {
      const rect = item.getBoundingClientRect();
      const distance = Math.hypot(event.clientX - rect.x - rect.width / 2, event.clientY - rect.y - rect.height / 2);
      return distance < best.distance ? { pin: item, distance } : best;
    }, { pin, distance: Infinity }).pin : pin;
    if (nearest !== pin) nearest.focus({ preventScroll: true });
    selectedCity = nearest.dataset.city;
    selectedMeeting = null;
    render();
    scrollTo(records.find((record) => record.classList.contains("is-active")));
  }));
  section.querySelectorAll("[data-record-city]").forEach((link) => link.addEventListener("click", (event) => {
    event.preventDefault();
    selectedCity = link.dataset.recordCity;
    selectedMeeting = link.dataset.recordId;
    const city = cities.find((item) => item.id === selectedCity);
    viewX = city.x - mapWidth / zoom / 2;
    viewY = city.y - mapHeight / zoom / 2;
    render();
    scrollTo(section.querySelector(".map-frame"));
  }));
  section.querySelectorAll("[data-zoom]").forEach((button) => button.addEventListener("click", () => {
    zoomAt(button.dataset.zoom === "reset" ? 1 : zoom + (button.dataset.zoom === "in" ? 0.5 : -0.5));
  }));
  render();
  section.querySelector(".map-controls").hidden = false;
  section.querySelector(".map-pins").hidden = false;
})();
