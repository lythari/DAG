from django.db import models
from django.template.defaultfilters import slugify
from django.template.loader import get_template


class Navbar(models.Model):
    CHOICES = (
        ('VL', 'Vertical Left'),
        ('VR', 'Vertical Right'),
        ('H', 'Horizontal'),
    )
    state = models.BooleanField(default=False, verbose_name="Active")
    position = models.CharField(max_length=64, choices=CHOICES)

    template_name = 'navbar/navbar.html'

    def get_context_data(self):
        return {
            "nav_class":     self.position,
            "nav_links": self.link_set.all(),
        }

    def render(self):
        return get_template(self.template_name).render(context=self.get_context_data())

    class Meta:
        verbose_name = "Barre de navigation"


class Link(models.Model):

    bar = models.ForeignKey(Navbar, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=255, blank=True)
    position = models.IntegerField()

    template_name = 'navbar/link.html'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_context_data(self):
        return {
            "link_name": self.name,
            "link_href": self.slug,
        }

    def render(self):
        return get_template(self.template_name).render(context=self.get_context_data())

    class Meta:
        ordering = ['position']
        verbose_name = "Lien"
