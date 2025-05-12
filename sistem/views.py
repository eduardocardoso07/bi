from django.views.decorators.http import require_POST
from django.contrib import messages
from openpyxl import Workbook
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from sistem.forms import BrindeForm, LancamentoForm
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import Usuario, Acesso, Lancamentos, Brindes
import logging

logger = logging.getLogger(__name__)

# ESTRUTURA ORIGINAL (DICIONÁRIO SIMPLES)
relatorios_urls = {
    'Comercial': {
        'Comercial Geral': 'https://app.powerbi.com/view?r=eyJrIjoiNTE5YWNiMWMtODFiZi00MTA1LTljZTItYzg5YzM3MTUzZGE5IiwidCI6IjVmOWVhMWVjLTE4Y2UtNGFlZi1hNzBhLTI3MjQ1M2ViYWVjNiJ9',
        'Comercial Revenda': 'https://app.powerbi.com/view?r=eyJrIjoiZGY1MjNlYjctMzI4MS00ZDQwLWJjODctYjBkZmI5YjQwOGMwIiwidCI6IjVmOWVhMWVjLTE4Y2UtNGFlZi1hNzBhLTI3MjQ1M2ViYWVjNiJ9',
        'Comercial B2B': 'https://app.powerbi.com/view?r=eyJrIjoiODIwNjc3MTUtOWUwYy00YjNhLWIwMTctNzg4YmY4Mzk5YzMxIiwidCI6IjVmOWVhMWVjLTE4Y2UtNGFlZi1hNzBhLTI3MjQ1M2ViYWVjNiJ9',

        'Comercial Revenda MS': 'https://app.powerbi.com/view?r=eyJrIjoiZmM1MDRjYzItZDc3NC00MDAxLWE1MDktNjEyNzAzNjg1NTExIiwidCI6IjVmOWVhMWVjLTE4Y2UtNGFlZi1hNzBhLTI3MjQ1M2ViYWVjNiJ9',
        'Comercial Revenda MT': 'https://app.powerbi.com/view?r=eyJrIjoiN2U5OTc4OWUtOTZhZC00ZTYyLWFlZTQtZWEzMGEzYThmYzcxIiwidCI6IjVmOWVhMWVjLTE4Y2UtNGFlZi1hNzBhLTI3MjQ1M2ViYWVjNiJ9',
        'Comercial Revenda MT': 'https://app.powerbi.com/view?r=eyJrIjoiYTdkMDk2NjktYjlkZC00MWJiLWIxMTgtYWJhYjQ1NzQyNGVjIiwidCI6IjVmOWVhMWVjLTE4Y2UtNGFlZi1hNzBhLTI3MjQ1M2ViYWVjNiJ9',
        'Comercial Consumo MS e MT': 'https://app.powerbi.com/view?r=eyJrIjoiYjczM2E3N2UtMDY1Ni00YzUyLWI1YmItN2Y4ZmRhMmE4NGMzIiwidCI6IjVmOWVhMWVjLTE4Y2UtNGFlZi1hNzBhLTI3MjQ1M2ViYWVjNiJ9',
        'Comercial Consumo MS' : 'https://app.powerbi.com/view?r=eyJrIjoiMDZmMDdmNjItNDljNy00NmFlLWIzYmEtOGMxYmE4ZDFiMzc1IiwidCI6IjVmOWVhMWVjLTE4Y2UtNGFlZi1hNzBhLTI3MjQ1M2ViYWVjNiJ9',
        'Comercial Consumo MT': 'https://app.powerbi.com/view?r=eyJrIjoiMjJmNGE1YTItODNkYy00M2UyLWE0ZmItMzZlZDQxNDE2YWM4IiwidCI6IjVmOWVhMWVjLTE4Y2UtNGFlZi1hNzBhLTI3MjQ1M2ViYWVjNiJ9',
        'VEND124 - REV - MS': 'https://app.powerbi.com/view?r=eyJrIjoiOTg5ZWRmOGItYTVlMS00NDc2LTlhOTAtZDNmY2U4OWU0OTRmIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    }
}

logistica_url = {
    'Logística': 'https://app.powerbi.com/view?r=eyJrIjoiZjQyNmViZjItNWYyNC00NDU4LTlkNTgtM2VmNTNjNmZjNzNhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
}

financeiro_url = {
    'Financeiro': 'https://app.powerbi.com/view?r=eyJrIjoiYzgyZTFmYWYtYzQ1ZC00ODZhLWFmMmYtMWJjYmJjMjJhMTQ4IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9'
}

def verificar_credenciais(usuario, senha):
    try:
        user = Usuario.objects.get(usuario=usuario, senha=senha)
        if user.acesso:
            relatorios_list = list(user.relatorios.all().values_list('relatorio', flat=True))
            return user, relatorios_list, True
        else:
            return user, [], False
    except Usuario.DoesNotExist:
        return None, [], False  # agora retorna 3 valores corretamente
    
def login_view(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        senha = request.POST['senha']

        usuario_obj, relatorios, acesso_liberado = verificar_credenciais(usuario, senha)

        if acesso_liberado:
            request.session['usuario_id'] = usuario_obj.id  # salva ID do usuário
            request.session['relatorios'] = relatorios
            request.session.set_expiry(14400)  # 4 horas

            usuario_obj.last_login = timezone.now()
            usuario_obj.save()

            Acesso.objects.create(
                usuario=usuario_obj,
                ip_address=request.META.get('REMOTE_ADDR')
            )

            logger.info(f'Usuário {usuario} realizou login em {timezone.now()}')

            return redirect('tela')
        else:
            return render(request, 'login.html', {'erro': 'Usuário ou senha incorretos'})

    return render(request, 'login.html')

def logistica_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario_id = request.session['usuario_id']

    usuario_id = request.session['usuario_id']
    relatorios = request.session.get('relatorios', [])
    nome_relatorio_associado = "".join(relatorios) # Recebendo o nome do relatório associado ao usuário em formato de String
    nome_relatorio_associado = nome_relatorio_associado.replace('Comercial Geral', "")
    nome_relatorio_associado = nome_relatorio_associado.replace('Financeiro', "")
    print(nome_relatorio_associado)

    # Gerando a lista de relatórios disponíveis
    # relatorios_disponiveis = [{'nome': r, 'url': relatorios_urls.get(r, {}).get(usuario, '#')} for r in relatorios]

    # Obtendo o nome do relatório da URL
    relatorio_nome = request.GET.get('relatorio')

    if relatorio_nome and nome_relatorio_associado in logistica_url:
        relatorio_selecionado = logistica_url[relatorio_nome]
        print(f"Relatório Encontrado: {relatorio_selecionado}")

    else:
        relatorio_selecionado = None
        print("Relatório não encontrado ou usuário sem permissão.")

    # Renderizando o template com os dados
    return render(request, 'logistica.html', {
        # 'relatorios': relatorios_disponiveis,
        'relatorio_selecionado': relatorio_selecionado,
        'usuario_id': usuario_id,
    })

def comercial_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario_id = request.session['usuario_id']
    relatorios = request.session.get('relatorios', [])
    nome_relatorio_associado = "".join(relatorios) # Recebendo o nome do relatório associado ao usuário em formato de String
    nome_relatorio_associado = nome_relatorio_associado.replace('Logística', '')
    nome_relatorio_associado = nome_relatorio_associado.replace('Financeiro', '')

    print(nome_relatorio_associado)

    

    # Gerando a lista de relatórios disponíveis
    # relatorios_disponiveis = [{'nome': r, 'url': relatorios_urls.get(r, {}).get(usuario, '#')} for r in relatorios]

    # Obtendo o nome do relatório da URL
    relatorio_nome = request.GET.get('relatorio')

    # Verificando se o nome do relatório está na lista de relatórios e se a URL é válida para o usuário
    if relatorio_nome in relatorios_urls:
        if nome_relatorio_associado and relatorio_nome in relatorios_urls and nome_relatorio_associado in relatorios_urls[relatorio_nome]:
            # O relatório existe e a URL é válida para o usuário
            relatorio_selecionado = relatorios_urls[relatorio_nome].get(nome_relatorio_associado, '#')
            print(f"Relatório Encontrado = {relatorio_selecionado}")
        else:
            # Relatório não encontrado ou o usuário não tem permissão
            relatorio_selecionado = None
            print("Relatório Não Encontrado ou Usuário sem permissão")
    else:
        relatorio_selecionado = None
        print("Relatório Não Encontrado - else de fora")

    # Renderizando o template com os dados
    return render(request, 'comercial.html', {
        # 'relatorios': relatorios_disponiveis,
        'relatorio_selecionado': relatorio_selecionado,
        'usuario_id': usuario_id,
    })

def financeiro_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    relatorios = request.session.get('relatorios', [])
    nome_relatorio_associado = "".join(relatorios).replace('Logística', '').replace('Comercial Geral', '')

    relatorio_nome = request.GET.get('relatorio')
    relatorio_selecionado = None

    if relatorio_nome and nome_relatorio_associado in financeiro_url:
        relatorio_selecionado = financeiro_url[relatorio_nome]

    return render(request, 'financeiro.html', {
        'relatorio_selecionado': relatorio_selecionado,
        'usuario_id': usuario_id,
    })


def marketing_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario_id = request.session['usuario_id']
    
    usuario = Usuario.objects.get(id=request.session['usuario_id'])

    brindes = Brindes.objects.all().order_by('description')
    search = request.GET.get('search')
    print(search)
    
    if search:
        brindes = Brindes.objects.filter(description__icontains=search)
        
    if usuario.setor == "Marketing" or usuario.setor == "BI":

        return render(request, 'marketing.html', {
            'usuario': usuario,
            'brindes': brindes,
        })

    else:
        return redirect('sem_permissao')

class MarketingRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        usuario_id = request.session.get('usuario_id')

        if not usuario_id:
            print("Saind")
            return redirect('login')

        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            print("Saind pelo except")
            return redirect('login')

        if usuario.setor not in ["Marketing", "BI"]:
            return redirect('sem_permissao')

        request.usuario = usuario  # Guarda o objeto completo
        return super().dispatch(request, *args, **kwargs)

    

    
class new_brinde_view(MarketingRequiredMixin, CreateView):
    model = Brindes
    form_class = BrindeForm
    template_name = 'new_brinde.html'
    success_url = '/tela/marketing/'


class brinde_update_view(MarketingRequiredMixin, UpdateView):
    model = Brindes
    form_class = BrindeForm
    template_name = 'update_brinde.html'
    success_url = '/tela/marketing/'

    def get_object(self):
        return super().get_object()
    
class brinde_delete_view(MarketingRequiredMixin, DeleteView):
    model = Brindes
    template_name = 'brinde_delete.html'
    success_url = '/tela/marketing/'

class lancamento_view(MarketingRequiredMixin, CreateView):
    model = Lancamentos
    form_class = LancamentoForm
    template_name = 'new_lancamento.html'
    success_url = '/tela/marketing/lista_lancamento/'

    def form_valid(self, form):
        brinde = form.cleaned_data['brinde']
        quantidade_lancada = form.cleaned_data['quantidade_lancada']

        # Verifica se há estoque suficiente
        if brinde.quantity >= quantidade_lancada:
            # Subtrai do estoque
            brinde.quantity -= quantidade_lancada
            brinde.save()
            messages.success(self.request, "Lançamento realizado e estoque atualizado!")
            return super().form_valid(form)
        else:
            # Exibe erro e retorna à página sem salvar
            messages.error(self.request, "Estoque insuficiente para esse brinde.")
            return redirect(self.request.path)

class lista_lancamento_view(MarketingRequiredMixin, ListView):
    model = Lancamentos
    template_name = 'lista_lancamento.html'
    context_object_name = 'lancamentos'
    ordering = ['-data']
    paginate_by = 11

@require_POST
def lancamento_delete_view(request):
    ids = request.POST.getlist('selecionados')
    if ids:
        Lancamentos.objects.filter(id__in=ids).delete()
        messages.success(request, f"{len(ids)} lançamento(s) excluído(s) com sucesso.")
    else:
        messages.warning(request, "Nenhum lançamento foi selecionado.")
    return redirect('lista_lancamento')


def exportar_lancamentos_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Lançamentos"

    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    ws.append([f'Relatório exportado em: {agora}'])
    
    ws.append([])

    ws.append([
        'Data',
        'Nota Fiscal',
        'Cliente',
        'Vendedor',
        'Brinde',
        'Quantidade',
        'Valor Total',
        'Valor Unitário',
    ])

    for lanc in Lancamentos.objects.all():
        quantidade = lanc.quantidade_lancada or 0
        valor_total = float(lanc.valor_total or 0)
        valor_unitario = valor_total / quantidade if quantidade else 0

        ws.append([
            lanc.data.strftime('%d/%m/%Y') if lanc.data else '',
            str(lanc.nota_fiscal),
            str(lanc.cliente_codigo),
            str(lanc.vendedor),        # já tratado como string
            lanc.brinde.description if lanc.brinde else 'Sem brinde',
            quantidade,
            valor_total,
            round(valor_unitario, 2),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="relatorio_lancamentos.xlsx"'
    wb.save(response)
    return response

def tela_view(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario = Usuario.objects.get(id=request.session['usuario_id'])  # objeto completo

    return render(request, 'tela.html', {
        'usuario': usuario,
    })

def logout_view(request):
    logout(request)
    return redirect('login')