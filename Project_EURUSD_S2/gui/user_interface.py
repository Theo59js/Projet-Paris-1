import tkinter as tk
from tkinter import ttk
import pandas as pd
from utils.data_processing import create_predict_dataframe, generate_daily_dataframe


def launch_gui():
    predict_datas = None

    def submit_data():
        nonlocal predict_datas
        libor_values = [float(liborusd_ov_entry1.get()), float(liborusd_ov_entry2.get()),
                        float(liborusd_ov_entry3.get())]
        libor_dates = [libor_date_entry1.get(), libor_date_entry2.get(), libor_date_entry3.get()]
        ester_values = [float(estereonia_entry1.get()), float(estereonia_entry2.get()), float(estereonia_entry3.get())]
        ester_dates = [ester_date_entry1.get(), ester_date_entry2.get(), ester_date_entry3.get()]
        libor_data = {'values': libor_values, 'dates': libor_dates}
        ester_data = {'values': ester_values, 'dates': ester_dates}
        user_predict_datas = create_predict_dataframe(libor_data, ester_data)
        predict_datas = generate_daily_dataframe(user_predict_datas)
        print("DataFrame créé avec succès :\n", predict_datas)

    root = tk.Tk()
    root.title("Entrée de données")

    liborusd_ov_label = ttk.Label(root, text="Libor USD Overnight:")
    liborusd_ov_label.grid(row=0, column=0, padx=5, pady=5)
    liborusd_ov_entry1 = ttk.Entry(root)
    liborusd_ov_entry1.grid(row=0, column=1, padx=5, pady=5)

    libor_date_label = ttk.Label(root, text="Date (jj/mm/aaaa):")
    libor_date_label.grid(row=0, column=2, padx=5, pady=5)
    libor_date_entry1 = ttk.Entry(root)
    libor_date_entry1.grid(row=0, column=3, padx=5, pady=5)

    liborusd_ov_entry2 = ttk.Entry(root)
    liborusd_ov_entry2.grid(row=1, column=1, padx=5, pady=5)
    libor_date_entry2 = ttk.Entry(root)
    libor_date_entry2.grid(row=1, column=3, padx=5, pady=5)

    liborusd_ov_entry3 = ttk.Entry(root)
    liborusd_ov_entry3.grid(row=2, column=1, padx=5, pady=5)
    libor_date_entry3 = ttk.Entry(root)
    libor_date_entry3.grid(row=2, column=3, padx=5, pady=5)

    estereonia_label = ttk.Label(root, text="ESTER (Eonia) Rate:")
    estereonia_label.grid(row=3, column=0, padx=5, pady=5)
    estereonia_entry1 = ttk.Entry(root)
    estereonia_entry1.grid(row=3, column=1, padx=5, pady=5)

    ester_date_label = ttk.Label(root, text="Date (jj/mm/aaaa):")
    ester_date_label.grid(row=3, column=2, padx=5, pady=5)
    ester_date_entry1 = ttk.Entry(root)
    ester_date_entry1.grid(row=3, column=3, padx=5, pady=5)

    estereonia_entry2 = ttk.Entry(root)
    estereonia_entry2.grid(row=4, column=1, padx=5, pady=5)
    ester_date_entry2 = ttk.Entry(root)
    ester_date_entry2.grid(row=4, column=3, padx=5, pady=5)

    estereonia_entry3 = ttk.Entry(root)
    estereonia_entry3.grid(row=5, column=1, padx=5, pady=5)
    ester_date_entry3 = ttk.Entry(root)
    ester_date_entry3.grid(row=5, column=3, padx=5, pady=5)

    submit_button = ttk.Button(root, text="Soumettre", command=submit_data)
    submit_button.grid(row=6, column=0, columnspan=4, padx=5, pady=5)

    root.mainloop()

launch_gui()