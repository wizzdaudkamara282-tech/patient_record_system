"""Patient Record System (a Digital Public Good) - complete program in one file.

Run with:  python patient_record_system.py


Privacy note: no names, phone numbers, addresses or diagnoses are stored.
Patients are identified only by an anonymous ID code such as P001.
"""

# Tuple (immutable): (highest age in the group, label). Used by Patient.age_group().
AGE_GROUPS = ((17, "Under 18"), (59, "18 to 59"), (150, "60 and above"))


class Doctor:
    """A doctor (or clinic staff member) who can see a limited number of patients."""

    def __init__(self, doctor_id, specialty, max_patients):
        self.doctor_id = doctor_id
        self.specialty = specialty
        self.max_patients = max_patients
        self.patients_assigned = 0

    def has_space(self):
        """Return True if the doctor can still take another patient."""
        return self.patients_assigned < self.max_patients

    def take_patient(self):
        """Reserve one place for a patient. Return True if it worked."""
        if self.has_space():
            self.patients_assigned += 1
            return True
        return False

    def update_record(self, specialty=None, max_patients=None):
        """Change the doctor's specialty or daily patient limit."""
        if specialty is not None:
            self.specialty = specialty
        if max_patients is not None:
            self.max_patients = max_patients

    def display_info(self):
        print(f"Doctor {self.doctor_id} | {self.specialty} | "
              f"patients {self.patients_assigned}/{self.max_patients}")


class Patient:
    """An anonymous patient record."""

    patients_created = 0  # class attribute shared by every Patient object

    def __init__(self, patient_id, age, reason):
        if not Patient.is_valid_id(patient_id):
            raise ValueError("Patient ID must look like P001 (letter P + 3 digits).")
        if not 0 <= age <= 150:
            raise ValueError("Age must be between 0 and 150.")
        self.patient_id = patient_id
        self.age = age
        self.reason = reason          # general reason for visit, e.g. "General check-up"
        self.status = "Waiting"       # Waiting -> Seen
        self.doctor_id = None
        Patient.patients_created += 1

    # ---------- instance methods ----------
    def assign_doctor(self, doctor):
        """Link this patient to a doctor (interaction between two objects)."""
        if self.doctor_id is not None:
            print(f"  {self.patient_id} already has doctor {self.doctor_id}.")
            return False
        if doctor.take_patient():
            self.doctor_id = doctor.doctor_id
            return True
        print(f"  Doctor {doctor.doctor_id} is full. {self.patient_id} was not assigned.")
        return False

    def mark_as_seen(self):
        """Change the status to Seen (only possible after a doctor is assigned)."""
        if self.doctor_id is None:
            print(f"  {self.patient_id} needs a doctor before being marked as seen.")
            return False
        self.status = "Seen"
        return True

    def update_record(self, age=None, reason=None):
        """Correct the age or the reason for visit."""
        if age is not None:
            if not 0 <= age <= 150:
                raise ValueError("Age must be between 0 and 150.")
            self.age = age
        if reason is not None:
            self.reason = reason

    def get_summary(self):
        """Return a tuple with the key facts: (ID, age group, status)."""
        return (self.patient_id, Patient.age_group(self.age), self.status)

    def display_info(self):
        doctor = self.doctor_id if self.doctor_id else "not assigned"
        group = Patient.age_group(self.age)
        print(f"Patient {self.patient_id} | age {self.age} ({group}) | "
              f"{self.reason} | {self.status} | doctor: {doctor}")

    # ---------- class methods ----------
    @classmethod
    def from_string(cls, text):
        """Create a Patient from text such as 'P002,45,Antenatal visit'."""
        parts = [part.strip() for part in text.split(",")]
        if len(parts) != 3:
            raise ValueError("Use the format: ID,age,reason")
        return cls(parts[0], int(parts[1]), parts[2])

    @classmethod
    def get_patients_created(cls):
        """Return how many Patient objects have been created."""
        return cls.patients_created

    # ---------- static methods ----------
    @staticmethod
    def is_valid_id(patient_id):
        """Check that an ID is the letter P followed by exactly 3 digits."""
        return len(patient_id) == 4 and patient_id[0] == "P" and patient_id[1:].isdigit()

    @staticmethod
    def age_group(age):
        """Return the age group label for an age, using the AGE_GROUPS tuple."""
        for highest_age, label in AGE_GROUPS:
            if age <= highest_age:
                return label
        return "Unknown"


