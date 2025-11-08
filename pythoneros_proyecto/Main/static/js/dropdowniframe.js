function StartDropdown() {
  const menu = document.getElementById("app-dropdown");
  let currentQuadrante = null;

  // Reconstruir cuadrantes desde localStorage
  document.querySelectorAll(".st-home-cuadrante").forEach(q => {
    const savedUrl = localStorage.getItem(q.id);
    if (savedUrl) {
      if (savedUrl !== "closed") {
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

        delete_button.addEventListener("click", (e) => {
          e.stopPropagation();
          q.innerHTML = "+";
          localStorage.setItem(q.id, "closed");
        });

        q.style.position = "relative";
        q.appendChild(delete_button);
      }
    }
  });

  // Click en cuadrante
  document.querySelectorAll(".st-home-cuadrante").forEach(q => {
    q.addEventListener("click", (e) => {
      e.stopPropagation();
      currentQuadrante = q;
      menu.style.left = e.pageX + "px";
      menu.style.top = e.pageY + "px";
      menu.style.display = "block";
    });
  });

  // Selección del dropdown
  menu.querySelectorAll("[data-url]").forEach(opt => {
    opt.addEventListener("click", () => {
      menu.style.display = "none";
      if (!currentQuadrante) return;

      const url = opt.getAttribute("data-url");
      if (url && url !== "#") {
        currentQuadrante.innerHTML = "";
        //IFRAME
        const iframe = document.createElement("iframe");
        iframe.src = url;
        iframe.style.width = "100%";
        iframe.style.height = "100%";
        iframe.style.border = "none";
        currentQuadrante.appendChild(iframe);

        //DELETE BUTTON
        const delete_button = document.createElement("span");
        delete_button.textContent = "X";
        delete_button.style.position = "absolute";
        delete_button.style.top = "5px";
        delete_button.style.right = "5px";
        delete_button.style.cursor = "pointer";
        
        //FUNCION DEL DELETE BUTTON
        delete_button.addEventListener("click", (e) => {
          e.stopPropagation();
          currentQuadrante.innerHTML = "+";
          localStorage.setItem(currentQuadrante.id, "closed");
        });

        currentQuadrante.style.position = "relative";
        currentQuadrante.appendChild(delete_button);

        // Guardar en localStorage
        localStorage.setItem(currentQuadrante.id, url);
      }
    });
  });

  //CERRAR CUANDO SE CLICKEE AFUERA
  document.body.addEventListener("click", (e) => {
    if (!menu.contains(e.target)) {
      menu.style.display = "none";
    }
  });
}

document.addEventListener("DOMContentLoaded", StartDropdown);
document.body.addEventListener("htmx:afterSwap", StartDropdown);

