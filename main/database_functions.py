from flask import g
import sqlite3
import os
import datetime

current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, 'lib\database', 'database.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database_path)
        db.row_factory = sqlite3.Row
    return db

def insert_ervaringsdeskundige_into_database(form):
    voornaam = form.get('firstname')
    achternaam = form.get('lastname')
    postcode = form.get('postcode')
    geslacht = form.get('sex')
    email = form.get('email')
    gebruikersnaam = form.get('username')
    wachtwoord = form.get('password')
    telefoonnummer = form.get('phonenumber')
    geboortedatum = form.get('birthdate')
    gebruikte_hulpmiddel = form.get('used_accessory')
    bijzonderheden = form.get('particularities')
    toezichthouder = int(form.get('guardian'))
    if toezichthouder == 1:
        naam_voogd_of_toezichthouder = form.get('name_guardian')
        email_adres_voogd = form.get('email_guardian')
        telefoonnummer_voogd = form.get('phonenumber_guardian')
    else:
        naam_voogd_of_toezichthouder = None
        email_adres_voogd = None
        telefoonnummer_voogd = None
    voorkeur_benadering = form.get('contact_preference')
    type_onderzoek = form.get('research_type')
    bijzonderheden_beschikbaarheid = form.get('particularities_availability')
    status = 'nieuw'
    beheerder_id = None
    datum_status_update = None
    beperking = form.get('disability')
    try:
      connection = get_db()
      cursor = connection.cursor()
      cursor.execute("""
                    INSERT INTO Ervaringsdeskundige (voornaam, achternaam, postcode, geslacht, email, gebruikersnaam, wachtwoord, telefoonnummer,
                    geboortedatum, gebruikte_hulpmiddel, bijzonderheden, toezichthouder, naam_voogd_of_toezichthouder, email_adres_voogd, telefoonnummer_voogd,
                    voorkeur_benadering, type_onderzoek, bijzonderheden_beschikbaarheid, status, beheerder_id, datum_status_update) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """, (voornaam,achternaam,postcode,geslacht,email,gebruikersnaam,wachtwoord,telefoonnummer,geboortedatum,gebruikte_hulpmiddel,bijzonderheden,
                          toezichthouder,naam_voogd_of_toezichthouder,email_adres_voogd,telefoonnummer_voogd,voorkeur_benadering,type_onderzoek,bijzonderheden_beschikbaarheid,
                          status,beheerder_id,datum_status_update,))
      connection.commit()
      msg = "Account added"
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        msg = f"Error in the INSERT: {e}"
    finally:
        if connection:
            cursor.close()
            connection = get_db()
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT id FROM Ervaringsdeskundige WHERE gebruikersnaam == ?
                            """, (gebruikersnaam,))
            id = cursor.fetchone()
            cursor.close()
            insert_ervaringsdeskundige_beperking_into_database(id[0], beperking)
            return msg

def insert_ervaringsdeskundige_beperking_into_database(id, beperking):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Ervaringsdeskundige_beperking (ervaringsdeskundige_id, beperking_id) VALUES (?,?)',(id,beperking,))
    connection.commit()
    cursor.close()

def select_type_beperkingen_from_database():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT type_beperking FROM beperking')
    type_beperkingen = cursor.fetchall()
    cursor.close()
    return type_beperkingen

def select_beperking_from_database_by_type(type):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT beperking, id FROM beperking WHERE type_beperking = ?',(type,))
    beperkingen = cursor.fetchall()
    cursor.close()
    return beperkingen


def beheerder_login(form):
    connection = get_db()
    cursor = connection.cursor()
    name = form.get('usernameInput')
    wachtwoord = form.get('passwordInput')
    query = 'SELECT wachtwoord FROM beheerder WHERE gebruikersnaam = ?'
    cursor.execute(query, (name,))
    user_data = cursor.fetchone()
    cursor.close()
    if(user_data[0] == wachtwoord):
        return True
    else: return False

def get_all_evd_from_database():
    connection = get_db()
    cursor = connection.cursor()
    query = "SELECT * FROM Ervaringsdeskundige"
    cursor.execute(query)
    user_data = cursor.fetchall()
    cursor.close()
    return user_data

def get_evd_from_database_by_status_nieuw():
    connection = get_db()
    cursor = connection.cursor()
    query = "SELECT * FROM Ervaringsdeskundige WHERE status = 'nieuw'"
    cursor.execute(query)
    user_data = cursor.fetchall()
    cursor.close()
    return user_data

def get_evd_from_database_by_id(id):
    connection = get_db()
    cursor = connection.cursor()
    query = "SELECT * FROM Ervaringsdeskundige WHERE id = ?"
    cursor.execute(query, (id,))
    user_data = cursor.fetchone()
    cursor.close()
    return user_data

def confirm_evd_status(id):
    try:
        connection = get_db()
        cursor = connection.cursor()
        current_datetime = datetime.datetime.now()
        beheerder_id = 1 #moet nog aangepast worden naar ID van de ingelogde beheerder
        query = "UPDATE Ervaringsdeskundige SET status = 'goedgekeurd', beheerder_id = ?, datum_status_update = ? WHERE id = ?"
        cursor.execute(query, (beheerder_id,current_datetime,id,))
        connection.commit()
        msg = "status updated"
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        msg = f"Error in the INSERT: {e}"
    finally:
        cursor.close()
        return msg

def deny_evd_status(id):
    try:
        connection = get_db()
        cursor = connection.cursor()
        current_datetime = datetime.datetime.now()
        beheerder_id = 1 #moet nog aangepast worden naar ID van de ingelogde beheerder
        query = "UPDATE Ervaringsdeskundige SET status = 'afgekeurd', beheerder_id = ?, datum_status_update = ? WHERE id = ?"
        cursor.execute(query, (beheerder_id,current_datetime,id,))
        connection.commit()
        msg = "status updated"
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        msg = f"Error in the INSERT: {e}"
    finally:
        cursor.close()
        return msg

def get_aanvragen():
    connection = get_db()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM Ervaringsdeskundige WHERE status='nieuw';"
    cursor.execute(query)
    count_aanvragen = cursor.fetchone()[0]
    cursor.close()
    return count_aanvragen

def get_onderzoeken():
    connection = get_db()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM Onderzoek WHERE status='nieuwe';"
    cursor.execute(query)
    count_onderzoeken = cursor.fetchone()[0]
    cursor.close()
    return count_onderzoeken

def get_evd():
    connection = get_db()
    cursor = connection.cursor()
    query = "SELECT count(*) FROM Inschrijving_ervaringsdeskundige_onderzoek  WHERE status='nieuw';"
    cursor.execute(query)
    count_evd = cursor.fetchone()[0]
    cursor.close()
    return count_evd


def get_onderzoek(params = {'beschikbaar': True}):
     connection = get_db()
     cursor = connection.cursor()
     print(params)
     cursor.execute("SELECT * FROM Onderzoek WHERE beschikbaar = ?", (params['beschikbaar'],))
     onderzoeks = cursor.fetchall()
     cursor.close()
     onderzoeks_as_dicts = [dict(row) for row in onderzoeks]
     return onderzoeks_as_dicts
# TO DO -remove alleen voor test
def insert_dom_data():
     connection = get_db()
     cursor = connection.cursor()
     cursor.execute('''INSERT INTO Onderzoek ("titel", "beschikbaar", "beschrijving", "datum_vanaf", "datum_tot", "type_onderzoek", "locatie", "met_beloning", "doelgroep_leeftijd_van", "doelgroep_leeftijd_tot", "organisatie_id", "status", "datum_status_update", "beheerder_id")
     VALUES ('Nieuw onderzoek', 1, 'Dit is een nieuw onderzoek', '2024-03-07', '2024-03-14', 'Kwalitatief', 'Amsterdam', 1, 18, 60, 1, 'nieuwe', '2024-03-07 12:00:00', 1);''')
     new_category_id = cursor.lastrowid
     print(new_category_id)
     connection.commit()
     cursor.close()
     return
 
def get_geregisteered_onderzoek(params = {'ervaringsdeskundige_id': -1, 'status': 'nieuw'}):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT Onderzoek.*, inschrijving_ervaringsdeskundige_onderzoek.status AS inschrijving_ervaringsdeskundige_onderzoek_status

    FROM Onderzoek
    INNER JOIN Inschrijving_ervaringsdeskundige_onderzoek ON Onderzoek.id = Inschrijving_ervaringsdeskundige_onderzoek.onderzoek_id
    WHERE Inschrijving_ervaringsdeskundige_onderzoek.ervaringsdeskundige_id = ?
""", ((params['ervaringsdeskundige_id'],)))

    geregisteeredOnderzoeks = cursor.fetchall()
    cursor.close()
    geregisteeredOnderzoeks_as_dicts = [dict(row) for row in geregisteeredOnderzoeks]
    return geregisteeredOnderzoeks_as_dicts
    
    
