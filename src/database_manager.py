import sqlite3
from sqlite3 import Error
import json
import os


class DatabaseManager:
    def __init__(self):
        if not os.path.exists('moma.db') or os.path.getsize('moma.db') == 0:
            try:
                self.create_db()
            except Error as e:
                print(e)
        self.connection = sqlite3.connect('moma.db')

    def get_connection(self):
        return self.connection

    @staticmethod
    def create_db():
        conn = sqlite3.connect('moma.db')
        cursor = conn.cursor()

        with open('Artists.json', 'r', encoding='utf-8') as f:
            Artists_data = json.load(f)

        with open('Artworks.json', 'r', encoding='utf-8') as f:
            Artworks_data = json.load(f)

        

        # Δημιουργία πίνακα Artworks, ObjectID το PK
        cursor.execute('''CREATE TABLE Artworks(
                    ObjectID TEXT PRIMARY KEY NOT NULL,
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
                    Duration_sec FLOAT)''')

        # Εδώ στο json μερικά στοιχεία ήταν σε λίστες :/
        for y in Artworks_data:
            if  y.get('Department') == 'Painting & Sculpture' or y.get('Department') == 'Media and Performance':
                ObjectID = y.get('ObjectID', None)
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
                    ULAN INT,
                    FOREIGN KEY (ConstituentID) REFERENCES Artworks(ConstituentID))   ''')

        for x in Artists_data:
            # Μερικές τιμές είναι NULL οπότε ελέγχω την ύπαρξη ή μη πριν την εισαγωγή
            ConstituentID = x.get('ConstituentID', None)
            cursor.execute('SELECT COUNT(*) FROM Artworks WHERE ConstituentID = ?', (ConstituentID,))
            count = cursor.fetchone()[0]
            if count > 0:
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


        conn.commit()

        cursor.close()

        conn.close()
