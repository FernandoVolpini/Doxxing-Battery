import tkinter as tk
from tkinter import ttk
import psutil

def get_system_details():
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory_info.percent,
        "disk_percent": disk_info.percent
    }

def get_battery_details():
    battery = psutil.sensors_battery()
    if not battery:
        return None

    return {
        "plugged": battery.power_plugged,
        "percent": battery.percent,
        "secsleft": battery.secsleft,
        "uptime": psutil.boot_time()
    }

def update_system_info():
    details = get_system_details()
    cpu_label.config(text=f"Uso da CPU: {details['cpu_percent']}%")
    memory_label.config(text=f"Uso da Memoria: {details['memory_percent']}%")
    disk_label.config(text=f"Uso do Disco: {details['disk_percent']}%")
    root.after(30000, update_system_info)

def update_battery_info():
    details = get_battery_details()
    if not details:
        no_battery_label.grid(row=10, column=0, sticky=tk.W, pady=5)
        return

    battery_status_label.config(text=f"Estado da Bateria: {details['percent']}%")
    if details['plugged']:
        charger_status_label.config(text="O carregador está ligado.")
    else:
        charger_status_label.config(text="O carregador está desligado.")
    if details['secsleft'] == psutil.POWER_TIME_UNLIMITED:
        battery_secsleft_label.config(text="Tempo Restante: Ilimitado")
    else:
        battery_secsleft_label.config(text=f"Tempo Restante: {details['secsleft']} segundos")
    uptime_label.config(text=f"Tempo de Funcionamento: {details['uptime']} segundos")

    if not details['plugged'] and details['percent'] <= 10:
        low_battery_alert()

    root.after(30000, update_battery_info)

def low_battery_alert():
    alert_window = tk.Toplevel(root)
    alert_window.title("Alerta de Bateria Baixa")
    ttk.Label(alert_window, text="Sua bateria está baixa! Por favor, conecte o carregador.", font=("Arial", 16)).pack(pady=20)
    ttk.Button(alert_window, text="Ok", command=alert_window.destroy).pack(pady=10)
    alert_window.geometry("400x150")

def show_change_tips():
    change_tips_window = tk.Toplevel(root)
    change_tips_window.title("Dicas para Troca de Bateria")
    ttk.Label(change_tips_window, text="Dicas Gerais para Trocar a Bateria do Computador:", font=title_font).pack(pady=10)
    tips = [
        "1. Sempre desligue o computador antes de trocar a bateria.",
        "2. Use a bateria recomendada pelo fabricante do seu computador.",
        "3. Evite tocar nos contatos da bateria com as mãos.",
        "4. Se não se sentir seguro, procure ajuda profissional."
    ]
    for tip in tips:
        ttk.Label(change_tips_window, text=tip).pack(pady=5)
    change_tips_window.geometry("600x400")
    change_tips_window.mainloop()

def show_usage_tips():
    usage_tips_window = tk.Toplevel(root)
    usage_tips_window.title("Dicas de Uso da Bateria")
    ttk.Label(usage_tips_window, text="Dicas sobre o Uso Adequado da Bateria do Computador:", font=title_font).pack(pady=10)
    tips = [
        "1. Não exponha a bateria a temperaturas extremas.",
        "2. Evite deixar seu computador carregando o tempo todo.",
        "3. Se possível, remova a bateria se estiver usando o computador na tomada por longos períodos.",
        "4. Recalibre a bateria do seu notebook pelo menos uma vez por ano."
    ]
    for tip in tips:
        ttk.Label(usage_tips_window, text=tip).pack(pady=5)
    usage_tips_window.geometry("600x400")
    usage_tips_window.mainloop()

root = tk.Tk()
root.title("Informações do Sistema e Bateria")
style = ttk.Style()
style.theme_use('clam')
background_color = "#34495E"
foreground_color = "#ECF0F1"
button_color = "#2ECC71"
style.configure("TFrame", background=background_color)
style.configure("TLabel", background=background_color, foreground=foreground_color, font=("Arial", 12))
style.configure("TButton", background=button_color, foreground=foreground_color, font=("Arial", 12))
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
title_font = ("Arial", 18, "bold")
cpu_label = ttk.Label(frame)
cpu_label.grid(row=0, column=0, sticky=tk.W, pady=5)
memory_label = ttk.Label(frame)
memory_label.grid(row=1, column=0, sticky=tk.W, pady=5)
disk_label = ttk.Label(frame)
disk_label.grid(row=2, column=0, sticky=tk.W, pady=5)
battery_status_label = ttk.Label(frame)
battery_status_label.grid(row=3, column=0, sticky=tk.W, pady=5)
charger_status_label = ttk.Label(frame)
charger_status_label.grid(row=4, column=0, sticky=tk.W, pady=5)
battery_secsleft_label = ttk.Label(frame)
battery_secsleft_label.grid(row=6, column=0, sticky=tk.W, pady=5)
uptime_label = ttk.Label(frame)
uptime_label.grid(row=7, column=0, sticky=tk.W, pady=5)
no_battery_label = ttk.Label(frame, text="Nenhuma informação de bateria disponível.")
change_tips_button = ttk.Button(frame, text="Dicas para Troca de Bateria", command=show_change_tips)
change_tips_button.grid(row=8, column=0, pady=10)
usage_tips_button = ttk.Button(frame, text="Dicas de Uso da Bateria", command=show_usage_tips)
usage_tips_button.grid(row=9, column=0, pady=10)
update_system_info()
update_battery_info()
root.geometry("500x500")
root.mainloop()
