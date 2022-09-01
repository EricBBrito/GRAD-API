from pydantic import BaseModel, Field
from .generic import GenericModel
from uuid import UUID
from datetime import date
from typing import List


class IdentityCard(GenericModel):
    number: str = Field(title='Number of identity card')
    expediter: str = Field(title='Expediter of identity card')
    uf: str = Field(title='State of expediter', min_length=2, max_length=2)

    class Config:
        schema_extra = {
            "example": {
                "number": "00000000-0",
                "expediter": "SSP",
                "uf":  "AL"
            }
        }


class StudentData(GenericModel):
    name: str = Field(title='Name of student')
    birth_date: date | None = Field(
        default=None, title='Birth date of student')
    cpf: str = Field(title="CPF of student",
                     regex='[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}')
    rg: IdentityCard | None = Field(title='Identity card info of student')

    class Config:
        schema_extra = {
            "example": {
                "name": "Jane Smith",
                "birth_date": "2021-12-31",
                "cpf":  "000.000.000-00",
                "rg": {
                    "number": "00000000-0",
                    "expediter": "SSP",
                    "uf":  "AL"
                },
                "course_id": "UUID"
            }
        }


class Course(GenericModel):
    name: str = Field(title='Name of the course')
    creation_date: date = Field(title='Date of creation')
    bilding: str = Field(title='Bilding of the course')
    coodinator_id: UUID = Field(
        "ID of the professor coordinating this course")

    class config:
        schema_extra = {
            "example": {
                "name": "Civil Engineering",
                "creation_date": "yyyy-mm-dd",
                "bilding": "CTEC",
                "coordinator_id": "UUID"
            }
        }


class Class(GenericModel):
    name: str = Field(title="Name of the class")
    code: str = Field(title="Code of the class")
    description: str = Field(title="Description of the class")
    professor_id: str = Field("ID of the professor who teaches this class")

    class config:
        schema_extra = {
            "example": {
                "name": "Engineering Introduction",
                "code": "E101",
                "description": "In this class you'll learn things that you'll never use in your life",
                "professor_ID": "UUID"
            }
        }


class Student(StudentData):
    id: UUID = Field(title='ID of student')
    course: UUID | None = Field(title='ID of the course of the student')
    classes: list[UUID] | None = Field(
        title='IDs of the classes of the student')


class Professor(GenericModel):
    cpf: str = Field(title="CPF of professor",
                     regex='[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}')
    name: str = Field(title="Name of professor")
    title: str = Field(title="Title of professor")

    class Config:
        schema_extra = {
            "example": {
                "cpf": "000.000.000-00",
                "name": "Roberaldo",
                "title": "Doctor"
            }
        }


class SetStudentCourse(GenericModel):
    student_id: UUID = Field(title="ID of student")
    new_course_id: UUID = Field(title="ID of the student's new course")

    class Config:
        schema_extra = {
            "example": {
                "student_id": "UUID",
                "new_course_id": "UUID"
            }
        }


class SetCourseCoordinator(GenericModel):
    professor_id: UUID = Field(title="ID of course's new coordinator")
    course_id: UUID = Field(title="ID of the course")

    class Config:
        schema_extra = {
            "example": {
                "professor_id": "UUID",
                "course_id": "UUID"
            }
        }


class SetTeacherClass(GenericModel):
    professor_id: UUID = Field(title="ID of course's new coordinator")
    class_id: UUID = Field(title="ID of the course")

    class Config:
        schema_extra = {
            "example": {
                "professor_id": "UUID",
                "class_id": "UUID"
            }
        }


class StudentClass(GenericModel):
    student_id: UUID = Field(title="ID of student")
    class_id: UUID = Field(title="ID of the class")

    class Config:
        schema_exta = {
            "example": {
                "student_id": "UUID",
                "class_id": "UUID"
            }
        }


class StudentList(BaseModel):
    __root__: List[Student]

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "title": 'List of students'
        }
