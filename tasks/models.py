from django.db import models

class Task(models.Model):
    status_choices = ["მიმდინარეობს", "დასრულდა"]
    title = models.CharField(max_length=118, blank=False, null=False)
    description = models.TextField()
    deadline = models.DateField()
    status = status_choices
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title