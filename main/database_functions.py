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
            return msg


