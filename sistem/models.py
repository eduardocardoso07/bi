from django.db import models

class Coordenador(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    relatorios = models.ManyToManyField('Relatorio', related_name='usuarios', blank=True)
    acesso = models.BooleanField()
    onedrive_link = models.URLField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    coordenador = models.ForeignKey(Coordenador, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendedores')

    def __str__(self):
        return self.usuario


class Relatorio(models.Model):
    nome = models.CharField(max_length=255)  # O tamanho deve corresponder ao banco de dados (255)
    link = models.CharField(max_length=2000)
    acesso_externo = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Acesso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='acessos')
    data_hora = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f'{self.usuario.usuario} - {self.data_hora}'
