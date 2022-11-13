from .models import Movie

def lista_filmes_recentes(request):
    list_filmes = Movie.objects.all().order_by('-data_criacao')[0:8]
    return {"lista_filmes_recentes": list_filmes}


def lista_filmes_populares(request):
    list_filmes = Movie.objects.all().order_by('-visualizacoes')[0:8]
    return {"lista_filmes_populares": list_filmes}

def filme_destaque(request):
    lista_filmes_destaque = Movie.objects.order_by('-data_criacao')[0]
    return {"lista_filmes_destaque": lista_filmes_destaque}
