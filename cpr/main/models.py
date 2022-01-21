from django.db import models
from main.utils import transform_text

class Sector(models.Model):
    name = models.TextField()


class Policy(models.Model):
    # policy_id,policy_title,sectors,description_text
    title = models.TextField()
    sectors = models.ManyToManyField(to=Sector) # , on_delete=models.PROTECT)
    description_text = models.TextField()
    terms = models.TextField()

    def save(self, *args, **kwargs):
        words_only_text = transform_text(self.description_text)
        unique_words = ' '.join(sorted(set(words_only_text.split())))
        self.terms = unique_words
        super().save(*args, **kwargs)


