from Models import UserStore, Patient_test, Patient_Medicine, Patient_details, Diagnosis, Medicine
from Config import db

def create_p(details):
    db.session.add(Patient_details(details))
    db.session.commit()
    return True