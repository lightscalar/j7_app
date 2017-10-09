from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.recycleview import RecycleView
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.properties import ObjectProperty, ListProperty
from sixer import *
from solid_db import SolidDB
from time import sleep


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
    patients = ListProperty([])
    scan = ObjectProperty(None)
    scans = ListProperty([])
    scan_status = StringProperty('')

    def create_patient(self):
        # Create a new patient. Set as current patient
        print('Creating a patient.')
        patient = {'hid': sixer()}
        patient['description'] = ''
        patient['gender'] = 'Male'
        self.patient = db.insert('patient', patient)
        self.root.home.patients.refresh()
        self.patient_hid = self.patient['hid']
        self.patients = db.all('patients')
        self.scans = db.find_where('scans', 'patient_id', self.patient['_id'])
        self.root.patient.scans.patient_id = self.patient['_id']
        self.root.patient.scans.refresh()
        self.root.current = 'patient_screen'

    def delete_patient(self, patient_id):
        # Delete a patient.
        db.delete(patient_id)
        self.root.home.patients.refresh()
        self.patients = db.all('patients')

    def delete_scan(self, scan_id):
        # Delete a patient.
        db.delete(scan_id)
        self.root.patient.scans.refresh()
        self.scans = db.find_where('scans', 'patient_id', self.patient['_id'])

    def create_scan(self):
        # Create a new scan.
        patient_id = self.patient['_id']
        scan = {'patient_id': patient_id, 'gcs': '15', 'notes': ''}
        self.scan = db.insert('scan', scan)
        self.root.current='scan_screen'
        self.root.patient.scans.refresh()
        self.patients = db.all('patients')
        self.scans = db.find_where('scans', 'patient_id', self.patient['_id'])

    def update_scan(self, package):
        # Update the scan with notes/gcs.
        db.update(package, self.scan['_id'])

    def update_patient(self, package):
        # Update the scan with notes/gcs.
        db.update(package, self.patient['_id'])

    def set_patient(self, patient_id):
        # Set current patient.
        self.patient = db.find_by_id(patient_id)
        self.patient_hid = self.patient['hid']
        self.root.current = 'patient_screen'
        self.root.patient.scans.patient_id = self.patient['_id']
        self.root.patient.scans.refresh()
        self.scans = db.find_where('scans', 'patient_id', self.patient['_id'])

    def schedule_scan(self):
        # Schedule the scan.
        self.scan_status = 'Hold Steady'
        Clock.schedule_once(self.start_scan)

    def start_scan(self, dt):
        # Perform an eye scan!
        sleep(2)
        self.root.current = 'home_screen'

    def build(self):
        # Build the application.
        self.patients = db.all('patients')
        print(self.root)


if __name__ == '__main__':
    JohnnySevenApp().run()

