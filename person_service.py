import person_repository
import IBasicPersonDTO


def set_person_data(person, conn, cur):
    # for inserting person to database
    person_repository.insert_person_values(person[0], person[1], person[2], conn, cur)
    return "Added New Person"


def delete_person_data(id, conn, cur):
    # for deleting a person based on id
    person_repository.delete_persons(id, conn, cur)
    return "Deleted New Person"


def get_all_person_data(cur):
    # for getting all person data
    persons = person_repository.get_all_person_data(cur)
    list_basic_persons = list(map(create_basic_person_dto, persons))
    return list_basic_persons


def get_person_by_ids(id, cur):
    # for getting data relevant by id
    persons = person_repository.get_person_by_ids(id, cur)
    list_basic_persons = list(map(create_basic_person_dto, persons))
    return list_basic_persons


def create_basic_person_dto(person):
    # for creating a basic person dto
    basic_person = IBasicPersonDTO.IBasicPersonDTO(
        person[0], person[1], person[2], person[3]
    )
    return basic_person
