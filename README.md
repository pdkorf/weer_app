# PDK Weather Pro - Documentatie

## Inhoudsopgave

1. [Overzicht](#overzicht)
2. [Project Structuur](#project-structuur)
3. [Gebruikte Technologieën](#gebruikte-technologieën)
4. [API's](#apis)
5. [Belangrijke Functies](#belangrijke-functies)
6. [Onderhoud](#onderhoud)

## Overzicht

PDK Weather Pro is een weer-applicatie die het huidige weer en een 5-daagse weersverwachting toont voor elke opgezochte stad. De applicatie toont ook een stadsafbeelding, een interactieve kaart en grafieken met weergegevens.

## Project Structuur

```

## Gebruikte Technologieën

1. **Backend**
   - Flask (Python web framework)
   - Python requests library voor API calls

2. **Frontend**
   - HTML5 & CSS3
   - JavaScript (vanilla)
   - Bootstrap 5 (voor layout en styling)
   - Chart.js (voor grafieken)
   - Leaflet.js (voor kaarten)
   - Font Awesome (voor iconen)
   - DM Sans font (voor typografie)

## API's

De applicatie gebruikt drie externe API's:

1. **OpenWeatherMap API**
   - Gebruikt voor weer data
   - Endpoints:
     - `/data/2.5/weather` (huidig weer)
     - `/data/2.5/forecast` (5-daagse voorspelling)
   - Vereist API sleutel in `config.py`
   - Retourneert:
     - Temperatuur
     - Weerbeschrijving
     - Luchtvochtigheid
     - Windsnelheid
     - Weericons

2. **Unsplash API**
   - Gebruikt voor stadsafbeeldingen
   - Endpoint: `/search/photos`
   - Vereist API sleutel in `config.py`
   - Zoekt naar skyline afbeeldingen van steden
   - Retourneert URL van hoge kwaliteit afbeeldingen

3. **OpenStreetMap/Nominatim**
   - Gebruikt voor geocoding (stad → coördinaten)
   - Geen API sleutel nodig
   - Rate limiting ingebouwd
   - Zet stadsnamen om naar coördinaten voor de kaart

## Belangrijke Functies

### Backend (app.py)

1. `get_city_image(city)`
   - Haalt stadsafbeelding op via Unsplash
   - Parameters: stadsnaam
   - Retourneert URL van de afbeelding
   - Foutafhandeling ingebouwd

2. `get_weather(city)`
   - Haalt huidig weer op via OpenWeatherMap
   - Parameters: stadsnaam
   - Retourneert:
     - Temperatuur (°C)
     - Weerbeschrijving
     - Luchtvochtigheid (%)
     - Windsnelheid (km/u)

3. `get_forecast(city)`
   - Haalt 5-daagse voorspelling op
   - Parameters: stadsnaam
   - Verwerkt data naar bruikbaar formaat
   - Filtert op unieke datums

### Frontend (script.js)

1. `loadWeather(city)`
   - Hoofdfunctie voor ophalen weerdata
   - Roept backend API aan
   - Handelt fouten af
   - Triggert UI updates

2. `createCharts(data)`
   - Maakt grafieken met Chart.js
   - Toont:
     - Temperatuurverloop
     - Neerslagverwachting
     - Windsnelheid
   - Responsive design
   - Interactieve legenda

3. `initMap()`
   - Initialiseert Leaflet kaart
   - Standaard view op Amsterdam
   - Laadt lichte kaart-stijl
   - Handelt markers

4. `updateWeatherDisplay(city, data)`
   - Update alle UI elementen:
     - Achtergrondafbeelding
     - Weer informatie
     - Voorspelling cards
     - Grafieken
     - Kaartlocatie

## Onderhoud

### API Sleutels
1. Maak een kopie van `config.example.py` naar `config.py`
2. Vul je API sleutels in voor:
   - OpenWeatherMap (`API_KEY`)
   - Unsplash (`UNSPLASH_ACCESS_KEY`)
3. Houd sleutels geheim (niet committen naar Git)

### Veel voorkomende problemen

1. **Kaart laadt niet**
   - Controleer of Leaflet CSS/JS correct geladen zijn
   - Check console voor JavaScript errors
   - Controleer of map container zichtbaar is
   - Verifieer coördinaten format

2. **Weer data niet beschikbaar**
   - Controleer API sleutels in config.py
   - Controleer API limieten
   - Check netwerk requests in browser
   - Verifieer stad spelling

3. **Grafieken tonen niet correct**
   - Check console voor data format
   - Controleer Chart.js initialisatie
   - Verifieer canvas element
   - Check responsive opties

4. **Afbeeldingen laden niet**
   - Controleer Unsplash API limiet
   - Verifieer API sleutel
   - Check netwerk requests
   - Controleer fallback mechanisme

### Updates

- Bootstrap en andere libraries worden via CDN geladen
- Update versienummers in index.html indien nodig
- Test altijd in development voordat je naar productie gaat
- Houd libraries up-to-date voor security

### Backup

- Belangrijke bestanden om te backuppen:
  - config.py (bevat API sleutels)
  - Eventuele aanpassingen in templates/
  - Custom static bestanden
  - Aangepaste styling
  - JavaScript aanpassingen

### Monitoring

- Controleer regelmatig:
  - API limieten
  - Error logs
  - Performance metrics
  - Browser compatibiliteit

## Contact

Voor vragen over onderhoud of problemen:
- Check eerst de documentatie
- Controleer error logs
- Raadpleeg de API documentatie
- Neem contact op met de ontwikkelaars bij blijvende problemen

---

Laatste update: [Datum]
```
