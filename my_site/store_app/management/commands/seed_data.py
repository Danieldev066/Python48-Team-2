from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from store_app.models import (
    UserProfile, Category, Project, Tag, Task, Subtask, Comment
)


class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными (по 10 записей на модель)'

    def handle(self, *args, **options):
        # Пользователь-владелец
        user, _ = UserProfile.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com'}
        )
        user.set_password('admin')
        user.is_staff = True
        user.is_superuser = True
        user.save()

        # Категории
        category_names = [
            'Работа', 'Учёба', 'Дом', 'Здоровье', 'Финансы',
            'Покупки', 'Спорт', 'Хобби', 'Путешествия', 'Личное'
        ]
        categories = []
        for name in category_names:
            category, _ = Category.objects.get_or_create(category_name=name)
            categories.append(category)

        # Проекты
        project_data = [
            'Дипломная работа', 'Ремонт квартиры', 'Подготовка к экзаменам',
            'Личный бюджет', 'Спортивные тренировки', 'Изучение Django',
            'Планирование отпуска', 'Организация дня рождения',
            'Уборка гаража', 'Чтение книг'
        ]
        projects = []
        for i, name in enumerate(project_data):
            project, _ = Project.objects.get_or_create(
                project_name=name,
                defaults={
                    'description': f'Описание проекта «{name}»',
                    'category': categories[i],
                    'owner': user,
                }
            )
            projects.append(project)

        # Теги
        tag_names = [
            'срочно', 'важно', 'на потом', 'быстро', 'сложно',
            'легко', 'встреча', 'звонок', 'документы', 'идея'
        ]
        tags = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(tag_name=name)
            tags.append(tag)

        # Задачи
        task_titles = [
            'Купить продукты на неделю',
            'Позвонить клиенту по контракту',
            'Написать введение к диплому',
            'Оплатить коммунальные услуги',
            'Записаться к врачу',
            'Сходить на тренировку',
            'Подготовить презентацию для встречи',
            'Забронировать отель для отпуска',
            'Разобрать вещи в шкафу',
            'Прочитать главу учебника по Django',
        ]
        priorities = ['low', 'medium', 'high']
        tasks = []
        for i, title in enumerate(task_titles):
            task, _ = Task.objects.get_or_create(
                title=title,
                defaults={
                    'description': f'Подробности: {title.lower()}',
                    'priority': priorities[i % 3],
                    'deadline': timezone.now() + timedelta(days=i + 1),
                    'project': projects[i],
                    'assignee': user,
                }
            )
            task.tags.add(tags[i])
            tasks.append(task)

        # Подзадачи
        subtask_titles = [
            'Составить список покупок',
            'Найти номер клиента',
            'Собрать источники для введения',
            'Проверить квитанции',
            'Выбрать удобное время записи',
            'Собрать спортивную сумку',
            'Сделать слайды',
            'Сравнить цены на отели',
            'Отсортировать вещи по сезонам',
            'Сделать конспект главы',
        ]
        for i, title in enumerate(subtask_titles):
            Subtask.objects.get_or_create(
                task=tasks[i],
                title=title,
                defaults={'completed': i % 2 == 0}
            )

        # Комментарии
        comment_texts = [
            'Не забыть про молоко и хлеб',
            'Клиент просил перезвонить после обеда',
            'Нужно добавить статистику за 2025 год',
            'Счёт за интернет ещё не пришёл',
            'Врач принимает только по вторникам',
            'После тренировки взять протеин',
            'Добавить графики в презентацию',
            'Уточнить у второго участника даты',
            'Часть вещей отдать на благотворительность',
            'Особое внимание главе про сериализаторы',
        ]
        for i, text in enumerate(comment_texts):
            Comment.objects.get_or_create(
                task=tasks[i],
                user=user,
                text=text
            )

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!'))