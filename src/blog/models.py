from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=36)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Catégorie"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    # relation many2one : +ieurs article pour 1 seul auteur (ici le super user)
    # si CASCADE =>supprime l'auteur si on supprime l'article
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    slug = models.SlugField(blank=True)

    published = models.BooleanField(default=False)
    date = models.DateField(blank=True, null=True)
    content = models.TextField()
    description = models.TextField()

    class Meta:
        verbose_name = "Article"

    def __str__(self):
        return self.title

    def number_of_words(self):
        return len(self.content.split())

    def get_absolute_url(self):
        return reverse("blog-post", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # on surcharge la méthode save de base, car on va effectuer une vérif sur le slug avant d'effectuer la sauvegarde en BDD
        if not self.slug:  # permet de déterminer automatiquement un slug si on n'en a pas spécifié
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