# ===================== RECORD FUNCTIONS =====================
# All patients are stored in ONE data structure: a dictionary
# where the key is the patient ID and the value is the Patient object.


def add_patient(records, patient):
    """Add a Patient object to the dictionary. Return True if it was added."""
    if patient.patient_id in records:
        print(f"  Record {patient.patient_id} already exists. Not added.")
        return False
    records[patient.patient_id] = patient
    print(f"  Record {patient.patient_id} added.")
    return True


def display_patients(records):
    """Loop through the dictionary and display every record."""
    if not records:
        print("  No patient records yet.")
        return
    for patient in records.values():
        patient.display_info()


def find_patient(records, patient_id):
    """Return the Patient with this ID, or None if it does not exist."""
    return records.get(patient_id)


# ===================== DEMO PROGRAM =====================


def main():
    print("=== PATIENT RECORD SYSTEM ===")

    # 1. Create Doctor objects
    print("\n1. Creating doctors")
    doctor_a = Doctor("D01", "General Medicine", 2)
    doctor_b = Doctor("D02", "Child Health", 1)
    doctor_a.display_info()
    doctor_b.display_info()

    # 2. Create Patient objects (constructor and class method)
    print("\n2. Creating patients")
    records = {}  # the one data structure: a dictionary of Patient objects
    add_patient(records, Patient("P001", 34, "General check-up"))
    add_patient(records, Patient.from_string("P002,45,Antenatal visit"))
    add_patient(records, Patient("P003", 7, "Child immunisation"))
    add_patient(records, Patient("P004", 62, "Blood pressure check"))
    add_patient(records, Patient("P001", 20, "Duplicate ID test"))

    # 3. Validation with a static method
    print("\n3. Checking IDs with a static method")
    for test_id in ("P005", "X12", "P12A"):
        print(f"  {test_id} valid? {Patient.is_valid_id(test_id)}")
    try:
        Patient("BAD1", 30, "Test")
    except ValueError as error:
        print(f"  Error caught: {error}")

    # 4. Objects interacting: patients are assigned to doctors
    print("\n4. Assigning patients to doctors")
    find_patient(records, "P001").assign_doctor(doctor_a)
    find_patient(records, "P002").assign_doctor(doctor_a)
    find_patient(records, "P004").assign_doctor(doctor_a)   # doctor_a is full
    find_patient(records, "P003").assign_doctor(doctor_b)
    doctor_a.display_info()
    doctor_b.display_info()

    # 5. Update records and change status
    print("\n5. Updating records")
    find_patient(records, "P001").mark_as_seen()
    find_patient(records, "P004").mark_as_seen()            # no doctor yet
    find_patient(records, "P002").update_record(age=46)
    doctor_b.update_record(max_patients=3)
    doctor_b.display_info()

    # 6. Display all records
    print("\n6. All patient records")
    display_patients(records)

    # 7. Tuple summaries and class method
    print("\n7. Summary tuples (ID, age group, status)")
    for patient in records.values():
        print(" ", patient.get_summary())
    created = Patient.get_patients_created()
    print(f"\nPatient objects created (including the rejected duplicate): {created}")
    print(f"Records stored: {len(records)}")

    # 8. Searching for a missing record
    print("\n8. Searching for a record")
    result = find_patient(records, "P999")
    print("  P999 found." if result else "  P999 not found.")


if __name__ == "__main__":
    main()
