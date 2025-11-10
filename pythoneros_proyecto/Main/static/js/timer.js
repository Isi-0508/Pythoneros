document.addEventListener("DOMContentLoaded", () => {
  // Estado inicial
  let sesionesRestantes = [1, 1];
  const btnUp = document.getElementById("btnUp");
  const btnDown = document.getElementById("btnDown");
  const sessionCount = document.getElementById("sessionCount");

  // Función para actualizar la vista
  function actualizarVista() {
    sessionCount.textContent = sesionesRestantes.length;
  }

  // Obtener CSRF token de Django
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }



  async function actualizarServidor(url) {
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCookie("csrftoken"),
        },
      });
      const data = await response.json();
      sesionesRestantes = data.sesiones;
      actualizarVista();
      guardarEstado();
    } catch (error) {
      console.error("Error al actualizar:", error);
    }
  }



  function guardarEstado() {
    const estado = {
      sesionesRestantes,
      indice,
      remaining,
      enDescanso,
      pausado
    };
    localStorage.setItem("pomodoroEstado", JSON.stringify(estado));
  }



  function cargarEstado() {
    const estado = localStorage.getItem("pomodoroEstado");
    if (!estado) return null;
    return JSON.parse(estado);
  }


  btnUp.addEventListener("click", () => {
    if (sesionesRestantes.length < 4) {
      sesionesRestantes.push(1);
      actualizarVista();
      actualizarServidor("{% url 'aumentar_sesiones' %}");
    } else {
      alert("No es recomendable hacer más de 4 sesiones");
    }
  });


  btnDown.addEventListener("click", () => {
    if (sesionesRestantes.length > 1) {
      sesionesRestantes.pop();
      actualizarVista();
      actualizarServidor("{% url 'disminuir_sesiones' %}");
    } else {
      alert("Debes tener al menos una sesión.");
    }
  });

  document.body.addEventListener("htmx:configRequest", (event) => {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    event.detail.headers["X-CSRFToken"] = csrfToken;
  });

  actualizarVista();

  //POMODORO
  let sesiones = sesionesRestantes.map(s => s); // copia de las sesiones
  let descanso = 1; // minutos
  let indice = 0;
  let remaining = 0;
  let enDescanso = false;
  let interval = null;
  let pausado = false;

  const estado = cargarEstado();
  if (estado) {
    sesionesRestantes = estado.sesionesRestantes || sesionesRestantes;
    indice = estado.indice || 0;
    remaining = estado.remaining || 0;
    enDescanso = estado.enDescanso || false;
    pausado = estado.pausado || false;

    if (remaining > 0 && !pausado) {
      iniciarTemporizador(remaining, enDescanso ? "Descanso" : "Estudio");
    }
  }

  function iniciarPomodoro() {
    if (pausado) {
      // reanudar
      pausado = false;
      iniciarTemporizador(remaining, enDescanso ? "Descanso" : "Estudio");
      guardarEstado();
      return;
    }

    if (indice < sesionesRestantes.length) {
      let duracion = sesionesRestantes[indice] * 1500; // convertir a segundos
      iniciarTemporizador(duracion, "Estudio");
    } else {
      alert("¡Ciclo completado!");
      localStorage.removeItem("pomodoroEstado");
    }
  }

  function iniciarTemporizador(segundos, tipo) {
    clearInterval(interval);
    remaining = segundos;
    enDescanso = tipo === "Descanso";
    const display = document.getElementById("timerDisplay");

    interval = setInterval(() => {
      let min = Math.floor(remaining / 60);
      let sec = remaining % 60;
      display.textContent = `${tipo}: ${min}:${sec.toString().padStart(2, "0")}`;

      remaining--;
      guardarEstado();

      if (remaining < 0) {
        clearInterval(interval);
        if (!enDescanso) {
          // iniciar descanso
          iniciarTemporizador(descanso * 900, "Descanso");
        } else {
          // siguiente sesión
          indice++;
          iniciarPomodoro();
        }
      }
    }, 1000);
  }

  const btnStart = document.querySelector(".pomodoro-btn");
  btnStart.addEventListener("click", () => {
    iniciarPomodoro();
  });
});

  // Botón iniciar/pausar
  //const btnStart = document.querySelector(".pomodoro-btn");
  //btnStart.addEventListener("click", () => {
  //  if (pausado) {
  //    pausado = false;
  //    iniciarTemporizador(remaining, enDescanso ? "Descanso" : "Estudio");
  //  } else if (interval) {
  //    clearInterval(interval);
  //    pausado = true;
  //    guardarEstado();
  //  } else {
  //    iniciarPomodoro();
  //  }
  //});
  //});