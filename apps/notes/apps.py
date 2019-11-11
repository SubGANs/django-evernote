from django.apps import AppConfig


class NotesConfig(AppConfig):
    name = 'notes'
    verbose_name = 'Заметки'

    def ready(self):
        import notes.signals
