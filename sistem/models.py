from django.db import models

class Coordenador(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome

class Relatorios(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)  # Evita conflito com o nome do modelo
    link = models.TextField()
    acesso_externo = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=100)
    relatorios = models.ManyToManyField(
        Relatorios, 
        through='UsuarioRelatorios', 
        blank=True, 
        related_name='usuarios_relacionados'
    )  # Alterado related_name para evitar conflitos
    acesso = models.BooleanField()
    onedrive_link = models.URLField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    coordenador = models.ForeignKey(Coordenador, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendedores')

    def __str__(self):
        return self.usuario

class UsuarioRelatorios(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    relatorio = models.ForeignKey(Relatorios, on_delete=models.CASCADE)
    data_associacao = models.DateTimeField(auto_now_add=True)

class Acesso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='registros_acesso')
    data_hora = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f'{self.usuario.usuario} - {self.data_hora}'
