CREATE TABLE IF NOT EXISTS Organisatie (
  id integer PRIMARY KEY AUTOINCREMENT,
  "naam" varchar,
  "type" varchar,
  "website" varchar,
  "beschrijving" varchar,
  "contactpersoon" varchar,
  "email" varchar,
  "telefoonnummer" integer,
  "overige_details" varchar
);
CREATE TABLE IF NOT EXISTS Beperking (
  "id" integer PRIMARY KEY AUTOINCREMENT,
  "beperking" varchar,
  "type_beperking" varchar
);
CREATE TABLE IF NOT EXISTS Beheerder (
  "id" integer PRIMARY KEY AUTOINCREMENT,
  "gebruikersnaam" varchar UNIQUE,
  "wachtwoord" varchar,
  "voornaam" varchar,
  "achternaam" varchar,
  "team" varchar,
  "is_admin" integer
);
CREATE TABLE IF NOT EXISTS Onderzoek (
  "id" integer PRIMARY KEY AUTOINCREMENT,
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
  "id" integer PRIMARY KEY AUTOINCREMENT,
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
  "bijzonderheden_beschikbaarheid" varchar,
  "status" varchar,
  "beheerder_id" integer,
  "datum_status_update" timestamp,
  FOREIGN KEY ("beheerder_id") REFERENCES Beheerder("id")
);
CREATE TABLE IF NOT EXISTS Onderzoeks_vraag (
  "id" integer PRIMARY KEY AUTOINCREMENT,
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
INSERT INTO Beperking ('beperking', 'type_beperking') VALUES ('Doof','Auditieve Beperkingen'),('Slechthorend','Auditieve Beperkingen'),('Doofblind', 'Auditieve Beperkingen'),
('Blind','Visuele Beperkingen'),('Slechtziend','Visuele Beperkingen'),('Kleurenblind','Visuele Beperkingen'),('Amputatie en mismaaktheid', 'Motorische / Lichamelijke Beperkingen'),
('Artritus', 'Motorische / Lichamelijke Beperkingen'),('Fibromyalgie', 'Motorische / Lichamelijke Beperkingen'),('Reuma', 'Motorische / Lichamelijke Beperkingen'),('Verminderde handvaardigheid', 'Motorische / Lichamelijke Beperkingen'),
('Spierdystrofie', 'Motorische / Lichamelijke Beperkingen'),('RSI', 'Motorische / Lichamelijke Beperkingen'),('Tremor en Spasmen', 'Motorische / Lichamelijke Beperkingen'),('Quadriplegie of tetraplegie', 'Motorische / Lichamelijke Beperkingen'),
('ADHD','Cognitieve / Neurologische Beperkingen'),('Autisme','Cognitieve / Neurologische Beperkingen'),('Leerstoornis','Cognitieve / Neurologische Beperkingen'),
('Geheugen beperking','Cognitieve / Neurologische Beperkingen'),('Epilepsie','Cognitieve / Neurologische Beperkingen'),('Migraine','Cognitieve / Neurologische Beperkingen');

INSERT INTO Beheerder ('gebruikersnaam','wachtwoord','voornaam','achternaam','team','is_admin') VALUES ('admin','admin','admin','admin','admin','1');

INSERT INTO Organisatie ('naam', 'type', 'website', 'beschrijving', 'contactpersoon', 'email', 'telefoonnummer', 'overige_details') VALUES ('Organisatie1', 'Organisatie', 'www.Organisatie1.nl', 'Organisatie1 is een organisatie', 'contactpersoon Organisatie1', 'Organisatie1@gmail.com', 0612345678, 'Organisatie1 details');

INSERT INTO Onderzoek ('titel', 'beschikbaar', 'beschrijving', 'datum_vanaf', 'datum_tot', 'type_onderzoek', 'locatie', 'met_beloning', 'beloning', 'doelgroep_leeftijd_van', 'doelgroep_leeftijd_tot', 'doelgroep_beperking', 'organisatie_id', 'status', 'datum_status_update', 'beheerder_id') VALUES ('Onderzoek voor doven', 1, 'Onderzoek voor doven', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 1, 1, 'goedgekeurd', null, null),
('Onderzoek voor slechthorenden', 1, 'Onderzoek voor slechthorenden', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 2, 1, 'goedgekeurd', null, null),
('Onderzoek voor doofblinden', 1, 'Onderzoek voor doofblinden', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 3, 1, 'goedgekeurd', null, null),
('Onderzoek voor blinden', 1, 'Onderzoek voor blinden', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 4, 1, 'goedgekeurd', null, null),
('Onderzoek voor slechtzienden', 1, 'Onderzoek voor slechtzienden', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 5, 1, 'goedgekeurd', null, null),
('Onderzoek voor kleurenblinden', 1, 'Onderzoek voor kleurenblinden', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 6, 1, 'goedgekeurd', null, null),
('Onderzoek voor amputatie en mismaaktheid', 1, 'Onderzoek voor amputatie en mismaaktheid', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 7, 1, 'goedgekeurd', null, null),
('Onderzoek voor artritus', 1, 'Onderzoek voor artritus', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 8, 1, 'goedgekeurd', null, null),
('Onderzoek voor fibromyalgie', 1, 'Onderzoek voor fibromyalgie', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 9, 1, 'goedgekeurd', null, null),
('Onderzoek voor reuma', 1, 'Onderzoek voor reuma', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 10, 1, 'goedgekeurd', null, null),
('Onderzoek voor verminderde handvaardigheid', 1, 'Onderzoek voor verminderde handvaardigheid', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 11, 1, 'goedgekeurd', null, null),
('Onderzoek voor spierdystrofie', 1, 'Onderzoek voor spierdystrofie', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 12, 1, 'goedgekeurd', null, null),
('Onderzoek voor RSI', 1, 'Onderzoek voor RSI', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 13, 1, 'goedgekeurd', null, null),
('Onderzoek voor tremor en spasmen', 1, 'Onderzoek voor tremor en spasmen', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 14, 1, 'goedgekeurd', null, null),
('Onderzoek voor quadriplegie of tetraplegie', 1, 'Onderzoek voor quadriplegie of tetraplegie', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 15, 1, 'goedgekeurd', null, null),
('Onderzoek voor ADHD', 1, 'Onderzoek voor ADHD', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 16, 1, 'goedgekeurd', null, null),
('Onderzoek voor autisme', 1, 'Onderzoek voor autisme', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 17, 1, 'goedgekeurd', null, null),
('Onderzoek voor leerstoornis', 1, 'Onderzoek voor leerstoornis', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 18, 1, 'goedgekeurd', null, null),
('Onderzoek voor geheugenbeperking', 1, 'Onderzoek voor geheugenbeperking', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 19, 1, 'goedgekeurd', null, null),
('Onderzoek voor epilepsie', 1, 'Onderzoek voor epilepsie', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 20, 1, 'goedgekeurd', null, null),
('Onderzoek voor migraine', 1, 'Onderzoek voor migraine', '2024-03-10', '2024-06-10', 'telephone', 'Rotterdam', 1, null, 0, 99, 21, 1, 'goedgekeurd', null, null);