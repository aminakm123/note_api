from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'notes_note'
        verbose_name = _('note')
        verbose_name_plural = _('notes')


    def __str__(self):
        return str(self.title)
