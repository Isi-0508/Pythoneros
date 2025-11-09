function StartDropdown() {
  const menu = document.getElementById("app-dropdown");
  let currentQuadrante = null;

  // Función para comparar URLs de manera confiable
  function urlsIguales(url1, url2) {
    try {
      return new URL(url1, location.href).href === new URL(url2, location.href).href;
    } catch {
      return url1 === url2;
    }
  }

  // Reconstruir cuadrantes desde localStorage
  document.querySelectorAll(".st-home-cuadrante").forEach(q => {
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
      delete_button.class = "btn btn-outline-danger"

      delete_button.addEventListener("click", (e) => {
        e.stopPropagation();
        q.innerHTML = "+";
        localStorage.setItem(q.id, "closed");
      });

      q.style.position = "relative";
      q.appendChild(delete_button);
    }
  });

  //Click en cuadrante
  document.querySelectorAll(".st-home-cuadrante").forEach(q => {
    q.addEventListener("click", (e) => {
      e.stopPropagation();
      currentQuadrante = q;
      menu.style.left = e.pageX + "px";
      menu.style.top = e.pageY + "px";
      menu.style.display = "block";
    });
  });

  //Selección del dropdown
  menu.querySelectorAll("[data-url]").forEach(opt => {
    opt.addEventListener("click", () => {
      menu.style.display = "none";
      if (!currentQuadrante) return;

      const url = opt.getAttribute("data-url");
      if (!url || url === "#") return;

      //CHECK PARA EVITAR 2 CUADRANTES IGUALES
      const cuadrantes = document.querySelectorAll(".st-home-cuadrante");
      for (const q of cuadrantes) {
        const iframeExistente = q.querySelector("iframe");
        if (iframeExistente && urlsIguales(iframeExistente.src, url)) {
          return;
        }
      }

      currentQuadrante.innerHTML = "";

      // Crear iframe
      const iframe = document.createElement("iframe");
      iframe.src = url;
      iframe.style.width = "100%";
      iframe.style.height = "100%";
      iframe.style.border = "none";
      currentQuadrante.appendChild(iframe);

      // Boton Delete
      const delete_button = document.createElement("span");
      delete_button.textContent = "X";
      delete_button.style.position = "absolute";
      delete_button.style.top = "5px";
      delete_button.style.right = "5px";
      delete_button.style.cursor = "pointer";
      delete_button.class = "btn btn-outline-danger"

      const cuadranteActual = currentQuadrante;

      delete_button.addEventListener("click", (e) => {
          e.stopPropagation();
          cuadranteActual.innerHTML = "+";
          localStorage.setItem(cuadranteActual.id, "closed");
      });



      currentQuadrante.style.position = "relative";
      currentQuadrante.appendChild(delete_button);

      // Guardar en localStorage
      localStorage.setItem(currentQuadrante.id, url);
    });
  });

  // Cerrar dropdown al hacer clic afuera
  document.body.addEventListener("click", (e) => {
    if (!menu.contains(e.target)) {
      menu.style.display = "none";
    }
  });
}

document.addEventListener("DOMContentLoaded", StartDropdown);
document.body.addEventListener("htmx:afterSwap", StartDropdown);




