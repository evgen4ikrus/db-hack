from random import randint

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid, Subject)
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


def get_schoolkid_by_name(name):
    try:
        target_schoolkid = Schoolkid.objects.get(full_name__contains=name)
        return target_schoolkid

    except MultipleObjectsReturned:
        exit(f'Найдено несколько учеников с именем {name}')
    except ObjectDoesNotExist:
        exit(f'Ученик с именем {name} не найден')


def get_school_subject(subject, schoolkid):
    try:
        school_subject = Subject.objects.get(
            title=subject,
            year_of_study=schoolkid.year_of_study
            )

        return school_subject
    except ObjectDoesNotExist:
        exit('Такого школьного предмета нет, проверьте написание')


def fix_marks(name):
    schoolkid = get_schoolkid_by_name(name)
    bad_schoolkid_marks = Mark.objects.filter(
        schoolkid__full_name__contains=schoolkid.full_name,
        points__lte='3'
        )

    for mark in bad_schoolkid_marks:
        mark.points = randint(4, 5)
        mark.save()


def emove_chastisements(name):
    schoolkid = get_schoolkid_by_name(name)
    chastisements = Chastisement.objects.filter(
        schoolkid__full_name__contains=schoolkid.full_name
        )

    chastisements.delete()


def create_commendation(name, subject):
    schoolkid = get_schoolkid_by_name(name)
    random_commendation = Commendation.objects.all().order_by('?').first()
    school_subject = get_school_subject(subject, schoolkid)

    group_lesson = Lesson.objects.filter(
        subject__title__contains=school_subject.title,
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter
        ).order_by('?').first()

    commendation = Commendation.objects.create(
        text=random_commendation.text,
        created=group_lesson.date,
        schoolkid=schoolkid,
        subject=school_subject,
        teacher=group_lesson.teacher
        )

    commendation.save()
