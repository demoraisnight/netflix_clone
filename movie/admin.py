from django.contrib import admin
from .models import Movie, Episodio, Usuario
from django.contrib.auth.admin import UserAdmin

campos = list(UserAdmin.fieldsets)
campos.append(
    ("Histórico", {'fields': ('filmes_vistos',)})
)
UserAdmin.fieldsets = tuple(campos)

admin.site.register(Movie)
admin.site.register(Episodio)
admin.site.register(Usuario, UserAdmin)