def inschrijven_onderzoek(ervaringsdeskundige_id, onderzoek_id, beheerder_id, status, Datum_laatste_status_update):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO Inschrijving_ervaringsdeskundige_onderzoek (ervaringsdeskundige_id, onderzoek_id, status, beheerder_id, Datum_laatste_status_update)
    VALUES (?, ?, ?, ?, ?)
""", (ervaringsdeskundige_id, onderzoek_id, status, beheerder_id, Datum_laatste_status_update))
    connection.commit()
    cursor.close()
    
def uitschrijven_onderzoek(onderzoek_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("""
    DELETE FROM Inschrijving_ervaringsdeskundige_onderzoek
    WHERE onderzoek_id = ?
""", (onderzoek_id,))
    connection.commit()
    cursor.close()
    
def get_onderzoek_by_id(id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Onderzoek WHERE id = ?""", (id,) )
    onderzoek = cursor.fetchone()
    cursor.close()
    return dict(onderzoek) if not None else {}

def get_inschrijvingen_op_onderzoeken():
    connection = get_db()
    cursor = connection.cursor()
    query = ("""SELECT * FROM Inschrijving_ervaringsdeskundige_onderzoek 
                INNER JOIN Ervaringsdeskundige ON Ervaringsdeskundige.id = Inschrijving_ervaringsdeskundige_onderzoek.ervaringsdeskundige_id 
                INNER JOIN Onderzoek ON Onderzoek.id = Inschrijving_ervaringsdeskundige_onderzoek.onderzoek_id 
                WHERE Inschrijving_ervaringsdeskundige_onderzoek.status = 'nieuw'""")
    cursor.execute(query)
    inschrijving_onderzoek = cursor.fetchall()
    cursor.close()
    return inschrijving_onderzoek

