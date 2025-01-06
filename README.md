# Fundmünzen

## Beschreibung

Dieses Projekt zielt darauf ab, Münzen in Bildern mithilfe fortschrittlicher Bildverarbeitungstechniken und Clustering zu erkennen und zu klassifizieren.

### Voraussetzungen

Anforderungen an die Software und andere Tools zum Erstellen, Testen und Pushen:
- [Python 3.7+](https://www.python.org/downloads/)
- [OpenCV](https://opencv.org/)
- [TensorFlow](https://www.tensorflow.org/)
- [NumPy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)

## Installation

Eine schrittweise Reihe von Beispielen, die Ihnen zeigen, wie Sie eine Entwicklungsumgebung einrichten:

1. Klonen Sie das Repository:
    ```bash
    git clone https://code.ovgu.de/altalab/fundmuenzen.git
    cd fundmuenzen
    ```

2. Erstellen Sie eine virtuelle Umgebung (optional, aber empfohlen):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Auf Windows: venv\Scripts\activate
    ```

3. Installieren Sie die erforderlichen Abhängigkeiten:
    ```bash
    pip install -r requirements.txt
    ```

## Ausführen des Projekts

1. Aktivieren Sie die virtuelle Umgebung (falls Sie eine erstellt haben):
    ```bash
    source venv/bin/activate  # Auf Windows: venv\Scripts\activate
    ```

2. Führen Sie das Hauptskript aus:
    ```bash
    python main.py
    ```

3. Folgen Sie den Anweisungen auf dem Bildschirm, um ein Bild auszuwählen und die Münzerkennung durchzuführen.

## Bilddatenverarbeitungs-Workflow

### Bild-Eingabe
Benutzereingabe: Der Benutzer wählt eine Bilddatei aus, die Münzen enthält. Dies kann über Folgendes erfolgen:
- Eine grafische Benutzeroberfläche (GUI)

### Vorverarbeitung
Das Bild wird einer Vorverarbeitung unterzogen, um seine Qualität zu verbessern und es für die Analyse geeignet zu machen. Dies kann folgende Schritte umfassen:

#### Grauwertbild-Konvertierung
Das Bild wird in Graustufen konvertiert, um die Daten zu vereinfachen und die rechnerische Komplexität zu reduzieren.

#### Rauschreduzierung
Anwendung von Filtern (z. B. Gaußscher Unschärfefilter), um Rauschen zu reduzieren, das die Erkennungsgenauigkeit beeinträchtigen könnte.

#### Schwellenwertbildung
Verwendung von Techniken wie der Otsu-Methode, um ein binäres Bild zu erstellen, das die Münzen vom Hintergrund hervorhebt.

### Münzerkennung
#### Kantenerkennung
Das Programm wendet Kantenerkennungsalgorithmen (z. B. Canny-Kantenerkennung) an, um die Umrisse der Münzen zu identifizieren.
#### Konturfindung
Das Programm findet Konturen, die die Formen der Münzen darstellen.
##### Kreis-Erkennung
Verwendung von Techniken wie der Hough-Kreis-Transformation, um speziell kreisförmige Formen zu erkennen, die den Münzen entsprechen.

### Feature Extraktion
Für jede erkannte Münze extrahiert das Programm Merkmale wie:
#### Größe
Durchmesser oder Radius der Münze.
#### Form
Bestätigung, dass die erkannte Form kreisförmig ist.
#### Farbe
Analyse der Farbe der Münze, um sie zu klassifizieren.

### Klassifikation
#### Modellvorhersage
Das Programm verwendet ein vortrainiertes Deep-Learning-Modell, um die erkannten Münzen basierend auf den extrahierten Merkmalen zu klassifizieren.

### Ausgabeerstellung
Ergebniskomposition: Das Programm erstellt die Ergebnisse des Erkennungs- und Klassifikationsprozesses, einschließlich:
- Der Anzahl der erkannten Münzen,
- Der Typen und Werte der Münzen.

#### Benutzereingabe
Der Benutzer kann angeben, ob er die Ergebnisse auf dem Bildschirm anzeigen oder in einer Datei (z. B. im CSV-Format) speichern möchte.

## Funktionen

- **Münzidentifikation**: Erkennung und Klassifizierung von verschiedenen Münztypen in Bildern.
- **Wertbestimmung**: Bestimmung des Wertes der erkannten Münzen.
- **Bildverarbeitung**: Verwendung von OpenCV für die Vorverarbeitung und Analyse von Bildern.
- **CSV-Ausgabe**: Möglichkeit, die Ergebnisse in eine CSV-Datei zu exportieren.

## Tests ausführen

Erklären Sie, wie Sie die automatisierten Tests für dieses System ausführen.

### Beispieltests

Die Tests überprüfen die Genauigkeit des Münzdetektionsalgorithmus und dessen Fähigkeit, Münzen korrekt zu klassifizieren. Sie können beispielsweise den folgenden Befehl ausführen, um die Tests auszuführen:
```bash
pytest tests/test_coin_detection.py