document.addEventListener("DOMContentLoaded", () => {

  // 🚨 Si NO existe el timer → no ejecutar nada
  const btnUp = document.getElementById("btnUp");
  const btnDown = document.getElementById("btnDown");
  const sessionCount = document.getElementById("sessionCount");
  const timerDisplay = document.getElementById("timerDisplay");
  const btnStart = document.querySelector(".pomodoro-btn");

  if (!btnUp || !btnDown || !sessionCount || !timerDisplay || !btnStart) {
    // Página sin Pomodoro → no hacer nada.
    return;
  }

  // Estado inicial
  let sesionesRestantes = [1, 1];

  function actualizarVista() {
    sessionCount.textContent = sesionesRestantes.length;
  }

  // Obtener CSRF
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

  // Botón subir sesiones
  btnUp.addEventListener("click", () => {
    if (sesionesRestantes.length < 4) {
      sesionesRestantes.push(1);
      actualizarVista();
      actualizarServidor("/aumentar_sesiones/");
    } else {
      alert("No es recomendable hacer más de 4 sesiones");
    }
  });

  // Botón bajar sesiones
  btnDown.addEventListener("click", () => {
    if (sesionesRestantes.length > 1) {
      sesionesRestantes.pop();
      actualizarVista();
      actualizarServidor("/disminuir_sesiones/");
    } else {
      alert("Debes tener al menos una sesión.");
    }
  });

  // Configurar timer
  let sesiones = sesionesRestantes.map(s => s);
  let descanso = 1;
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
      pausado = false;
      iniciarTemporizador(remaining, enDescanso ? "Descanso" : "Estudio");
      guardarEstado();
      return;
    }

    if (indice < sesionesRestantes.length) {
      let duracion = sesionesRestantes[indice] * 1500;
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

    interval = setInterval(() => {
      let min = Math.floor(remaining / 60);
      let sec = remaining % 60;
      timerDisplay.textContent = `${tipo}: ${min}:${sec.toString().padStart(2, "0")}`;

      remaining--;
      guardarEstado();

      if (remaining < 0) {
        clearInterval(interval);
        if (!enDescanso) {
          iniciarTemporizador(descanso * 900, "Descanso");
        } else {
          indice++;
          iniciarPomodoro();
        }
      }
    }, 1000);
  }

  // Botón de iniciar
  btnStart.addEventListener("click", () => {
    iniciarPomodoro();
  });

  actualizarVista();
}); // <-- cierre correcto del DOMContentLoaded listener
