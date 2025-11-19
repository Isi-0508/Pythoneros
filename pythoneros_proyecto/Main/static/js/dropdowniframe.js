function StartDropdown() {

  const menu = document.getElementById("app-dropdown");


  const cuadrantes = document.querySelectorAll(".st-home-cuadrante");
  if (!menu || cuadrantes.length === 0) return;

  let currentQuadrante = null;

  function urlsIguales(url1, url2) {
    try {
      return new URL(url1, location.href).href === new URL(url2, location.href).href;
    } catch {
      return url1 === url2;
    }
  }

  // ========== RECONSTRUIR CUADRANTES ==========
  cuadrantes.forEach(q => {
    const savedUrl = localStorage.getItem(q.id);
    if (savedUrl && savedUrl !== "closed") {

      q.innerHTML = "";

      const iframe = document.createElement("iframe");
      iframe.src = savedUrl;
      iframe.style.width = "100%";
      iframe.style.height = "100%";
      iframe.style.border = "none";
      q.appendChild(iframe);

      const delete_button = document.createElement("span");
      delete_button.textContent = "X";
      delete_button.style.position = "absolute";
      delete_button.style.top = "5px";
      delete_button.style.right = "5px";
      delete_button.style.cursor = "pointer";
      delete_button.class = "btn btn-outline-danger";

      delete_button.addEventListener("click", (e) => {
        e.stopPropagation();
        q.innerHTML = "+";
        localStorage.setItem(q.id, "closed");
      });

      q.style.position = "relative";
      q.appendChild(delete_button);
    }
  });

  // ========== CLICK EN CUADRANTE ==========
  cuadrantes.forEach(q => {
    q.addEventListener("click", (e) => {
      e.stopPropagation();
      currentQuadrante = q;
      menu.style.left = e.pageX + "px";
      menu.style.top = e.pageY + "px";
      menu.style.display = "block";
    });
  });

  // ========== OPCIONES DEL MENÚ ==========
  const opciones = menu.querySelectorAll("[data-url]");
  opciones.forEach(opt => {

    opt.addEventListener("click", () => {

      menu.style.display = "none";
      if (!currentQuadrante) return;

      const url = opt.getAttribute("data-url");
      if (!url || url === "#") return;

      const cuadrantes = document.querySelectorAll(".st-home-cuadrante");
      for (const q of cuadrantes) {
        const iframeExistente = q.querySelector("iframe");
        if (iframeExistente && urlsIguales(iframeExistente.src, url)) {
          return;
        }
      }

      currentQuadrante.innerHTML = "";

      const iframe = document.createElement("iframe");
      iframe.src = url;
      iframe.style.width = "100%";
      iframe.style.height = "100%";
      iframe.style.border = "none";
      currentQuadrante.appendChild(iframe);

      const delete_button = document.createElement("span");
      delete_button.textContent = "X";
      delete_button.style.position = "absolute";
      delete_button.style.top = "5px";
      delete_button.style.right = "5px";
      delete_button.style.cursor = "pointer";
      delete_button.class = "btn btn-outline-danger";

      delete_button.addEventListener("click", (e) => {
        e.stopPropagation();
        currentQuadrante.innerHTML = "+";
        localStorage.setItem(currentQuadrante.id, "closed");
      });

      currentQuadrante.style.position = "relative";
      currentQuadrante.appendChild(delete_button);

      localStorage.setItem(currentQuadrante.id, url);
    });

  });

  // ========== CERRAR DROPDOWN ==========
  document.body.addEventListener("click", (e) => {
    if (!menu.contains(e.target)) {
      menu.style.display = "none";
    }
  });

}

// SOLO EJECUTAR SI EXISTE app-dropdown
document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("app-dropdown"))
      StartDropdown();
});

document.body.addEventListener("htmx:afterSwap", () => {
  if (document.getElementById("app-dropdown"))
      StartDropdown();
});
