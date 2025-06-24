import time
import ctypes
import threading
import sys
import os
import tkinter as tk

# --- Constantes ---
INTERVALO_MINUTOS = 30
INTERVALO_SEGUNDOS = INTERVALO_MINUTOS * 60
DURACAO_BLOQUEIO_MINUTOS = 5
DURACAO_BLOQUEIO_SEGUNDOS = DURACAO_BLOQUEIO_MINUTOS * 60


NOME_PROCESSO_UNICO = "Pause30MinAppUnico"

# Variável global para a janela de bloqueio
lock_window_global = None

def show_lock_screen_overlay():
    """Mostra uma janela de overlay em tela cheia para bloquear a interação."""
    global lock_window_global

    if lock_window_global is not None and lock_window_global.winfo_exists():
        # Se a janela já existe (caso raro, mas para segurança)
        return

    root = tk.Tk()
    lock_window_global = root # Armazena a referência globalmente
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True) # Tenta manter no topo
    root.configure(bg="black")
    root.lift() # Eleva a janela
    root.focus_force() # Força o foco

    # Remove decorações da janela (barra de título, botões de fechar)
    root.overrideredirect(True)

    # Captura todos os eventos de teclado e mouse para evitar interações
    root.grab_set() # Impede interação com outras janelas

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    message_label = tk.Label(root, text=f"PAUSA OBRIGATÓRIA!\n\nLevante-se e movimente-se.\n\nO computador será liberado em:",
                             font=("Arial", 30, "bold"), fg="white", bg="black", wraplength=screen_width*0.8)
    message_label.pack(pady=(screen_height // 4, 20))

    timer_label = tk.Label(root, text="", font=("Arial", 50, "bold"), fg="red", bg="black")
    timer_label.pack(pady=20)

    def update_timer(seconds_left):
        if not root.winfo_exists(): # Verifica se a janela ainda existe
            return
        minutes = seconds_left // 60
        seconds = seconds_left % 60
        timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        if seconds_left > 0:
            root.after(1000, update_timer, seconds_left - 1)
        else:
            if root.winfo_exists():
                root.grab_release() # Libera a captura de eventos
                root.destroy()
            global lock_window_global
            lock_window_global = None # Limpa a referência global

    update_timer(DURACAO_BLOQUEIO_SEGUNDOS)
    
    # Tenta desabilitar o fechamento por Alt+F4 (pode não ser 100% eficaz em todas as configs do Windows)
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    root.mainloop()


def lock_screen_action():
    """Função chamada pela thread do timer para iniciar o bloqueio."""
    # Criamos uma nova thread para a GUI do Tkinter, pois Tkinter precisa rodar em seu próprio loop.
    # A thread principal do timer continuará rodando para o próximo ciclo.
    print(f"Intervalo de {INTERVALO_MINUTOS} minutos completo. Bloqueando a tela por {DURACAO_BLOQUEIO_MINUTOS} minutos...")
    gui_thread = threading.Thread(target=show_lock_screen_overlay, daemon=False) # daemon=False para que o script espere
    gui_thread.start()
    gui_thread.join() # Espera a tela de bloqueio ser fechada antes de continuar o timer principal
    print("Tela desbloqueada.")


def criar_mutex():
    """Cria um mutex para garantir que apenas uma instância do app rode."""
    mutex = ctypes.windll.kernel32.CreateMutexW(None, True, NOME_PROCESSO_UNICO)
    if ctypes.windll.kernel32.GetLastError() == 183: # ERROR_ALREADY_EXISTS
        return None # Mutex já existe, outra instância está rodando
    return mutex

def liberar_mutex(mutex):
    """Libera o mutex."""
    if mutex:
        ctypes.windll.kernel32.CloseHandle(mutex)

def timer_loop():
    """Main loop that triggers screen lock every X minutes."""
    # Esconde a janela do console. Requer `pythonw.exe` para não abrir console.
    # Se executado com `python.exe`, a janela ainda aparecerá brevemente.
    if hasattr(sys, 'frozen') or hasattr(sys, '_MEIPASS'): # PyInstaller
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd != 0:
            ctypes.windll.user32.ShowWindow(hwnd, 0) # SW_HIDE
            ctypes.windll.kernel32.CloseHandle(hwnd)
    elif os.name == 'nt': # Windows
        # Tenta obter o handle da janela do console e escondê-la
        # Funciona melhor se o script for nomeado com .pyw e executado com pythonw.exe
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 0) # SW_HIDE


    print(f"Pause-30min iniciado. A tela será bloqueada a cada {INTERVALO_MINUTOS} minutos.")
    print("Este aplicativo está rodando em segundo plano.")
    print(f"Para pará-lo, finalize o processo 'python.exe' ou 'pythonw.exe' (ou o nome do executável se compilado) no Gerenciador de Tarefas.")
    
    while True:
        time.sleep(INTERVALO_SEGUNDOS)
        # print(f"Intervalo de {INTERVALO_MINUTOS} minutos completo. Bloqueando a tela...") # Movido para lock_screen_action
        lock_screen_action()

if __name__ == "__main__":
    # Tenta ocultar o console imediatamente se não for debug e for Windows
    # Isso é mais eficaz se o script for executado com pythonw.exe
    if not sys.flags.debug and os.name == 'nt': # Não oculta em modo debug
        try:
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 0) # SW_HIDE
        except Exception as e:
            print(f"Erro ao tentar ocultar console: {e}")


    mutex = criar_mutex()
    if not mutex:
        # print("Pause-30min já está em execução.") # Pode ser útil para debug
        sys.exit(0) # Sai silenciosamente se outra instância já estiver rodando

    # Inicia o timer em uma thread separada
    timer_thread = threading.Thread(target=timer_loop, daemon=True)
    timer_thread.start()

    # Mantém o script principal rodando indefinidamente em segundo plano.
    # O daemon=True na thread fará com que ela seja encerrada quando o script principal terminar.
    # No entanto, como queremos que ele rode "para sempre" (até o PC desligar ou processo ser morto),
    # precisamos de um loop aqui também, ou o script principal terminaria e a thread daemon junto.
    try:
        while True:
            time.sleep(3600) # Verifica a cada hora, apenas para manter o main thread vivo.
                           # A lógica principal está na timer_thread.
    except KeyboardInterrupt:
        print("Pause-30min encerrado pelo usuário.")
    finally:
        liberar_mutex(mutex)
        # print("Mutex liberado.") # Para debug