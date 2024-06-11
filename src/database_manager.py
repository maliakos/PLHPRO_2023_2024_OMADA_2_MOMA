import sqlite3
import json
import os


class DatabaseManager:
    def __init__(self):
        #Ελέγχουμε την ύπαρξη της ΒΔ, εάν υπάρχει τη δημιουργούμε
        if not os.path.exists('moma.db') or os.path.getsize('moma.db') == 0:
            try:
                self.create_db()
            except sqlite3.Error as e:
                print(f"Error creating Database:{e}")

    #Μέθοδος για σύνδεση με τη ΒΔ
    def get_connection(self):
        self.connection = sqlite3.connect('moma.db')

        return self.connection

    
    def create_db(self):
        #Δημιουργία της ΒΔ
        conn = sqlite3.connect('moma.db')
        cursor = conn.cursor()
        self.IDs = []
        self.create_artworks(cursor)
        self.create_artists(cursor)

        self.json_management(cursor)

        conn.commit()

        cursor.close()

        conn.close()

    def create_artworks(self, cursor):
        # Δημιουργία πίνακα Artworks, ObjectID το PK
        cursor.execute('''CREATE TABLE Artworks(
                    ObjectID TEXT PRIMARY KEY NOT NULL,
                    Title TEXT,
                    Artist TEXT,
                    ConstituentID TEXT,
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
    
    def create_artists(self, cursor):
        # Δημιουργία πίνακα Artists, PK το ConstituentID
        cursor.execute('''CREATE TABLE Artists(
                    ConstituentID TEXT PRIMARY KEY NOT NULL,
                    DisplayName TEXT,
                    ArtistBio TEXT,
                    Nationality TEXT,
                    Gender TEXT,
                    BeginDate INT,
                    EndDate INT,
                    "Wiki QID" TEXT,
                    ULAN INT,
                    FOREIGN KEY (ConstituentID) REFERENCES Artworks(ConstituentID))   ''')
        
    def  json_management(self, cursor):
        #Φόρτωση των δεδομένων από τα json αρχεία
        with open('Artists.json', 'r', encoding='utf-8') as f:
            Artists_data = json.load(f)

        with open('Artworks.json', 'r', encoding='utf-8') as f:
            Artworks_data = json.load(f)

        self.insert_artworks(cursor, Artworks_data)
        self.insert_artists(cursor, Artists_data)
        

    def insert_artworks(self, cursor, Artworks_data):
        # Εισαγωγή δεδομένων στον πίνακα Artworks
        for y in Artworks_data:
            departments = ['Painting & Sculpture', 'Media and Performance']
            #Χρησιμοποιούμε μόνο τα στοιχεία με όνομα Painting & Sculpture ή Media and Performance στο πεδίο Department
            #Χρήση κατάλληλων μεθόδων για την απόκτηση στοιχείων που βρίσκονται σε λίστες στο json
            if  y.get('Department') in departments:
                try:
                    ObjectID = y.get('ObjectID', None)
                    Title = y.get('Title', None)
                    Artist = ', '.join(y.get('Artist', []))

                    ConstituentID_list = y.get('ConstituentID', [])
                    ConstituentID = ','.join(map(str, ConstituentID_list))
                
                    for id in ConstituentID_list:
                        self.ID_Search(id)

                    
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
                    cursor.execute('''INSERT INTO Artworks (Title, Artist, ConstituentID, Date, Medium, Dimensions, CreditLine, AccessionNumber, Classification, Department, DateAcquired, Cataloged, ObjectID, URL, ImageURL, OnView, Circumference_cm, Depth_cm, Diameter_cm, Height_cm, Length_cm, Weight_kg, Width_cm, SeatHeight_cm, Duration_sec)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                            (Title, Artist, ConstituentID, 
                                Date, Medium, Dimensions,
                                CreditLine, AccessionNumber, Classification, Department,
                                DateAcquired, Cataloged, ObjectID, URL, ImageURL,
                                OnView, Circumference_cm, Depth_cm, Diameter_cm,
                                Height_cm, Length_cm, Weight_kg, Width_cm,
                                SeatHeight_cm, Duration_sec))
                except sqlite3.Error as e:
                    print(f"Error inserting Artwork: {e}")
    
    def insert_artists(self, cursor, Artists_data):

        
        for x in Artists_data:
            #Εισαγωγή δεδομένων στον πίνακα Artists
            #Έλεγχος αν το ID υπάρχει σε κάποιο έργο στον Artworks, προκειμένου να υπάρχουν στον πίνακα μόνο καλλιτέχνες με έργα στη ΜοΜΑ
            try:
                ConstituentID = x.get('ConstituentID', None)
                
                
                if ConstituentID in self.IDs:
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

            except sqlite3.Error as e:
                print(f"Error inserting Artist:{e}")

    def ID_Search(self, ConstituentID):
        self.IDs.append(ConstituentID)