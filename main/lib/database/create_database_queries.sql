CREATE TABLE IF NOT EXISTS Organisatie (
  "id" integer PRIMARY KEY,
  "aam" varchar,
  "type" varchar,
  "website" varchar,
  "beschrijving" varchar,
  "contactpersoon" varchar,
  "email" varchar,
  "telefoonnummer" integer,
  "overige_details" varchar
);
CREATE TABLE IF NOT EXISTS Beperking (
  "id" integer PRIMARY KEY,
  "beperking" varchar,
  "type_beperking" varchar
);
CREATE TABLE IF NOT EXISTS Beheerder (
  "id" integer PRIMARY KEY,
  "gebuikersnaam" varchar UNIQUE,
  "wachtwoord" varchar,
  "voornaam" varchar,
  "achternaam" varchar,
  "team" varchar
);
CREATE TABLE IF NOT EXISTS Onderzoek (
  "id" integer PRIMARY KEY,
  "titel" varchar,
  "beschikbaar" integer,
  "beschrijving" varchar,
  "datum_vanaf" date,
  "datum_tot" date,
  "type_onderzoek" varchar,
  "locatie" varchar,
  "met_beloning" integer,
  "beloning" varchar,
  "doelgroep_leeftijd_van" integer,
  "doelgroep_leeftijd_tot" integer,
  "doelgroep_beperking" integer,
  "organisatie_id" integer,
  "status" varchar,
  "datum_status_update" timestamp,
  "beheerder_id" integer,
  FOREIGN KEY ("beheerder_id") REFERENCES Beheerder("id")
  FOREIGN KEY ("doelgroep_beperking") REFERENCES Beperking("id")
  FOREIGN KEY ("organisatie_id") REFERENCES Organisatie("id")
);
CREATE TABLE IF NOT EXISTS Ervaringsdeskundige (
  "id" integer PRIMARY KEY,
  "voornaam" varchar,
  "achternaam" varchar,
  "postcode" varchar,
  "geslacht" varchar,
  "email" varchar,
  "gebruikersnaam" varchar UNIQUE,
  "wachtwoord" varchar,
  "telefoonnummer" integer,
  "geboortedatum" date,
  "gebruikte_hulpmiddel" varchar,
  "bijzonderheden" varchar,
  "toezichthouder" integer,
  "naam_voogd_of_toezichthouder" varchar,
  "email_adres_voogd" varchar,
  "telefoonnummer_voogd" integer,
  "voorkeur_benadering" varchar,
  "type_onderzoek" varchar,
  "bijzonderheden_beschikbaarheid" varchar
  "status" varchar,
  "beheerder_id" integer,
  "datum_status_update" timestamp,
  FOREIGN KEY ("beheerder_id") REFERENCES Beheerder("id")
);
CREATE TABLE IF NOT EXISTS Onderzoeks_vraag (
  "id" integer PRIMARY KEY,
  "titel" varchar,
  "vraag" text,
  "onderzoek_id" integer,
  FOREIGN KEY("onderzoek_id") REFERENCES Onderzoek("id")
);
CREATE TABLE IF NOT EXISTS Ervaringsdeskundige_beperking (
  "ervaringsdeskundige_id" integer,
  "beperking_id" integer,
  PRIMARY KEY ("ervaringsdeskundige_id", "beperking_id")
  FOREIGN KEY ("ervaringsdeskundige_id") REFERENCES Ervaringsdeskundige("id"),
  FOREIGN KEY ("beperking_id") REFERENCES Beperking("id")
);
CREATE TABLE IF NOT EXISTS Inschrijving_ervaringsdeskundige_onderzoek (
  "ervaringsdeskundige_id" integer,
  "onderzoek_id" integer,
  "status" varchar,
  "beheerder_id" integer,
  "Datum_laatste_status_update" timestamp,
  PRIMARY KEY ("ervaringsdeskundige_id", "onderzoek_id"),
  FOREIGN KEY ("ervaringsdeskundige_id") REFERENCES Ervaringsdeskundige("id"),
  FOREIGN KEY ("beheerder_id") REFERENCES Beheerder("id"),
  FOREIGN KEY ("onderzoek_id") REFERENCES Onderzoek("id")
);