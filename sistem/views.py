from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import Usuario, Acesso, Relatorio  # Adicionado Relatorio
import logging

logger = logging.getLogger(__name__)

# ESTRUTURA ORIGINAL (DICIONÁRIO SIMPLES)
relatorios_urls = {
    'Dashboard Comercial':'https://app.powerbi.com/view?r=eyJrIjoiMTEwOGZjYTUtZGFjZC00ZThlLWFiYjUtMmQwOGExYTQzOGU5IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9&pageName=46b4077b080b2b4404d1',
    'Marketing':'https://linktr.ee/colubrificantes',
    'Novo Painel':'https://app.powerbi.com/view?r=eyJrIjoiYjIxZmE1N2QtZTg2OS00M2U5LWI2ZGYtNzhiN2IzNmRmYjZjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - Business Intelligence': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ein-hXyOGLFCh-FVwHmmHucBVpWVBOoGh5nSMg4w_g2j7w?e=BnvepW',
    'OneDrive - Diretor e Gerente Geral': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ein-hXyOGLFCh-FVwHmmHucBVpWVBOoGh5nSMg4w_g2j7w?e=VBBIZH',
    'One Drive Gerente Consumo': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Euf-04YEZqxIrNmm3nL6yMQBr_bS2sKZ8VCP6rxbThErVQ',
    'OneDrive Gerente Revenda': 'https://colubrificantes-my.sharepoint.com/:f:/r/personal/sabrina_manzoli_colubrificantes_com_br/Documents/ONEDRIVE%20COMERCIAL/REVENDA?e=5%3a69b5e3c24c7444db80bb58e226a810b6&sharingv2=true&fromShare=true&at=9',
    'OneDrive - COORD REVENDA - MS': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Enjok5klGqpEjKVFGhazJbgBrfcf7bNAcUunO6MVdgNajA?e=j0zX5y',
    'OneDrive - COORD REVENDA - MT Sul': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EggYms1nftdPpnzoAsmMI28BJcXreG9CnoAXctcAIj-IKQ',
    'OneDrive - COORD REVENDA - MT Norte': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuAddOfY2c5DmoW80Gr4rrcBocXpRhF4xQSP2RkHFrut8A?e=Fh4rjE',
    'OneDrive - INSIDE': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Eh10RGR4UMpLhi-KtcA6xh0B-20RwZMoCZK5TOn6OP5gjQ?e=HF5GPt',
    'OneDrive - COORD CONSUMO - MT': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/En408h0ED8hMkcdiZP-6xMEBwOj8w-kEtdyIcfmnQWbztg?e=oYDgba',
    'OneDrive - COORD CONSUMO - AGRI - MS': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Eho5jGEx_nBJs4UtiQbU8fgBCDllr0AQg53KgjWos3YsTA?e=ZnNiIA',
    'OneDrive - COORD CONSUMO - MS': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsV1cc3j85hCv2YOtlOqftoBRAqXSJ2waNgAUK2gd1VcEA?e=7zG7r8',
    'OneDrive - V10094': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EkD67IqV0OdEr03LLz1sUW4BVLcvkUaKa_gXAPMRtFF-8w?e=iHrXPX',
    'OneDrive - V10096': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ErIyLJ_Vj8lFgmu9cVtRh0MBPBjsEviR0Ttkty4YYc0dAQ?e=LLpgzk',
    'OneDrive - V10097': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsPyXkbVChxOs_enTLBLDF4BmTkQV9ZlPeffhFif9flerQ?e=7vS8PR',
    'OneDrive - V10113': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsbzMMlq1gJHhIThsQDPwSABX9UJUx12MMUWVEIiuLBokw?e=9qrgqN',
    'OneDrive - V10099': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Erd_k9lYmJdDowWCNPvRlrIBps3BDtA2s-iZzAHkmtDEcA?e=8ajVRX',
    'OneDrive - V10111': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EheXU-iH46lDlJlx8ZqQ9m8B1r8fmcWHlXq1jJxXuziV0Q?e=hTUvuB',
    'OneDrive - V20048': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Etg47nS1nqtCrHDzekwBVq0BMitMOAfxp7IYupzMZ6yZ9Q?e=mS7LnU',
    'OneDrive - V20086': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EvacKj79cd1KjEJXHcgGEz8B6PHo8q9pwMbZScCl2uj8Xg?e=9xdc9o',
    'OneDrive - V20113': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuzP6mPqo9JGtvtC6FL1wPcB7zBqsjAdVbMWTX6yO6XItA?e=ZKe6yL',
    'OneDrive - V20033': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EiZW75iV3HpMof4ICXd03kcBJV4y6bcHt385GJbhFpLZ1g?e=5pmiii',
    'OneDrive - V20045': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ErlO_rGLHoRFs3b9mZBNtGsBnndBE2BBwJkbCjYLAlkxXA?e=Di0hCr',
    'OneDrive - V20050': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ErDkwWM6VRJNm09gRIDYbZgBKdm_4txZPfMtbKryNME88A?e=qS70j5',
    'OneDrive - V20052': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EvTwwXbK0RtFngov0SpO5A0BG8nK_aGM2IhAbjX62PbwrA?e=KhVtJB',
    'OneDrive - V20054': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EkUEwYay18NDnCDbbW8p3mYBZIBPVT4phKZSHvu7RLrEUA?e=yCpLLy',
    'OneDrive - V20076': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EqdqchXv8dVFlLkD_fJdGD0BHtB-x2LFILSOG3-HfXrjhg?e=81AJ9w',
    'OneDrive - V20087': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ErHAIyrd4qBMlWaCs4L45ooBxIBilplL5APQqKqxIwXfjg?e=7lDMQu',
    'OneDrive - V20099': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ElQgXKkqqpBAvjsrFxcfJvgB6jOHI1_F76cZ1nojDfUuQQ?e=qcRifA',
    'OneDrive - V20114': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EgFFfHbes99EgJlgVVmx08ABp8GOByUu34MIkrweq1RpoQ?e=zRU0Nd',
    'OneDrive - CONSUMO': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Eo46Tcxg0qZHtYAO5Y3F7koB3F9yF70tnDooNcOGHT7ViQ?e=d35j9r',
    'OneDrive - REV MS': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuFlaGpkDTtIg_RJdj-gBl0Bgd2zBfv55nG9W1L7n9hKyg?e=SO1Qgr',
    'OneDrive - REV MT': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsdC19yakbxCsVK2eFM3qj4Bhgj83ONMyPZ4zZVZAW0Z8Q?e=M86puY',
    'OneDrive - ISR02': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ElkKW78BlSFEhr09HQ0GOtQBkiYXxJJhb4JXylCK6Vt1ug?e=vDk8VA',
    'OneDrive - ISR03': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EgcO1UBgS2ZFqFaPmjB1KN8Bva0HRxnuLzp-h6XWAtb-eQ?e=Oasx8H',
    'OneDrive - ISR04': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ElrD9iqYDEtKrqL4UqrDV_EBXrJGJbaAU6u_dHwB5iTc4w?e=dzU73m',
    'OneDrive - ISR07': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsgllcZpbZ1JsgHBHF9gVr4Bt4gX7ejkdl3u9lQR5vUZCw?e=X8Mf2g',
    'OneDrive - ISR08': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EkWEf1EHmyFAhJd0_fF4DlEBo9OHGof1HtuqVArXMm-I3Q?e=x0LA3u',
    'OneDrive - CONSUMO MT': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EgkqRH7T9vZCo3KnlZ9BwGgBTeYfa94YUq3UYTnsowZnCw?e=9ktJi9',
    'OneDrive - R10002': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EnluWqlKR39OpfUVDxVtw8cBibD0LtNtNiM2eKAcjfz-5g?e=hayzcg',
    'OneDrive - R10004': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EnAd-sIoj6dOlRACCc5SC3QBgln1GKmOhu09tzwJ85n2OQ?e=fZgrbY',
    'OneDrive - R10005': ' https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Enk0Erdw7RtInSYNr0gImFUBMfPaJ6Vf4vVG_ro45Y-ZAA?e=5OmACa',
    'OneDrive - R10006': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EthcrSt_zI9PrDAFwfS_7LQBHH-W8OAaXEPIpGHEfEUI0A?e=hIaVIQ',
    'OneDrive - R10007': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ElAhsT9mlylLr4EmpcHiwh8B08XCXNZc0uiEUjDDWtBxgw?e=nNd8ts',
    'OneDrive - R10008': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EmBMR65N8lNDoBLO5YZp5X4B4Od22y3TKXx76GohJJyCRQ?e=yu5skA',
    'OneDrive - R10010': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ej6W9_81pphBpBjz4UqdKWcBuEZ2nDE-6NyXlwAhmyvfZQ?e=Hsm8IZ',
    'OneDrive - V10098': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ej6W9_81pphBpBjz4UqdKWcBuEZ2nDE-6NyXlwAhmyvfZQ?e=Hsm8IZ',
    'OneDrive - V10112': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuyJp5oQYEJGrw4fH-i-dGEB-HB1BFdsKbkBF-yg6zhKQA?e=1WOuVt',
    'OneDrive - R20005': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuWu-RP9Hv9OorYpaKhgF4IBxW2cownGJUD_lR_RPMfcPQ?e=xpTC8P',
    'OneDrive - R20009': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EnUUqka05eRPhW4MEG8bHVYB_EGBc3I8vjm2Gv-V9XDT5w?e=RDzhpw',
    'OneDrive - R20010': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EliQPazGsAdAn5RhVxmC5joBGluzCJco1aG3Iy2XRE-xoA?e=whDMDj',
    'OneDrive - R20011': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Et1wCwDeceNDqCphdZHDbwwBGwiLiE5aLTQyqD81KtpS1w?e=cc82VL',
    'OneDrive - R20014': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ek5XdS-uvFhGmU_l7v4zNIIBgzancotPv1A4NDQ9OeAwyA?e=ZheoJo',
    'OneDrive - R20039': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ElGuJWEjmXpLlwF-qrXOif8BYR0v5byIBG_F5IUQUFwNJw?e=NoQqPu',
    'OneDrive - R20001': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EgzzGixFt-hBiSLhdxnty-YB0mYRpCFH4P3JsOlJsrXjWA?e=6fPewa',
    'OneDrive - R20003': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EpMs_G202JlEoUu6i2e8gL4Bo_XFV62pfgujDSurxfWotg?e=gkMskT',
    'OneDrive - R20006': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/En2UBW0CmJdKmH15I22cGoUB0Qyb9LWb1KVmTxkmco621g?e=Rgdo8k',
    'OneDrive - R20008': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuyeW0hHebdEmZiS32CAP-wBpbwYqgdOM6dw8kZmUgNusw?e=fsgbCi',
    'OneDrive - R20012': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EvIWf2A3tg5NprlBWt63CNEBnpyCUdR7s1jgj9Z1MrFw8A?e=tXmurI',
    'OneDrive - R20015': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EvCgjCAlsWpLgPbtVRorJsUB9uutEbrbJo3FkhdqHZIFSw?e=iqKu1o',
    'Logistica': 'https://app.powerbi.com/view?r=eyJrIjoiZmE2YWQ3NTItMmE1NS00MmY4LTk0ZjAtY2RlNjhiZTVlMGVkIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9&pageName=ReportSectione8639981062376e059d9',
}

