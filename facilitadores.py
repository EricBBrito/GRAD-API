

def print_students(students: list, search_id: str | None = None):
    x = []
    for i in range(len(students)):
        if search_id == None or students[i][0] == search_id:
            s_id = students[i][0]
            cpf = students[i][1]
            name = students[i][2]
            birthDate = students[i][3]
            number = students[i][4]
            expediter = students[i][5]
            uf = students[i][6]
            course = students[i][7]

            x.append(("ID: " + s_id, "Name: " + name, "Date of birth: " + str(birthDate),
                     "CPF: " + cpf, "RG: " + number + " " + expediter + "-" + uf, "Course: " + str(course)))
    return x


def print_professors(professors: list, search_id: str | None = None):
    x = []
    for i in range(len(professors)):
        if search_id == None or professors[i][0] == search_id:
            s_id = professors[i][0]
            cpf = professors[i][1]
            name = professors[i][2]
            title = professors[i][3]

            x.append(("ID: " + s_id, "CPF: " + cpf,
                     "Name: " + name, "Title: " + title))
    return x


def print_courses(courses: list, search_id: str | None = None):
    x = []
    for i in range(len(courses)):
        if search_id == None or courses[i][0] == search_id:
            s_id = courses[i][0]
            name = courses[i][1]
            date_of_creation = courses[i][2]
            bilding = courses[i][3]
            coordinator_id = courses[i][4]

            x.append(("ID: " + s_id, "Course: " + name, "Date of creation: " +
                     str(date_of_creation), "Bilding: " + bilding, "Coordinator ID: " + str(coordinator_id)))
    return x


def print_classes(classes: list, search_id: str | None = None):
    x = []
    for i in range(len(classes)):
        if search_id == None or classes[i][0] == search_id:
            s_id = classes[i][0]
            name = classes[i][1]
            code = classes[i][2]
            description = classes[i][3]
            professor_id = classes[i][4]

            x.append(("ID: " + s_id, "Class: " + name,
                     "Code: " + code, "Description: " + description, "Coordinator ID: " + str(professor_id)))
    return x
