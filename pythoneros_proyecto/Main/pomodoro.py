import threading
import time

def temporizador_pomodoro(duracion_minutos, callback=None):
    def run():
        print("⏳ Empecemos a estudiar 🤓")
        time.sleep(duracion_minutos * 60)
        print("⏰ ¡Buena sesión, descansemos un poco!")
        if callback:
            callback()
    hilo = threading.Thread(target=run)
    hilo.start()
    return hilo

sesiones_restantes = [1, 1]
def siguiente_sesion():
    if sesiones_restantes:
        duracion = sesiones_restantes.pop(0)
        temporizador_pomodoro(duracion, callback=siguiente_sesion)
    else:
        print("🎉 ¡Excelente, ciclo completado!")

temporizador_pomodoro(0.1, callback=siguiente_sesion)
print("El Pomodoro está corriendo en segundo plano")
time.sleep(0.2 * 60)