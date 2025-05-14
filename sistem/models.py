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


    setor = models.CharField(max_length=32, null=True, blank=True)

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
    
class Brindes(models.Model):


    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50, unique=True, verbose_name='Descrição')
    quantity = models.IntegerField(verbose_name='Quantidade')
    price = models.FloatField(verbose_name='Preço')
    image = models.ImageField(upload_to='tela/marketing/', blank=True, null=True, verbose_name='Imagem')

    def __str__(self):
        return self.description
    
class Lancamentos(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField(null=False, blank=False)
    nota_fiscal = models.IntegerField(null=True, blank=True)
    cliente_codigo = models.IntegerField(null=False, blank=False)
    vendedor = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    brinde = models.ForeignKey(Brindes, on_delete=models.CASCADE)
    quantidade_lancada = models.IntegerField(null=False, blank=False)
    
    @property
    def valor_total(self):
        return self.quantidade_lancada * self.brinde.price

    def __str__(self):
        return f"{self.id}"
    
