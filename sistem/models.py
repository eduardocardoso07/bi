from django.db import models

class Coordenador(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome

class Relatorio(models.Model):  # NOME CORRETO (SINGULAR)
    id = models.AutoField(primary_key=True)
    relatorio = models.CharField(max_length=100)  # NOME DO CAMPO CORRIGIDO
    link = models.TextField()
    
    def __str__(self):
        return self.relatorio  # RETORNA O CAMPO CORRETO

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=100)
    relatorios = models.ManyToManyField(
        Relatorio,  # REFERÊNCIA AO MODELO CORRETO
        related_name='usuarios',  # RELATED_NAME ORIGINAL
        blank=True
    )
    acesso = models.BooleanField()
    onedrive_link = models.URLField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    coordenador = models.ForeignKey(
        Coordenador, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='vendedores'
    )

    def __str__(self):
        return self.usuario

class Acesso(models.Model):
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='acessos'  # RELATED_NAME ORIGINAL
    )
    data_hora = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f'{self.usuario.usuario} - {self.data_hora}'