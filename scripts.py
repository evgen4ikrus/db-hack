from datacenter.models import Mark, Chastisement, Commendation, Lesson, Schoolkid, Subject
from random import randint
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def checks_the_schoolkid(schoolkid):
    try:
        Schoolkid.objects.get(full_name__contains=schoolkid)
    except MultipleObjectsReturned:
        exit(f'Найдено несколько учеников с именем {schoolkid}')
    except ObjectDoesNotExist:
        exit(f'Ученик с именем {schoolkid} не найден')


def fix_marks(schoolkid):
    checks_the_schoolkid(schoolkid)
    bad_schoolkid_marks = Mark.objects.filter(schoolkid__full_name__contains=schoolkid, points__lte='4')  
    for mark in bad_schoolkid_marks:
        mark.points = randint(4, 5)
        mark.save()


def emove_chastisements(schoolkid):
    checks_the_schoolkid(schoolkid)
    chastisements = Chastisement.objects.filter(schoolkid__full_name__contains=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid, subject):
    checks_the_schoolkid(schoolkid)
    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid)
    random_commendation = Commendation.objects.all().order_by('?').first()
    subject = Subject.objects.get(title=subject, year_of_study=schoolkid.year_of_study)
    group_lesson = Lesson.objects.filter(subject__title__contains=subject.title,
                                           year_of_study=schoolkid.year_of_study,
                                           group_letter=schoolkid.group_letter
                                           ).order_by('-date').first()
    commendation = Commendation.objects.create(text=random_commendation.text,
                                               created=group_lesson.date,
                                               schoolkid=schoolkid,
                                               subject=subject,
                                               teacher=group_lesson.teacher)
    commendation.save()