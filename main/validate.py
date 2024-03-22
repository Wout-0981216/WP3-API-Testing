from datetime import datetime

def is_een_geldige_kandidaat(evd, onderzoek):
    # check if research is available
    if onderzoek["beschikbaar"] == 0 or onderzoek["beschikbaar"] == False :
        return False
    
    if onderzoek["type_onderzoek"] != evd["type_onderzoek"]:
        return False
    # check if evd is valid candidate based on the age 
    evd_birthdate = datetime.strptime(evd["geboortedatum"], "%Y-%m-%d")
    onderzoek_min_age = onderzoek["doelgroep_leeftijd_van"]
    onderzoek_max_age = onderzoek["doelgroep_leeftijd_tot"]
    current_date = datetime.now()
    evd_age = current_date.year - evd_birthdate.year - ((current_date.month, current_date.day) < (evd_birthdate.month, evd_birthdate.day))
    if not (onderzoek_min_age <= evd_age <= onderzoek_max_age):
        return False
    if "beperkinging" in evd: 
     listofberperking = []
     for beperking in evd["beperkinging"]:
        listofberperking.append(beperking["id"])
     if onderzoek["doelgroep_beperking"] not in listofberperking:
        return False
    onderzoek_start_date = datetime.strptime(onderzoek["datum_vanaf"], "%Y-%m-%d")
    onderzoek_end_date = datetime.strptime(onderzoek["datum_tot"], "%Y-%m-%d")
    current_date = datetime.now()
    if not (onderzoek_start_date <= current_date <= onderzoek_end_date):
        return False
    
    return True


