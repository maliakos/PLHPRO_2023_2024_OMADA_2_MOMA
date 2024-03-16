import sqlite3
import json
import os

# Φαντάζομαι θα θέλει η ΒΔ να δημιουργείται εντός προγράμματος,
# οπότε έβαλα ένα check σε περίπτωση που υπάρχει, αν ξανατρέξεις
# το πρόγραμμα να μην προσπαθήσει να τη δημιουργήσει πάλι.
if not os.path.exists('moma.db'):
    conn = sqlite3.connect('moma.db')
    cursor = conn.cursor()

    with open('Artists.json', 'r', encoding='utf-8') as f:
        Artists_data = json.load(f)

    with open('Artworks.json', 'r', encoding='utf-8') as f:
        Artworks_data = json.load(f)

    # Δημιουργία πίνακα Artists, PK το ConstituentID
    cursor.execute('''CREATE TABLE Artists(
                ConstituentID INT PRIMARY KEY NOT NULL,
                DisplayName TEXT,
                ArtistBio TEXT,
                Nationality TEXT,
                Gender TEXT,
                BeginDate INT,
                EndDate INT,
                "Wiki QID" TEXT,
                ULAN INT)   ''')

    for x in Artists_data:
        # Μερικές τιμές είναι NULL οπότε ελέγχω την ύπαρξη ή μη πριν την εισαγωγή
        ConstituentID = x.get('ConstituentID', None)
        DisplayName = x.get('DisplayName', None)
        ArtistBio = x.get('ArtistBio', None)
        Nationality = x.get('Nationality', None)
        Gender = x.get('Gender', None)
        BeginDate = x.get('BeginDate', None)
        EndDate = x.get('EndDate', None)
        Wiki_QID = x.get('Wiki QID', None)
        ULAN = x.get('ULAN', None)

        # Εισαγωγή στοιχείων στις στήλες του Artists.
        cursor.execute(''' INSERT INTO Artists (ConstituentID, DisplayName, ArtistBio, Nationality, Gender, BeginDate, EndDate, "Wiki QID", ULAN )
                    VALUES (?,?,?,?,?,?,?,?,?)''', (
        ConstituentID, DisplayName, ArtistBio, Nationality, Gender, BeginDate,
        EndDate, Wiki_QID, ULAN))

    # Δημιουργία πίνακα Artworks, ObjectID το PK
    cursor.execute('''CREATE TABLE Artworks(
                Title TEXT,
                Artist TEXT,
                ConstituentID INT,
                ArtistBio TEXT,
                Nationality TEXT,
                BeginDate INT,
                EndDate INT,
                Gender TEXT,
                Date TEXT,
                Medium TEXT,
                Dimensions TEXT,
                CreditLine TEXT,
                AccessionNumber TEXT,
                Classification TEXT,
                Department TEXT,
                DateAcquired TEXT,
                Cataloged TEXT,
                ObjectID TEXT PRIMARY KEY NOT NULL,
                URL TEXT,
                ImageURL TEXT,
                OnView TEXT,
                Circumference_cm FLOAT,
                Depth_cm FLOAT,
                Diameter_cm FLOAT,
                Height_cm FLOAT,
                Length_cm FLOAT,
                Weight_kg FLOAT,
                Width_cm FLOAT,
                SeatHeight_cm FLOAT,
                Duration_sec FLOAT,
                FOREIGN KEY (Artist) REFERENCES Artists(DisplayName),
                FOREIGN KEY (ConstituentID) REFERENCES Artists(ConstituentID),
                FOREIGN KEY (ArtistBio) REFERENCES Artists(ArtistBio),
                FOREIGN KEY (Nationality) REFERENCES Artists(Nationality),
                FOREIGN KEY (Gender) REFERENCES Artists(Gender),
                FOREIGN KEY (BeginDate) REFERENCES Artists(BeginDate),
                FOREIGN KEY (EndDate) REFERENCES Artists(EndDate) )''')

    # Εδώ στο json μερικά στοιχεία ήταν σε λίστες :/
    for y in Artworks_data:
        Title = y.get('Title', None)
        Artist = ', '.join(y.get('Artist', []))
        ConstituentID = int(y.get('ConstituentID', [0])[0]) if y.get(
            'ConstituentID', [0]) else None
        ArtistBio = ', '.join(y.get('ArtistBio', []))
        Nationality = ', '.join(y.get('Nationality', []))
        BeginDate = int(y.get('BeginDate', [0])[0]) if y.get('BeginDate',
                                                             [0]) else None
        EndDate = int(y.get('EndDate', [0])[0]) if y.get('EndDate',
                                                         [0]) else None
        Gender = ', '.join(y.get('Gender', []))
        Date = y.get('Date', None)
        Medium = y.get('Medium', None)
        Dimensions = y.get('Dimensions', None)
        CreditLine = y.get('CreditLine', None)
        AccessionNumber = y.get('AccessionNumber', None)
        Classification = y.get('Classification', None)
        Department = y.get('Department', None)
        DateAcquired = y.get('DateAcquired', None)
        Cataloged = y.get('Cataloged', None)
        ObjectID = y.get('ObjectID', None)
        URL = y.get('URL', None)
        ImageURL = y.get('ImageURL', None)
        OnView = y.get('OnView', None)
        Circumference_cm = y.get('Circumference (cm)', None)
        Depth_cm = y.get('Depth (cm)', None)
        Diameter_cm = y.get('Diameter (cm)', None)
        Height_cm = y.get('Height (cm)', None)
        Length_cm = y.get('Length (cm)', None)
        Weight_kg = y.get('Weight (kg)', None)
        Width_cm = y.get('Width (cm)', None)
        SeatHeight_cm = y.get('SeatHeight (cm)', None)
        Duration_sec = y.get('Duration (sec.)', None)

        # Εισαγωγή στοιχείων στις στήλες του Artworks.
        cursor.execute('''INSERT INTO Artworks (Title, Artist, ConstituentID, ArtistBio, Nationality, BeginDate, EndDate, Gender, Date, Medium, Dimensions, CreditLine, AccessionNumber, Classification, Department, DateAcquired, Cataloged, ObjectID, URL, ImageURL, OnView, Circumference_cm, Depth_cm, Diameter_cm, Height_cm, Length_cm, Weight_kg, Width_cm, SeatHeight_cm, Duration_sec)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                       (Title, Artist, ConstituentID, ArtistBio, Nationality,
                        BeginDate, EndDate, Gender, Date, Medium, Dimensions,
                        CreditLine, AccessionNumber, Classification, Department,
                        DateAcquired, Cataloged, ObjectID, URL, ImageURL,
                        OnView, Circumference_cm, Depth_cm, Diameter_cm,
                        Height_cm, Length_cm, Weight_kg, Width_cm,
                        SeatHeight_cm, Duration_sec))

    conn.commit()

    cursor.close()

    conn.close()
