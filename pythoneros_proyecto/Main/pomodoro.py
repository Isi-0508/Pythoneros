import threading
import time

sesiones_restantes = [1, 1] #el número indica las cantidades de m dura la sesion y las separaciones son las veces que se hace el ciclo osea si es [2, 4, 6] serian 3 sesiones de 2m, 4m y 6m

def disminuir_sesiones(botón_abajo):
    global sesiones_restantes
    if botón_abajo and sesiones_restantes:
        sesiones_restantes.pop()
    return len(sesiones_restantes)

def aumentar_sesiones(botón_arriba):
    global sesiones_restantes
    if botón_arriba:
        sesiones_restantes.append(25)
    return len(sesiones_restantes)

def temporizador_pomodoro(duracion_minutos, callback=None):
    def run():
        print("⏳ Empecemos a estudiar 🤓")
        time.sleep(duracion_minutos * 25)
        print("⏰ ¡Buena sesión, descansemos un poco!")
        if callback:
            time.sleep(0.6 * 60) #10 segundos de espera antes de la siguiente sesion
            callback()
    hilo = threading.Thread(target=run)
    hilo.start()
    return hilo

def siguiente_sesion():
    global sesiones_restantes
    if sesiones_restantes:
        duracion = sesiones_restantes.pop(0)
        temporizador_pomodoro(duracion, callback=siguiente_sesion)
    else:
        print("🎉 ¡Excelente, ciclo completado!")