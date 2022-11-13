from django.shortcuts import render, redirect, reverse
from .models import Movie, Usuario
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CriarContaForm, FormHome

# Create your views here.


class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHome

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        else:
            return super().get(self, request, *args, **kwargs)

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')


class Homefilmes(LoginRequiredMixin,ListView):
    template_name = 'homefilmes.html'
    model = Movie
    # object_list - > lista de itens do modelo


class Detalhesfilme(LoginRequiredMixin,DetailView):
    template_name = 'detalhesfilme.html'
    model = Movie
    # object -> um item da lista de filmes

    def get(self, request, *args, **kwargs):
        filme = self.get_object()
        filme.visualizacoes = filme.visualizacoes + 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        #filtrar tabela de filmes com base nos filmes na mesma categoria...
        filmes_relacionados = Movie.objects.filter(categoria=self.get_object().categoria)[0:4]
        context['filmes_relacionados'] = filmes_relacionados
        return context


class Pesquisarfilme(LoginRequiredMixin,ListView):
    template_name = 'pesquisa.html'
    model = Movie

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = Movie.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None


class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = 'editarpefil.html'
    model = Usuario
    fields = ["first_name", "last_name", "email"]

    def get_success_url(self):
        return reverse('filme:homefilmes')

    def get(self, request, *args, **kwargs):
        if int(self.request.path.replace("/editarperfil/", "")) == self.request.user.id:
            return super().get(self, request, *args, **kwargs)
        else:
            return redirect(f'/editarperfil/{self.request.user.id}')





class Criarconta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:homefilmes')




#def homefilmes(request):
 #   context = {}
  #  lista_filmes = Movie.objects.all()
   # context['lista_filmes'] = lista_filmes
    #return render(request, "homefilmes.html",context)


# def homepage(request):
# return render(request, 'homepage.html')