def get_alle_inschrijvingen_op_onderzoeken():
    connection = get_db()
    cursor = connection.cursor()
    query = ("""SELECT * FROM Inschrijving_ervaringsdeskundige_onderzoek 
                INNER JOIN Ervaringsdeskundige ON Ervaringsdeskundige.id = Inschrijving_ervaringsdeskundige_onderzoek.ervaringsdeskundige_id 
                INNER JOIN Onderzoek ON Onderzoek.id = Inschrijving_ervaringsdeskundige_onderzoek.onderzoek_id """)
    cursor.execute(query)
    alle_inschrijvingen = cursor.fetchall()
    cursor.close()
    return alle_inschrijvingen


def confirm_inschrijving_status(onderzoek_id):
    try:
        connection = get_db()
        cursor = connection.cursor()
        current_datetime = datetime.datetime.now()
        beheerder_id = 1  # moet nog veranderd worden

        query = ("UPDATE Inschrijving_ervaringsdeskundige_onderzoek SET "
                 "status = 'goedgekeurd', beheerder_id = ?, "
                 "datum_laatste_status_update = ? WHERE onderzoek_id = ?")
        cursor.execute(query, (beheerder_id, current_datetime, onderzoek_id))

        connection.commit()
        msg = "Status updated successfully."
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        msg = f"Error in updating status: {e}"
    finally:
        cursor.close()
        return msg

def deny_inschrijving_status(onderzoek_id):
    try:
        connection = get_db()
        cursor = connection.cursor()
        current_datetime = datetime.datetime.now()
        beheerder_id = 1  # moet nog veranderd worden

        query = ("UPDATE Inschrijving_ervaringsdeskundige_onderzoek SET "
                 "status = 'afgekeurd', beheerder_id = ?, "
                 "datum_laatste_status_update = ? WHERE onderzoek_id = ?")
        cursor.execute(query, (beheerder_id, current_datetime, onderzoek_id))

        connection.commit()
        msg = "Status updated successfully."
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        msg = f"Error in updating status: {e}"
    finally:
        cursor.close()
        return msg


def get_new_onderzoeken():
    connection = get_db()
    cursor = connection.cursor()
    query = ("""SELECT * FROM Onderzoek LEFT JOIN beperking on Onderzoek.doelgroep_beperking = beperking.id WHERE status = 'nieuwe'""")
    cursor.execute(query)
    onderzoeken = cursor.fetchall()
    cursor.close()
    return onderzoeken


def confirm_onderzoek_status(id):
    try:
        connection = get_db()
        cursor = connection.cursor()
        current_datetime = datetime.datetime.now()
        beheerder_id = 1  # moet nog veranderd worden

        query = ("UPDATE Onderzoek SET "
                 "status = 'goedgekeurd', beheerder_id = ?, "
                 "datum_status_update = ? WHERE id = ?")
        cursor.execute(query, (beheerder_id, current_datetime, id))

        connection.commit()
        msg = "Status updated successfully."
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        msg = f"Error in updating status: {e}"
    finally:
        cursor.close()
        return msg

def deny_onderzoek_status(id):
    try:
        connection = get_db()
        cursor = connection.cursor()
        current_datetime = datetime.datetime.now()
        beheerder_id = 1  # moet nog veranderd worden

        query = ("UPDATE Onderzoek SET "
                 "status = 'afgekeurd', beheerder_id = ?, "
                 "datum_status_update = ? WHERE id = ?")
        cursor.execute(query, (beheerder_id, current_datetime, id))

        connection.commit()
        msg = "Status updated successfully."
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        msg = f"Error in updating status: {e}"
    finally:
        cursor.close()
        return msg
