from flask import Flask
from auth import auth_blueprint

from ervaringsdeskundige import ervaringsdeskundige_blueprint
from beheerder import beheerder_blueprint





app = Flask(__name__)

app.secret_key = 'super secret key'
app.register_blueprint(auth_blueprint)

app.register_blueprint(ervaringsdeskundige_blueprint)



app.register_blueprint(beheerder_blueprint)




if __name__ == '__main__':
    app.run(debug=True)



# Alaa zou je als je tijd hebt nog kunnen werken aan de volgende punten: 
# 1. de opmaak van de ervaringsdeskundige pagina ongeveer hetzelfde maken als de beheerdspagina. done
# 3. Ik dacht aan een soort dashboard  blokkwaarin je meerdereen had met een blok van openstaande onderzoeken 1 blok van geregistreerde onderzoeken en 1 blok met goedgekeurde onderzoeken. en 1 blok van afgekeurde onderzoeken na inschrijving maar hierin kun je zelf iets verzinnen. 
# Wil je laten weten of je dit gaat lukken? done
    

# 2. De ervaringsdeskundigen zien bij login welke onderzoeksvragen er open staan op basis van hun voorkeuren en de "filters" van het onderzoek. 
# dus vooral zorgen dat de persoon die ingelogd is alleen onderzoeken krijgt te zien op basis van voorkeur zoals benadering via telefoon.
