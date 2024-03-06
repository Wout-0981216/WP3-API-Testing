from flask import g
import sqlite3
import os

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
    status = "nieuw"
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
    query = "SELECT COUNT(*) FROM Onderzoek WHERE status='nieuw';"
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


