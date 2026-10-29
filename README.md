# Patient Record System (Digital Public Good)

A simple Python program that manages **anonymous patient records** for a clinic. Patients are assigned to doctors who have a daily patient limit. The whole program is in one file: `patient_record_system.py`.

**Author:** Alhaji Dauda Kamara

---

## 1. Purpose

Small clinics often lack affordable software to track who has been seen and which doctor is handling which patient. This program is a lightweight, free, open example of a Digital Public Good that:

- Stores patient records without any personal data
- Assigns patients to doctors without exceeding each doctor's limit
- Tracks whether a patient is *Waiting* or *Seen*

## 2. Privacy Design

No names, phone numbers, addresses or diagnoses are stored. A patient is identified only by an anonymous ID such as `P001`, plus age and a general reason for visit (e.g. "General check-up").

## 3. Requirements

- Python 3.6 or newer
- No external libraries

## 4. How to Run

```bash
python patient_record_system.py
```

The program runs a built-in demo (`main()`) and prints the results to the screen. No user input is needed.

## 5. Program Structure

| Part | Type | Description |
|---|---|---|
| `AGE_GROUPS` | Tuple (immutable) | Age limits and labels: Under 18, 18 to 59, 60 and above |
| `Doctor` | Class | Doctor ID, specialty, patient limit, number assigned |
| `Patient` | Class | Anonymous patient record with ID, age, reason, status, doctor |
| `add_patient()` | Function | Adds a patient to the dictionary (rejects duplicate IDs) |
| `display_patients()` | Function | Loops through the dictionary and prints every record |
| `find_patient()` | Function | Looks up a patient by ID, returns `None` if not found |
| `main()` | Function | Demo that runs every feature |

### Doctor methods

| Method | What it does |
|---|---|
| `has_space()` | True if the doctor can take another patient |
| `take_patient()` | Reserves one place, returns True if successful |
| `update_record()` | Changes specialty or patient limit |
| `display_info()` | Prints the doctor's details |

### Patient methods

| Method | Type | What it does |
|---|---|---|
| `assign_doctor(doctor)` | Instance | Links the patient to a doctor (if the doctor has space) |
| `mark_as_seen()` | Instance | Sets status to *Seen* (only after a doctor is assigned) |
| `update_record()` | Instance | Corrects age or reason for visit |
| `get_summary()` | Instance | Returns a tuple `(ID, age group, status)` |
| `display_info()` | Instance | Prints the patient's details |
| `from_string(text)` | Class method | Creates a patient from text like `P002,45,Antenatal visit` |
| `get_patients_created()` | Class method | Returns how many Patient objects were created |
| `is_valid_id(id)` | Static method | Checks the ID is `P` + 3 digits |
| `age_group(age)` | Static method | Returns the age group label |

## 6. Concepts Demonstrated

| Concept | Where it is used |
|---|---|
| Classes and objects | `Doctor` and `Patient` |
| Constructor (`__init__`) | Both classes |
| Class attribute | `Patient.patients_created` |
| Instance methods | `assign_doctor`, `mark_as_seen`, `update_record` |
| Class methods | `from_string`, `get_patients_created` |
| Static methods | `is_valid_id`, `age_group` |
| Object interaction | A `Patient` calls `Doctor.take_patient()` |
| Dictionary | `records` stores all patients by ID |
| Tuple | `AGE_GROUPS` and `get_summary()` |
| Loops | Displaying records, validation tests |
| Input validation | ID format and age range checks |
| Exception handling | `ValueError` raised and caught with `try/except` |

## 7. Validation Rules

- Patient ID must be the letter `P` followed by exactly 3 digits (e.g. `P001`)
- Age must be between 0 and 150
- A patient can only have one doctor
- A doctor cannot take more patients than their limit
- A patient cannot be marked as *Seen* without a doctor
- Duplicate patient IDs are not added

## 8. Demo Steps and Expected Output

The demo in `main()` runs 8 steps:

1. Create two doctors
2. Create patients (constructor, `from_string`, and a duplicate ID)
3. Test ID validation with a static method and catch an error
4. Assign patients to doctors (one doctor becomes full)
5. Update records and change status
6. Display all records
7. Show summary tuples and the number of objects created
8. Search for a record that does not exist

Sample output (key parts):

```
=== PATIENT RECORD SYSTEM ===

1. Creating doctors
Doctor D01 | General Medicine | patients 0/2
Doctor D02 | Child Health | patients 0/1

2. Creating patients
  Record P001 added.
  Record P002 added.
  Record P003 added.
  Record P004 added.
  Record P001 already exists. Not added.

3. Checking IDs with a static method
  P005 valid? True
  X12 valid? False
  P12A valid? False
  Error caught: Patient ID must look like P001 (letter P + 3 digits).

4. Assigning patients to doctors
  Doctor D01 is full. P004 was not assigned.
Doctor D01 | General Medicine | patients 2/2
Doctor D02 | Child Health | patients 1/1

5. Updating records
  P004 needs a doctor before being marked as seen.
Doctor D02 | Child Health | patients 1/3

6. All patient records
Patient P001 | age 34 (18 to 59) | General check-up | Seen | doctor: D01
Patient P002 | age 46 (18 to 59) | Antenatal visit | Waiting | doctor: D01
Patient P003 | age 7 (Under 18) | Child immunisation | Waiting | doctor: D02
Patient P004 | age 62 (60 and above) | Blood pressure check | Waiting | doctor: not assigned

7. Summary tuples (ID, age group, status)
  ('P001', '18 to 59', 'Seen')
  ('P002', '18 to 59', 'Waiting')
  ('P003', 'Under 18', 'Waiting')
  ('P004', '60 and above', 'Waiting')

Patient objects created (including the rejected duplicate): 5
Records stored: 4

8. Searching for a record
  P999 not found.
```

## 9. File List

```
patient_record_system.py   # complete program
README.md                  # this file
```
