from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from blog.forms import BlogPostForm, ConfirmDeleteForm

from blog.models import BlogPost


# Vue d'accueil du blog
class HomeView(View):
    def get(self, request):
        return HttpResponse("Accueil du site<br><a href='/blog/'>Le Blog<a/>")


# classe pour afficher tous les enregistrements en BDD du modèle BlogPost
class BlogIndexView(ListView):
    model = BlogPost
    template_name = "blog/index.html"
    context_object_name = "articles"  # on change le nom par défaut (object_list ou blogpost) par un nom de notre choix


# classe pour afficher le détail d'un enregistrement du modèle BlogPost
# même si cela n'apparait pas ici le slug est récupéré automatiquement via l'url pour être utilisé par cette vue
class PostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/post.html"
    context_object_name = "post"  # on change le nom par défaut (object) par un nom de notre choix


class PostCreateView(CreateView):
    # model = BlogPost
    template_name = "blog/create_or_update_post.html"
    # ici on spécifie quels champs du modèle BlogPost défini ci-dessus l'on veut utiliser avec 'Fields'
    # fields = ['title', 'slug', 'content', "published"]
    # si on souhaite utiliser un formulaire que l'on a défini plutôt que des champs on utilise l'attribut "form_class" qui nous permet
    # d'accéder à la classe du formulaire que l'on souhaite utiliser → on n'a donc plus besoin de l'attribut model = BlogPost
    form_class = BlogPostForm

    # en cas de validation du formulaire (d'où le terme 'success'), get_success_url() va nous rediriger vers
    # une autre url que celle prévue par défaut par la classe CreateView (= url de l'article créé)
    # on peut se passer de cette fonction en définissant un attribut success_url = reverse_lazy("blog-index")
    def get_success_url(self):
        return reverse("blog-index")

    def form_valid(self, form):  # form nous permet de récupérer le formulaire envoyé AUTOMATIQUEMENT par la classe
        # on effectue nos modifications sur notre formulaire VIA SON INSTANCE
        if self.request.user.is_authenticated:
            print(self.request.user)
            form.instance.author = self.request.user  # instance nous permet de récupérer l'instance associée à ce formulaire
        form.instance.published = False
        return super().form_valid(form)  # on retourne notre formulaire modifié à la méthode form_valid() de la classe super (CreateView)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submit_text"] = "Créer"
        return context


class PostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blog/delete_post.html"
    context_object_name = "post"
    success_url = reverse_lazy("blog-index")

    # On va personnaliser notre vue pour utiliser le formulaire de confirmation de suppression.
    # On surcharge la méthode get_context_data pour passer ce formulaire au template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confirm_form'] = ConfirmDeleteForm()
        return context

    # On doit s'assurer que la case a été cochée avant de supprimer l'article
    def post(self, request, *args, **kwargs):
        # On passe les données envoyées dans la requête au formulaire ConfirmDeleteForm
        confirm_form = ConfirmDeleteForm(request.POST)
        # On vérifie que le formulaire ainsi obtenu est valide et que la valeur du champ 'confirm' est égale à True
        if confirm_form.is_valid() and confirm_form.cleaned_data['confirm']:
            # si c'est le cas, on envoie les données de la requête à la vue DeleteView
            return super().post(request, *args, **kwargs)
        # else:
        #     # sinon repropose le formulaire
        #     return self.form_invalid(confirm_form)


class PostUpdateView(UpdateView):
    model = BlogPost  # l'attribut 'model' est obligatoire dans une UpdateView même en présence de 'form_class'
    form_class = BlogPostForm
    template_name = "blog/create_or_update_post.html"

    # on récupère le contexte de la classe super() pour ensuite le modifier afin de pouvoir l'utiliser dans le template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submit_text"] = "Modifier"
        return context

# Exemples de vues basées sur les fonctions

# def blog_posts(request):
#     posts = BlogPost.objects.all()
#
#     return render(request, "blog/index.html", context={"posts": posts})


# def blog_post(request, slug):
#     post = BlogPost.objects.get(slug=slug)
#
#     return render(request, "blog/post.html", context={"post": post})


# def blog_post_create(request):
#     # print(request.method)
#     if request.method == "POST":
#         form = BlogPostForm(request.POST)
#         if form.is_valid():
#             form.instance.published = True
#             if request.user.is_authenticated:
#                 form.instance.author = request.user
#             form.save()
#             return HttpResponseRedirect(reverse("blog-index"))
#     else:
#         form = BlogPostForm()
#
#     return render(request, "blog/create_or_update_post.html", {"form": form})



