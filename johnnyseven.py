from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.recycleview import RecycleView
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.properties import ObjectProperty
from sixer import *
from solid_db import SolidDB


db = SolidDB('data/db.json')


class PatientList(RecycleView):

    def __init__(self, **kwargs):
        super(PatientList, self).__init__(**kwargs)
        self.refresh()

    def refresh(self):
        data = db.all('patients')
        data = sorted(data, key=lambda x: x['createdAt'], reverse=True)
        self.data = data


class ScanList(RecycleView):

    patient_id = StringProperty('')

    def __init__(self, **kwargs):
        super(ScanList, self).__init__(**kwargs)
        self.refresh()

    def refresh(self):
        data = db.find_where('scans', 'patient_id', self.patient_id)
        data = sorted(data, key=lambda x: x['createdAt'], reverse=True)
        self.data = data


class JohnnySevenApp(App):

    patient_hid = StringProperty('NO ACTIVE PATIENT')
    patient_id = StringProperty('patient_id')
    patient = ObjectProperty(None)

    def create_patient(self):
        # Create a new patient. Set as current patient
        print('Creating a patient.')
        patient = {'hid': sixer()}
        patient['description'] = ''
        patient['gender'] = 'Male'
        self.patient = db.insert('patient', patient)
        self.root.home.patients.refresh()
        self.patient_hid = self.patient['hid']

    def delete_patient(self, patient_id):
        # Delete a patient.
        db.delete(patient_id)
        self.root.home.patients.refresh()

    def set_patient(self, patient_id):
        # Set current patient.
        self.patient = db.find_by_id(patient_id)
        self.patient_hid = self.patient['hid']
        self.root.current = 'patient_screen'

    def build(self):
        # Build the application.
        print(self.root)


if __name__ == '__main__':
    JohnnySevenApp().run()