def verificar_credenciais(usuario, senha):
    try:
        user = Usuario.objects.get(usuario=usuario, senha=senha)
        if user.acesso:
            # USANDO O NOME CORRETO DO CAMPO 'relatorio'
            relatorios_list = list(user.relatorios.all().values_list('relatorio', flat=True))
            return relatorios_list, True
    except Usuario.DoesNotExist:
        return [], False

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        senha = request.POST['senha']

        relatorios, acesso_liberado = verificar_credenciais(usuario, senha)
        if acesso_liberado:
            request.session['usuario'] = usuario
            request.session['relatorios'] = relatorios
            request.session.set_expiry(14400)

            usuario_obj = Usuario.objects.get(usuario=usuario)
            usuario_obj.last_login = timezone.now()
            usuario_obj.save()

            Acesso.objects.create(
                usuario=usuario_obj,
                ip_address=request.META.get('REMOTE_ADDR')
            )

            logger.info(f'Usuário {usuario} realizou login em {timezone.now()}')

            return redirect('relatorios')
        else:
            return render(request, 'login.html', {'erro': 'Usuário ou senha incorretos'})

    return render(request, 'login.html')

def relatorios_view(request):
    if not request.session.get('usuario'):
        return redirect('login')

    usuario = request.session['usuario']
    relatorios = request.session.get('relatorios', [])
    
    # USANDO A ESTRUTURA DE DICIONÁRIO ORIGINAL
    relatorios_disponiveis = [{'nome': r, 'url': relatorios_urls.get(r, '#')} for r in relatorios]

    # PARÂMETRO CORRETO 'relatorio' (SINGULAR)
    relatorio_nome = request.GET.get('relatorio')
    relatorio_selecionado = relatorios_urls.get(relatorio_nome) if relatorio_nome in relatorios else None

    return render(request, 'relatorios.html', {
        'relatorios': relatorios_disponiveis,
        'relatorio_selecionado': relatorio_selecionado,
        'usuario': usuario,
    })

def logout_view(request):
    logout(request)
    return redirect('login')