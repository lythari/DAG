from django.db import models
from django.template.defaultfilters import slugify


class Navbar(models.Model):
    CHOICES = (
        ('VL', 'Vertical Left'),
        ('VR', 'Vertical Right'),
        ('H', 'Horizontal'),
    )
    state = models.BooleanField(default=False, verbose_name="Active")
    position = models.CharField(max_length=64, choices=CHOICES)

    class Meta:
        verbose_name = "Barre de navigation"


class Link(models.Model):

    bar = models.ForeignKey(Navbar, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=255, blank=True)
    position = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['position']
        verbose_name = "Lien"
