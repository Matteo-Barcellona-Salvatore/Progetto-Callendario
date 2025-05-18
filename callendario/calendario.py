import tkinter as tk
from tkinter import simpledialog
import calendar
from datetime import datetime
import json
import os


giorni_settimana = ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato", "Domenica"]
mesi_italiano = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
                 "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
file_agenda = "agenda.json"


if os.path.exists(file_agenda):
    with open(file_agenda, "r", encoding="utf-8") as f:
        agenda = json.load(f)
else:
    agenda = {}


oggi = datetime.today()
giorno_oggi = oggi.day
mese_corrente = oggi.month
anno_corrente = oggi.year
cal = calendar.Calendar(firstweekday=0)
settimane = cal.monthdayscalendar(anno_corrente, mese_corrente)

def apri_agenda(giorno):
    if giorno == 0:
        return
    data = f"{anno_corrente:04d}-{mese_corrente:02d}-{giorno:02d}"
    nota_corrente = agenda.get(data, "")
    nota = simpledialog.askstring("Agenda", f"Inserisci nota per il {data}:", initialvalue=nota_corrente)

    if nota is not None:
        if nota.strip() == "": 
            agenda.pop(data, None)
        else:
            agenda[data] = nota.strip()

        with open(file_agenda, "w", encoding="utf-8") as f:
            json.dump(agenda, f, indent=4, ensure_ascii=False)


        aggiorna_calendario()



def cambia_mese(direzione):
    global mese_corrente, anno_corrente, settimane
    if direzione == "avanti":
        mese_corrente += 1
        if mese_corrente > 12:
            mese_corrente = 1
            anno_corrente += 1
    elif direzione == "indietro":
        mese_corrente -= 1
        if mese_corrente < 1:
            mese_corrente = 12
            anno_corrente -= 1

    cal.setfirstweekday(0)
    settimane = cal.monthdayscalendar(anno_corrente, mese_corrente)

    aggiorna_calendario()



def aggiorna_calendario():
    for widget in griglia.winfo_children():
        widget.destroy()

    titolo.config(text=f"{mesi_italiano[mese_corrente - 1]} {anno_corrente}")

    for i, giorno in enumerate(giorni_settimana):
        cella = tk.Label(griglia, text=giorno, font=("Arial", 14, "bold"),
                         width=larghezza_cella, height=2,
                         bg="#2196f3", fg="#ffffff", relief="solid", bd=2)
        cella.grid(row=0, column=i, sticky="nsew", padx=2, pady=2)


    for riga, settimana in enumerate(settimane, start=1):
        for colonna, giorno in enumerate(settimana):
            if giorno == 0:
                testo = ""
                bg_color = colore_sfondo
                fg_color = "#999999"
            elif giorno == giorno_oggi and mese_corrente == oggi.month and anno_corrente == oggi.year:
                testo = str(giorno)
                bg_color = colore_oggi_bg
                fg_color = colore_oggi_fg
            else:
                data_str = f"{anno_corrente:04d}-{mese_corrente:02d}-{giorno:02d}"
                ha_nota = data_str in agenda
                if ha_nota:
                    testo = str(giorno) + " 📌"
                    bg_color = colore_nota_bg
                    fg_color = colore_nota_fg
                else:
                    testo = str(giorno)
                    bg_color = colore_sfondo
                    fg_color = "#333333"

            btn = tk.Button(griglia, text=testo, font=("Arial", 12),
                            width=larghezza_cella, height=altezza_cella,
                            bg=bg_color, fg=fg_color,
                            relief="solid", bd=2, highlightthickness=0,
                            activebackground="#81c784", activeforeground="#ffffff",
                            command=lambda g=giorno: apri_agenda(g))

            btn.grid(row=riga, column=colonna, sticky="nsew", padx=5, pady=5)

    for i in range(7):
        griglia.grid_columnconfigure(i, weight=1)
    for i in range(6):
        griglia.grid_rowconfigure(i, weight=1)



def crea_calendario():
    global root, titolo, griglia, larghezza_cella, altezza_cella, colore_sfondo, colore_bordo, colore_oggi_bg, colore_oggi_fg, colore_nota_bg, colore_nota_fg


    larghezza_cella = 12
    altezza_cella = 4
    colore_sfondo = "#ffffff"
    colore_bordo = "#1e88e5" 
    colore_oggi_bg = "#a5d6a7" 
    colore_oggi_fg = "#388e3c"  
    colore_nota_bg = "#ffeb3b" 
    colore_nota_fg = "#f57f17"  

    root = tk.Tk()
    root.title("Calendario con Agenda")
    root.configure(bg="#e3f2fd") 
    root.geometry("750x780")

    barra_mese = tk.Frame(root, bg="#2196f3", pady=10)
    barra_mese.pack(fill="x")


    freccia_sinistra = tk.Button(barra_mese, text="◀", font=("Arial", 16, "bold"),
                                 bg="#ffffff", fg="#2196f3", command=lambda: cambia_mese("indietro"))
    freccia_sinistra.pack(side="left", padx=10)


    titolo = tk.Label(barra_mese, text=f"{mesi_italiano[mese_corrente - 1]} {anno_corrente}",
                      font=("Arial", 22, "bold"), bg="#2196f3", fg="#ffffff")
    titolo.pack(side="left", expand=True)


    freccia_destra = tk.Button(barra_mese, text="▶", font=("Arial", 16, "bold"),
                               bg="#ffffff", fg="#2196f3", command=lambda: cambia_mese("avanti"))
    freccia_destra.pack(side="right", padx=10)

    griglia = tk.Frame(root, bg="#ffffff")
    griglia.pack(pady=20)

    aggiorna_calendario()

    root.mainloop()


crea_calendario()
