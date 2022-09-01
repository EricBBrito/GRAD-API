from fastapi import FastAPI, HTTPException
import uvicorn
from uuid import UUID, uuid4
from schemas.gradmodels import StudentData, SetStudentCourse, Professor, Class, Course, StudentClass, SetCourseCoordinator, SetTeacherClass
import sqlite3
import facilitadores

connection = sqlite3.connect("grad.db")
client = connection.cursor()
tupl1 = client.execute("SELECT * FROM alunos;").fetchall()
students = [list(row) for row in tupl1]
tupl2 = client.execute("SELECT * FROM cursos;").fetchall()
courses = [list(row) for row in tupl2]
tupl3 = client.execute("SELECT * FROM disciplinas;").fetchall()
classes = [list(row) for row in tupl3]
professors = client.execute("SELECT * FROM professores;").fetchall()
students_classes = client.execute(
    "SELECT * FROM alunos_disciplinas;").fetchall()
connection.close()

app = FastAPI(title="PROGRAD API")


# Students


@app.get(   # Buscar todos os estudantes
    '/students',
    summary='Fetch all students data',
    tags=['Students'],
)
def get_students():
    return facilitadores.print_students(students)


@app.get(   # Buscar um estudante específico
    '/students/{student_id}',
    summary='Fetch student data',
    tags=['Students'],
)
def get_student(student_id: str):
    f = facilitadores.print_students(students, student_id)
    if f is None:
        raise HTTPException(
            status_code=404, detail=f'Student with id={student_id} not found')
    return f


@app.post(   # Adicionar um novo estudante
    '/students',
    summary='Add a new student',
    tags=['Students'],
    status_code=201,
)
def add_student(student_data: StudentData):
    student_id: UUID = uuid4()

    connection = sqlite3.connect("grad.db")
    client = connection.cursor()
    client.execute(
        f'INSERT INTO alunos values("{student_id}", "{student_data.cpf}", "{student_data.name}",\
            "{student_data.birth_date}", "{student_data.rg.number}", "{student_data.rg.expediter}",\
                "{student_data.rg.uf}", "Null");')
    connection.commit()
    connection.close()

    students.append([str(student_id), student_data.cpf, student_data.name, student_data.birth_date,
                     student_data.rg.number, student_data.rg.expediter, student_data.rg.uf, "Null"])

    return get_student(student_id=str(student_id))


@app.put(   # Alterar o curso de um estudante
    '/students/{students_id}/course/{course_id}',
    summary='Set or change a students course',
    tags=['Students'],
    status_code=201
)
def set_student_course(set_data: SetStudentCourse):
    for i in range(len(students)):
        if UUID(students[i][0]) == set_data.student_id:
            students[i][7] = set_data.new_course_id

            connection = sqlite3.connect("grad.db")
            client = connection.cursor()
            client.execute(
                f'UPDATE alunos SET curso_id="{set_data.new_course_id}" WHERE id="{set_data.student_id}";')
            connection.commit()
            connection.close()
    return get_student(student_id=str(set_data.student_id))


@app.post(  # Matriculando um aluno numa matéria
    '/students/{students_id}/class/{class_id}',
    summary='Enroll student in a class',
    tags=['Students'],
    status_code=201
)
def enroll_student_class(enroll_data: StudentClass):
    connection = sqlite3.connect("grad.db")
    client = connection.cursor()
    client.execute(
        f'INSERT INTO alunos_disciplinas values("{enroll_data.student_id}", "{enroll_data.class_id}");')
    connection.commit()
    connection.close()

    students_classes.append([enroll_data.student_id, enroll_data.class_id])

    return get_student(student_id=str(enroll_data.student_id)), get_class(class_id=str(enroll_data.class_id))


@app.delete(   # Removendo uma materia de um estudante
    '/students/{students_id}/class/{class_id}',
    summary='Remove student from a class',
    tags=['Students'],
    status_code=201
)
def remove_student_class(remove_data: StudentClass):
    connection = sqlite3.connect("grad.db")
    client = connection.cursor()
    client.execute(
        f'DELETE FROM alunos_disciplinas WHERE aluno_id="{remove_data.student_id}" AND disciplina_id="{remove_data.class_id}";')
    connection.commit()
    connection.close()

    for i in range(len(students_classes)):
        if students_classes[i][0] == remove_data.student_id:
            if students_classes[i][1] == remove_data.class_id:
                students_classes[i][0] = None
                students_classes[i][1] = None
    return get_student(student_id=str(remove_data.student_id)), get_class(class_id=str(remove_data.class_id))


# Professors


@app.get(   # Buscar todos os professores
    '/professors',
    summary='Fetch all professors data',
    tags=['Professors'],
)
def get_professors():
    return facilitadores.print_professors(professors)


@app.get(   # Buscar um professor específico
    '/professors/{professor_id}',
    summary='Fetch professor data',
    tags=['Professors'],
)
def get_professor(professor_id: str):
    f = facilitadores.print_professors(professors, professor_id)
    if f is None:
        raise HTTPException(
            status_code=404, detail=f'Professor with id={professor_id} not found')
    return f


@app.post(   # Adicionar um novo professor
    '/professors',
    summary='Add a new professor',
    tags=['Professors'],
    status_code=201,
)
def add_professor(professor_data: Professor):
    professor_id: UUID = uuid4()

    connection = sqlite3.connect("grad.db")
    client = connection.cursor()
    client.execute(
        f'INSERT INTO professores values("{professor_id}", "{professor_data.cpf}", "{professor_data.name}",\
            "{professor_data.title}");')
    connection.commit()
    connection.close()

    professors.append([str(professor_id), professor_data.cpf,
                      professor_data.name, professor_data.title])

    return get_professor(professor_id=str(professor_id))


