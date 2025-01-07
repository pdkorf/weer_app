import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

try:
    from config import API_KEY
except ImportError:
    print("Configuratiebestand niet gevonden. Kopieer config.example.py naar config.py en vul je API key in.")
    API_KEY = ""

class WeerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Wizard Pro")
        self.root.geometry("800x900")
        
        # Favoriete steden
        self.favoriete_steden = ["Amsterdam", "Reykjavik", "Parijs", "New York"]
        
        # Hoofdframe
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Favorieten frame
        self.fav_frame = ttk.Frame(self.main_frame)
        self.fav_frame.pack(fill=tk.X, pady=10)
        
        # Favorieten knoppen
        for stad in self.favoriete_steden:
            btn = ttk.Button(
                self.fav_frame,
                text=stad,
                command=lambda s=stad: self.zoek_stad(s)
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Zoekframe (bestaande code)
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.X, pady=10)
        
        self.stad_entry = ttk.Entry(self.search_frame, width=30, font=('Helvetica', 12))
        self.stad_entry.insert(0, "Voer een stad in...")
        self.stad_entry.pack(side=tk.LEFT, padx=5)
        
        self.zoek_button = ttk.Button(
            self.search_frame, 
            text="Zoek", 
            command=self.update_weer
        )
        self.zoek_button.pack(side=tk.LEFT, padx=5)
        
        # Huidige weer frame
        self.weer_frame = ttk.LabelFrame(self.main_frame, text="Huidig Weer", padding="10")
        self.weer_frame.pack(fill=tk.X, pady=10)
        
        # Labels voor huidig weer
        self.icon_label = ttk.Label(self.weer_frame)
        self.icon_label.pack(side=tk.LEFT, padx=10)
        
        self.current_weer_info = ttk.Frame(self.weer_frame)
        self.current_weer_info.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.temp_label = ttk.Label(self.current_weer_info, font=('Helvetica', 20))
        self.temp_label.pack(anchor='w')
        
        self.beschrijving_label = ttk.Label(self.current_weer_info, font=('Helvetica', 14))
        self.beschrijving_label.pack(anchor='w')
        
        self.details_frame = ttk.Frame(self.current_weer_info)
        self.details_frame.pack(fill=tk.X, pady=5)
        
        self.vochtigheid_label = ttk.Label(self.details_frame, font=('Helvetica', 12))
        self.vochtigheid_label.pack(side=tk.LEFT, padx=5)
        
        self.wind_label = ttk.Label(self.details_frame, font=('Helvetica', 12))
        self.wind_label.pack(side=tk.LEFT, padx=5)
        
        # Voorspelling frame
        self.forecast_frame = ttk.LabelFrame(self.main_frame, text="5-daagse Voorspelling", padding="10")
        self.forecast_frame.pack(fill=tk.X, pady=10)
        
        # Frame voor grafieken
        self.graph_frame = ttk.LabelFrame(self.main_frame, text="Weergrafieken", padding="10")
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Error label
        self.error_label = ttk.Label(
            self.main_frame,
            text="",
            foreground='red',
            font=('Helvetica', 10)
        )
        self.error_label.pack(pady=5)

        # Event bindings
        self.stad_entry.bind('<FocusIn>', self.on_entry_click)
        self.stad_entry.bind('<FocusOut>', self.on_focus_out)
        self.stad_entry.bind('<Return>', lambda e: self.update_weer())

    def on_entry_click(self, event):
        if self.stad_entry.get() == "Voer een stad in...":
            self.stad_entry.delete(0, tk.END)
            self.stad_entry.config(foreground='black')

    def on_focus_out(self, event):
        if self.stad_entry.get() == "":
            self.stad_entry.insert(0, "Voer een stad in...")
            self.stad_entry.config(foreground='grey')

    def haal_voorspelling_op(self, stad):
        api_key = API_KEY  # Gebruik key uit config
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={stad}&appid={api_key}&units=metric&lang=nl"
        
        try:
            response = requests.get(url)
            data = response.json()
            voorspelling = []
            
            # Filter één voorspelling per dag
            geziene_datums = set()
            for item in data['list']:
                datum = datetime.fromtimestamp(item['dt']).date()
                if datum not in geziene_datums:
                    geziene_datums.add(datum)
                    voorspelling.append({
                        'datum': datum.strftime("%d-%m"),
                        'temp': round(item['main']['temp']),
                        'beschrijving': item['weather'][0]['description'],
                        'icon': item['weather'][0]['icon'],
                        'regen': item.get('rain', {}).get('3h', 0),
                        'wind': round(item['wind']['speed'] * 3.6, 1)
                    })
                if len(voorspelling) >= 5:
                    break
                    
            return voorspelling
        except Exception as e:
            return f"Error: {str(e)}"

    def toon_voorspelling(self, voorspelling):
        # Verwijder bestaande voorspellingen
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()
            
        if isinstance(voorspelling, list):
            # Maak frame voor elke dag
            for dag in voorspelling:
                dag_frame = ttk.Frame(self.forecast_frame)
                dag_frame.pack(side=tk.LEFT, padx=10, expand=True)
                
                ttk.Label(dag_frame, text=dag['datum']).pack()
                ttk.Label(dag_frame, text=f"{dag['temp']}°C").pack()
                ttk.Label(dag_frame, text=dag['beschrijving'], wraplength=100).pack()
                
                # Laad weer-icoon
                try:
                    icon_url = f"http://openweathermap.org/img/wn/{dag['icon']}@2x.png"
                    response = requests.get(icon_url)
                    image = Image.open(BytesIO(response.content))
                    photo = ImageTk.PhotoImage(image)
                    icon_label = ttk.Label(dag_frame, image=photo)
                    icon_label.image = photo
                    icon_label.pack()
                except Exception as e:
                    print(f"Kon icoon niet laden: {e}")

    def maak_grafieken(self, voorspelling):
        if not isinstance(voorspelling, list):
            return
            
        # Verwijder bestaande grafieken
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
            
        # Data voorbereiden
        datums = [dag['datum'] for dag in voorspelling]
        temps = [dag['temp'] for dag in voorspelling]
        regen = [dag['regen'] for dag in voorspelling]
        wind = [dag['wind'] for dag in voorspelling]
        
        # Maak figuur met subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
        fig.tight_layout(pad=3.0)
        
        # Temperatuur grafiek
        ax1.plot(datums, temps, 'ro-', label='Temperatuur')
        ax1.set_ylabel('Temperatuur (°C)')
        ax1.grid(True)
        ax1.legend()
        
        # Regen grafiek
        ax2.bar(datums, regen, label='Neerslag', color='blue', alpha=0.6)
        ax2.set_ylabel('Neerslag (mm)')
        ax2.grid(True)
        ax2.legend()
        
        # Wind grafiek
        ax3.plot(datums, wind, 'go-', label='Windsnelheid')
        ax3.set_ylabel('Wind (km/u)')
        ax3.grid(True)
        ax3.legend()
        
        # Voeg canvas toe aan frame
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def zoek_stad(self, stad):
        self.stad_entry.delete(0, tk.END)
        self.stad_entry.insert(0, stad)
        self.update_weer()

    def update_weer(self):
        stad = self.stad_entry.get()
        if stad == "Voer een stad in...":
            return
            
        # Haal huidig weer op (bestaande code)
        weer_info = self.haal_weer_op(stad)
        
        # Haal voorspelling op
        voorspelling = self.haal_voorspelling_op(stad)
        
        # Update UI
        if isinstance(weer_info, dict):
            self.update_huidig_weer(weer_info)
            self.toon_voorspelling(voorspelling)
            self.maak_grafieken(voorspelling)
            self.pas_achtergrond_aan(weer_info)
        else:
            self.error_label.config(text=weer_info)

    def pas_achtergrond_aan(self, weer_info):
        # Bepaal achtergrondkleur op basis van temperatuur en weer
        temp = weer_info['temperatuur']
        beschrijving = weer_info['beschrijving'].lower()
        
        if 'regen' in beschrijving or 'buien' in beschrijving:
            kleur = '#E0E8F0'  # Blauwgrijs voor regen
        elif 'bewolkt' in beschrijving:
            kleur = '#F0F0F0'  # Lichtgrijs voor bewolkt
        elif 'zonnig' in beschrijving or 'helder' in beschrijving:
            kleur = '#FFF8E0'  # Lichtgeel voor zon
        else:
            if temp < 0:
                kleur = '#E8F0F8'  # Lichtblauw voor koud
            elif temp > 25:
                kleur = '#FFE8E0'  # Lichtrood voor warm
            else:
                kleur = '#F0F8F0'  # Lichtgroen voor gematigd
                
        self.root.configure(bg=kleur)
        self.main_frame.configure(style='Custom.TFrame')
        style = ttk.Style()
        style.configure('Custom.TFrame', background=kleur)

    def haal_weer_op(self, stad):
        api_key = API_KEY  # Gebruik key uit config
        url = f"http://api.openweathermap.org/data/2.5/weather?q={stad}&appid={api_key}&units=metric&lang=nl"
        
        try:
            response = requests.get(url)
            weer_data = response.json()
            
            return {
                'temperatuur': round(weer_data['main']['temp']),
                'beschrijving': weer_data['weather'][0]['description'],
                'luchtvochtigheid': weer_data['main']['humidity'],
                'windsnelheid': round(weer_data['wind']['speed'] * 3.6, 1),
                'icon_code': weer_data['weather'][0]['icon']
            }
        except Exception as e:
            return f"Error: {str(e)}"

    def update_huidig_weer(self, weer_info):
        """Update de labels voor het huidige weer"""
        self.temp_label.config(text=f"{weer_info['temperatuur']}°C")
        self.beschrijving_label.config(text=f"{weer_info['beschrijving'].capitalize()}")
        self.vochtigheid_label.config(text=f"💧 Luchtvochtigheid: {weer_info['luchtvochtigheid']}%")
        self.wind_label.config(text=f"💨 Windsnelheid: {weer_info['windsnelheid']} km/u")
        
        # Update weer-icoon
        icon_code = weer_info['icon_code']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        
        try:
            response = requests.get(icon_url)
            image = Image.open(BytesIO(response.content))
            photo = ImageTk.PhotoImage(image)
            self.icon_label.config(image=photo)
            self.icon_label.image = photo
        except Exception as e:
            print(f"Kon icoon niet laden: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeerApp(root)
    root.mainloop()
