from django.db import models
from django.utils.text import slugify

# Create your models here.

class Collection(models.Model):
    """Collection avec nom et un slug """
    name = models.fields.CharField(max_length=60)
    slug = models.fields.SlugField(blank=True)

    @classmethod
    def get_defaut_collection(cls):
        collection, created = Collection.objects.get_or_create(name="Default", slug="_defaut")
        return collection
    
    # def save(self, *args, **kwargs):
    #     self.slug = self.slug or slugify(self.name)
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    """ Task => description et collection  """
    description = models.fields.CharField(max_length=300)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.description