# Courses


@app.get(   # Buscar todos os cursos
    '/courses',
    summary='Fetch all courses data',
    tags=['Courses'],
)
def get_courses():
    return facilitadores.print_courses(courses)


@app.get(   # Buscar um curso específico
    '/courses/{course_id}',
    summary='Fetch course data',
    tags=['Courses'],
)
def get_course(course_id: str):
    f = facilitadores.print_courses(courses, course_id)
    if f is None:
        raise HTTPException(
            status_code=404, detail=f'Course with id={course_id} not found')
    return f


@app.post(   # Adicionar um novo curso
    '/courses',
    summary='Add a new course',
    tags=['Courses'],
    status_code=201,
)
def add_course(course_data: Course):
    course_id: UUID = uuid4()

    connection = sqlite3.connect("grad.db")
    client = connection.cursor()
    client.execute(
        f'INSERT INTO cursos values("{course_id}", "{course_data.name}", "{course_data.creation_date}",\
            "{course_data.bilding}", "{course_data.coodinator_id}");')
    connection.commit()
    connection.close()

    courses.append([str(course_id), course_data.name, course_data.creation_date,
                   course_data.bilding, course_data.coodinator_id])

    return get_course(course_id=str(course_id))


@app.get(   # Buscar alunos de um curso específico
    '/courses/{course_id}/students',
    summary='Fetch students of course',
    tags=['Courses'],
)
def get_students_course(course_id: str):
    x = []
    for i in range(len(students)):
        if students[i][7] == course_id:
            x.append(get_student(student_id=students[i][0]))
    return x


@app.put(   # Alterar o coordenador de um curso
    '/courses/{course_id}/coordinator/{professor_id}',
    summary='Set or change a professor as the course coordinator',
    tags=['Courses'],
    status_code=201
)
def set_course_coordinator(set_data: SetCourseCoordinator):
    for i in range(len(courses)):
        if UUID(courses[i][0]) == set_data.course_id:
            courses[i][4] = set_data.professor_id

            connection = sqlite3.connect("grad.db")
            client = connection.cursor()
            client.execute(
                f'UPDATE cursos SET coordenador="{set_data.professor_id}" WHERE id="{set_data.course_id}";')
            connection.commit()
            connection.close()
    return get_course(course_id=str(set_data.course_id))


# Classes


@app.get(   # Buscar todas as disciplinas
    '/classes',
    summary='Fetch all classes data',
    tags=['Classes'],
)
def get_classes():
    return facilitadores.print_classes(classes)


@app.get(   # Buscar uma disciplina específica
    '/classes/{class_id}',
    summary='Fetch a class data',
    tags=['Classes'],
)
def get_class(class_id: str):
    f = facilitadores.print_classes(classes, class_id)
    if f is None:
        raise HTTPException(
            status_code=404, detail=f'Class with id={class_id} not found')
    return f


@app.post(   # Adicionar uma nova disciplina
    '/classes',
    summary='Add a new class',
    tags=['Classes'],
    status_code=201,
)
def add_class(class_data: Class):
    class_id: UUID = uuid4()

    connection = sqlite3.connect("grad.db")
    client = connection.cursor()
    client.execute(
        f'INSERT INTO disciplinas values("{class_id}", "{class_data.name}", "{class_data.code}",\
            "{class_data.description}", "{class_data.professor_id}");')
    connection.commit()
    connection.close()

    classes.append([str(class_id), class_data.name, class_data.code,
                   class_data.description, class_data.professor_id])

    return get_class(class_id=str(class_id))


@app.get(   # Buscar os alunos de uma disciplina
    '/classes/{class_id}/students',
    summary='Fetch students of a class',
    tags=['Classes'],
)
def get_students_class(class_id: str):
    x = []
    for i in range(len(students_classes)):
        if students_classes[i][1] == class_id:
            x.append(students_classes[i][0])
    f = get_class(class_id=class_id)
    for n in range(len(x)):
        f.append(get_student(student_id=x[n]))
    return f


@app.put(   # Alterar o professor de uma disciplina
    '/classes/{classes_id}/teacher/{professor_id}',
    summary='Set or change a professor as the teacher of a class',
    tags=['Classes'],
    status_code=201
)
def set_teacher_class(set_data: SetTeacherClass):
    for i in range(len(classes)):
        if UUID(classes[i][0]) == set_data.class_id:
            classes[i][4] = set_data.professor_id

            connection = sqlite3.connect("grad.db")
            client = connection.cursor()
            client.execute(
                f'UPDATE disciplinas SET professor_id="{set_data.professor_id}" WHERE id="{set_data.class_id}";')
            connection.commit()
            connection.close()
    return get_class(class_id=str(set_data.class_id))


@app.get(   # Rankear as disciplinas de acordo com a quantidade de alunos
    '/classes/ranking',
    summary='Get a ranking of classes by the number of their enrolled students',
    tags=['Classes'],
    status_code=201
)
def set_classes_ranking():
    x = []
    for i in range(len(classes)):
        class_name = classes[i][1]
        count = 0
        for n in range(len(students_classes)):
            print("entrou")
            if students_classes[n][1] == classes[i][0]:
                print("entrou")
                count += 1
        x.append((class_name, count))
    f = sorted(x, key=lambda y: y[1], reverse=True)
    return f


if __name__ == '__main__':
    uvicorn.run(app='grad:app', port=3000, reload=True)
