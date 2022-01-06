class Student:
    fields = ["studentId", "firstName", "lastName", "department", "cycle", "semester"]
    types = [str, str, str, str, int, int]

    def __init__(self, stud):
        for s in stud:
            setattr(self, s, stud[s])
