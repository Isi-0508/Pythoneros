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