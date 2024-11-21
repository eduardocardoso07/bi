from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import Usuario, Acesso
import logging

logger = logging.getLogger(__name__)

relatorios_urls = {
    'Acompanhamento Gerentes': 'https://app.powerbi.com/view?r=eyJrIjoiYmZlNmNlZjYtZmNhZS00MDE4LTliMWQtYmExNWQ4NGZlZTlkIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Acompanhamento Diario': 'https://app.powerbi.com/view?r=eyJrIjoiNGE3MWQ5NjgtMzc1Ny00MGZmLWEzMDMtYTU1MTNmMzUwZDMxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'DAP KPI - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiZjI1NGY3NTktYTllMC00OGFmLThmYzctYjk5NGU1MWI4YzA0IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Performance CO': 'https://app.powerbi.com/view?r=eyJrIjoiODRmZDQ2ZjQtZTdkMS00ZDI3LWE4NzQtZjMyMWI0NGUzMzZmIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Potencial Área': 'https://app.powerbi.com/view?r=eyJrIjoiZWZkYTI3OTQtZjFkMS00Zjg5LTg3MzctZWZiMjcxMTg0YjhmIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Simulador Remuneração': 'https://app.powerbi.com/view?r=eyJrIjoiMDJlNDEwY2MtNjI5ZS00OTgyLWIxOGItMDhmM2MyODE5MmM0IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - Business Intelligence': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ein-hXyOGLFCh-FVwHmmHucBVpWVBOoGh5nSMg4w_g2j7w?e=BnvepW',
    'OneDrive - Diretor e Gerente Geral': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ein-hXyOGLFCh-FVwHmmHucBVpWVBOoGh5nSMg4w_g2j7w?e=VBBIZH',
    'Base de conhecimento Tecnologia da Informação':'https://linktr.ee/ti.colub',
    'Sales Development Representative':'https://app.powerbi.com/view?r=eyJrIjoiNjI4MDdiNzgtMGQyNC00OTgwLTliZGUtM2RkZDA5MzczN2JkIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Campanha Acelerando Execução':'https://app.powerbi.com/view?r=eyJrIjoiNzgwZjllMjYtNWU2YS00YTAxLTkwZWItZWEyMzc5YjUxYmUzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Revisão de Negócios':'https://app.powerbi.com/view?r=eyJrIjoiOTJlOWZiMmYtZDQxMi00ZGFjLWIzM2QtYWZmNDlmNjYzMjQxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Acompanhamento de Vendas':'https://app.powerbi.com/view?r=eyJrIjoiOWI0MTU2ZmEtYTYwZi00YzJiLThhYzQtOWY1NjdjODNiNThmIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Produtividade Diária':'https://app.powerbi.com/view?r=eyJrIjoiOTE2YzVlZGUtNDg4NC00ZmIxLWExZTYtMGZiNWJlNjMyZDBmIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Análise de Preço':'https://app.powerbi.com/view?r=eyJrIjoiM2JjOTI4MGMtNDY5Yi00YmUwLWI2MzYtNWVmZjVkZjkyOGJlIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',


    'Acompanhamento Gerentes - Revenda': 'https://app.powerbi.com/view?r=eyJrIjoiMjkwYTU3ZDktZjI0MC00Yjg1LWFlZGUtODI1ODAwNTVkNGFiIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Acompanhamento Gerentes - Consumo': 'https://app.powerbi.com/view?r=eyJrIjoiM2IxY2UyOTktMzcxMy00NzZhLWEwNmQtNzlkMGYwZjA4NDU5IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Acompanhamento Diario - Revenda': 'https://app.powerbi.com/view?r=eyJrIjoiYmRlOWE0M2UtZmQ0MS00NzdmLTgzNzgtNmRjMzhhYzA3NTUxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Acompanhamento Diario - Consumo': 'https://app.powerbi.com/view?r=eyJrIjoiYzA0Nzg5ZjYtMWVhMy00NzU3LWJmMjEtY2EyNTEyYjI0MTYxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'DAP KPI Revenda - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiMWExM2QxNzItYjgwNi00NzFjLWJiNzktYTE3MzJiZmFlYTAxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'DAP KPI Consumo - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiYjRhNmVjZDItMzFjZC00MDNlLThmZjQtN2MxMGMzZjI0ZDJhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Performance Gerente Revenda': 'https://app.powerbi.com/view?r=eyJrIjoiZjY2ZDQxYmEtNGYzYS00MWU0LTlhNDItNDhjMzcxYmFkMzU5IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Performance Gerente Consumo': 'https://app.powerbi.com/view?r=eyJrIjoiYzgwNTc2MjItMDIxYi00OTY3LWIyM2YtNmQwZmY4NWM3ZGNkIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Potencial Área - Revenda': 'https://app.powerbi.com/view?r=eyJrIjoiNjFhMGQ4OTktOTQxYy00ZTk1LWJmYzUtMDQ5NmI1MTdiMmYwIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Potencial Área - Consumo': 'https://app.powerbi.com/view?r=eyJrIjoiNTkxMGZkNDAtNmI0Yi00ZDU1LTliYmQtY2NhYWE4Yzk1YjI1IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'One Drive Gerente Consumo': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Euf-04YEZqxIrNmm3nL6yMQBr_bS2sKZ8VCP6rxbThErVQ',
    'OneDrive Gerente Revenda': 'https://colubrificantes-my.sharepoint.com/:f:/r/personal/sabrina_manzoli_colubrificantes_com_br/Documents/ONEDRIVE%20COMERCIAL/REVENDA?e=5%3a69b5e3c24c7444db80bb58e226a810b6&sharingv2=true&fromShare=true&at=9',
    'Produtividade Diária - Gerente Consumo':'https://app.powerbi.com/view?r=eyJrIjoiNmVmY2UyMDItZjY5Yi00NjJjLWExMzctOGM2MDFhMWVkMDc0IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Produtividade Diária - Gerente Revenda':'https://app.powerbi.com/view?r=eyJrIjoiMzc2MDI1NjQtNmI0OS00OTZmLWE5OGYtMzIxMzJiZTI1NmM2IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',

    'Acompanhamento Diario - CONSUMO - MS': 'https://app.powerbi.com/view?r=eyJrIjoiZjI2NjNiZmUtZjI4OC00MGM1LTk4OTItM2ViZDJiM2EyMDc0IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Acompanhamento Diario - CONSUMO - MT': 'https://app.powerbi.com/view?r=eyJrIjoiMjNmNTRhYWItMjY2MS00NjA2LThiYTAtNjkzMzMzOWFmZDAxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Acompanhamento Diario - CONSUMO AGRI - MS': 'https://app.powerbi.com/view?r=eyJrIjoiMTU4ZWEwYTgtYzZmOS00Y2NiLTk3NDUtN2RiZmZiMmIxZTVjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Acompanhamento Diario - INSIDE': 'https://app.powerbi.com/view?r=eyJrIjoiNzY4MTUwODMtYTJlNy00NmVkLTg4NmYtYTY3MzUzZDIyYWFhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Acompanhamento Diario - REVENDA - MS': 'https://app.powerbi.com/view?r=eyJrIjoiNjAyOTI3YjctMGIwNS00NTMwLWI1MzQtYjIxMDE0YTRjZmNjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Acompanhamento Diario - REVENDA - MT Norte': 'https://app.powerbi.com/view?r=eyJrIjoiZjg2ODcxMzYtNWVjZi00YjUxLThhOGEtZjQ5NGUxNzgxYWNlIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Acompanhamento Diario - REVENDA - MT Sul': 'https://app.powerbi.com/view?r=eyJrIjoiNWNiNDNlZmEtOTc1NS00MGZiLWFhYTUtODE3YmU5NTJlYWY2IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    
    'DAP KPI Consumo Agri MS - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiY2IzNGE3NGUtMmFkYy00ZWI1LTkxYTItMDhiZWFlOGM0YTJjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'DAP KPI Consumo MS - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiNmUxMzIzY2YtNWE1OC00NzUzLTgzZWYtYmVhYjZhZmI3NzkxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'DAP KPI Consumo MT - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiZGZjOWFiY2QtNWU2My00NDU2LWJiMWUtOTg5ODBlYTMzZmYyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'DAP KPI Inside Sales - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiMGZlZDA2ZWEtYjQzOS00MjUyLTkyYmItMThjMWQwYWI0NDgxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'DAP KPI Revenda MS - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiMTQxMjJiN2QtZjg1Ny00ZWEwLThkYjItZThjNTE4ZWIwYjYxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'DAP KPI Revenda MT Norte - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiYmJiYWFiNGYtNDA2OC00ODVlLThhMTUtNzY2NjU5MTBlNTdjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'DAP KPI Revenda MT Sul - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiYWEwYWM2YTYtNTZjMS00MDM1LWFiNDYtNzIxMjM3M2ZjMzQzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    
    'Performance Coordenador - CONSUMO - MS': 'https://app.powerbi.com/view?r=eyJrIjoiMzgzODUwYWQtOWEzMC00NWYzLTkyMzktYTE0Yjc5MjE4YzVlIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Performance Coordenador - CONSUMO - MT': 'https://app.powerbi.com/view?r=eyJrIjoiNzdkNDlkY2EtNmFhMy00MDFiLWJkODEtNWQ2NWQ5YmNkYWRhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Performance Coordenador -CONSUMO AGRI - MS': 'https://app.powerbi.com/view?r=eyJrIjoiMDY2OTQ3M2EtZWNmNi00ZDQ3LTg4NTktYmFjYjc0OWJlNDcyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Performance Coordenador - INSIDE': 'https://app.powerbi.com/view?r=eyJrIjoiODI4NmQwMTEtMjU5OS00MzUyLThhMDAtZWU4NTFmOGZjODYyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Performance Coordenador - REVENDA - MS': 'https://app.powerbi.com/view?r=eyJrIjoiMWIxN2M4ZDItZDc5Zi00MWIwLThiMjEtMjdiNTc3MmM4OWE4IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Performance Coordenador - REVENDA - MT Norte': 'https://app.powerbi.com/view?r=eyJrIjoiNTE5NmRiNGYtMWU3My00Yjc0LTgxYzktZmY1NGVlMzg4NDUzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Performance Coordenador - REVENDA - MT Sul': 'https://app.powerbi.com/view?r=eyJrIjoiNDljNDNiYjUtZDk5Ni00NDZiLTlhZTUtOTc3M2YwNTZhMDJiIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    
    'OneDrive - COORD REVENDA - MS': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Enjok5klGqpEjKVFGhazJbgBrfcf7bNAcUunO6MVdgNajA?e=j0zX5y',
    'OneDrive - COORD REVENDA - MT Sul': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EggYms1nftdPpnzoAsmMI28BJcXreG9CnoAXctcAIj-IKQ',
    'OneDrive - COORD REVENDA - MT Norte': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuAddOfY2c5DmoW80Gr4rrcBocXpRhF4xQSP2RkHFrut8A?e=Fh4rjE',
    'OneDrive - INSIDE': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Eh10RGR4UMpLhi-KtcA6xh0B-20RwZMoCZK5TOn6OP5gjQ?e=HF5GPt',
    'OneDrive - COORD CONSUMO - MT': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/En408h0ED8hMkcdiZP-6xMEBwOj8w-kEtdyIcfmnQWbztg?e=oYDgba',
    'OneDrive - COORD CONSUMO - AGRI - MS': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Eho5jGEx_nBJs4UtiQbU8fgBCDllr0AQg53KgjWos3YsTA?e=ZnNiIA',
    'OneDrive - COORD CONSUMO - MS': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsV1cc3j85hCv2YOtlOqftoBRAqXSJ2waNgAUK2gd1VcEA?e=7zG7r8',
    
    'Produtividade Diária CONS - AGRI - MS':'https://app.powerbi.com/view?r=eyJrIjoiMThmOTE1NTktYTdlMS00NDMzLWFmOTktNmUzMzk0MjAxNjE3IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Produtividade Diária CONS - MS':'https://app.powerbi.com/view?r=eyJrIjoiZmY3MzU5OTQtMmM0Yi00MWUwLTlmMzctNzNmZWNmMWFjNDgzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Produtividade Diária CONS - MT':'https://app.powerbi.com/view?r=eyJrIjoiZjc5MWU2NzUtMjYyZi00MzQ0LWE0MjQtMjUxZDU4NzczOGE0IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Produtividade Diária - INSIDE':'https://app.powerbi.com/view?r=eyJrIjoiN2M4YWVhZjQtNzAxMy00ZGZiLThiZGMtOTA3YzA4NzhmZWJlIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Produtividade Diária - REVENDA - MS':'https://app.powerbi.com/view?r=eyJrIjoiZDVhNjgzNTEtYTI5OC00YjNhLWJiMTgtM2QyYjM0NzViMzE0IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Produtividade Diária - REVENDA - MT Norte':'https://app.powerbi.com/view?r=eyJrIjoiMzZlYzcwYzktNThjMS00OGUwLWFkNTUtNmQ0ZDIwZDcyNzc1IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'Produtividade Diária - REVENDA - MT Sul':'https://app.powerbi.com/view?r=eyJrIjoiYjVhYjYzZjctZGI3Mi00ZWI3LTgyZTUtMzljMzM3Njc5MjUzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    
    'V10094 - CON - AGRI - MS': 'https://app.powerbi.com/view?r=eyJrIjoiMTFhYTE5MGYtNGJiNi00OWM4LWJmYzItOWMxOGZiNTdiYzUyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V10094': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EkD67IqV0OdEr03LLz1sUW4BVLcvkUaKa_gXAPMRtFF-8w?e=iHrXPX',
    'V10096 - CON - AGRI - MS': 'https://app.powerbi.com/view?r=eyJrIjoiYTk5OGVjZjQtN2JkMi00YTdmLTgzOWMtMWQ3OGY2MGFiMzkxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V10096': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ErIyLJ_Vj8lFgmu9cVtRh0MBPBjsEviR0Ttkty4YYc0dAQ?e=LLpgzk',
    'V10097 - CON - AGRI - MS': 'https://app.powerbi.com/view?r=eyJrIjoiOTQ5Y2YxOWQtYzVjYS00OWEyLWE5NWMtZDUyOGMxY2MzZDBhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V10097': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsPyXkbVChxOs_enTLBLDF4BmTkQV9ZlPeffhFif9flerQ?e=7vS8PR',
    'V10113 - CON - AGRI - MS': 'https://app.powerbi.com/view?r=eyJrIjoiMTUyNTg3MTAtNmM5Mi00M2UzLWIzMTEtNWVkZjExZTJkNDkxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V10113': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsbzMMlq1gJHhIThsQDPwSABX9UJUx12MMUWVEIiuLBokw?e=9qrgqN',
    
    'V10099 - CON - MS': 'https://app.powerbi.com/view?r=eyJrIjoiZGVhZDEzNDQtMzQwOC00MDYyLWI2N2QtNDkyMmM5MjliZmRlIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V10099': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Erd_k9lYmJdDowWCNPvRlrIBps3BDtA2s-iZzAHkmtDEcA?e=8ajVRX',
    'V10111 - CON - MS': 'https://app.powerbi.com/view?r=eyJrIjoiZWQ0MDE5NzktMmM3ZC00MDM5LWEyZWUtMmRhMjBkNDExYjMyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V10111': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EheXU-iH46lDlJlx8ZqQ9m8B1r8fmcWHlXq1jJxXuziV0Q?e=hTUvuB',
    'V20048 - CON - MS': 'https://app.powerbi.com/view?r=eyJrIjoiMThjMWIzNTctODM1Ny00NzI4LWEyMTctYjFlN2YyMjZiOTY3IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V20048': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Etg47nS1nqtCrHDzekwBVq0BMitMOAfxp7IYupzMZ6yZ9Q?e=mS7LnU',
    'V20086 - CON - MS': 'https://app.powerbi.com/view?r=eyJrIjoiNGIxNzMwMmYtYjgyOC00OGZmLWFjODItMzFiM2RmMmI4OGJmIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V20086': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EvacKj79cd1KjEJXHcgGEz8B6PHo8q9pwMbZScCl2uj8Xg?e=9xdc9o',
    'V20113 - CON - MS': 'https://app.powerbi.com/view?r=eyJrIjoiNjQ4MmI3OGQtZGQzZi00ZDM5LWI3MzYtODE1OTUxNGU0Y2FjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V20113': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuzP6mPqo9JGtvtC6FL1wPcB7zBqsjAdVbMWTX6yO6XItA?e=ZKe6yL',
 
    'V20033 - CON - MT': 'https://app.powerbi.com/view?r=eyJrIjoiYmRkNjgwZWMtNzkzMy00NjFlLWI4YTMtNTNhYjEwZDA2ZGJjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V20033': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EiZW75iV3HpMof4ICXd03kcBJV4y6bcHt385GJbhFpLZ1g?e=5pmiii',
    'V20045 - CON - MT': 'https://app.powerbi.com/view?r=eyJrIjoiZWMzYjk5MTgtYTMxZS00NTBhLTlmOWYtNTczY2FiZmI1YzNjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V20045': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ErlO_rGLHoRFs3b9mZBNtGsBnndBE2BBwJkbCjYLAlkxXA?e=Di0hCr',
    'V20050 - CON - MT': 'https://app.powerbi.com/view?r=eyJrIjoiMzk4YmFhNjEtMDRjNi00YzMyLWFjODQtMTA5MjRhNzEzMWE0IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V20050': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ErDkwWM6VRJNm09gRIDYbZgBKdm_4txZPfMtbKryNME88A?e=qS70j5',
    'V20052 - CON - MT': 'https://app.powerbi.com/view?r=eyJrIjoiMGY0ZDQyM2UtZGU4My00OGUxLWFlNjYtNGI3ZGUzZGJlNzgyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V20052': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EvTwwXbK0RtFngov0SpO5A0BG8nK_aGM2IhAbjX62PbwrA?e=KhVtJB',
    'V20054 - CON - MT': 'https://app.powerbi.com/view?r=eyJrIjoiYTQzMjgzZjktN2IzMy00OTIzLTk5MGQtMDA5NzExYjNhMDBlIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V20054': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EkUEwYay18NDnCDbbW8p3mYBZIBPVT4phKZSHvu7RLrEUA?e=yCpLLy',
    'V20076 - CON - MT': 'https://app.powerbi.com/view?r=eyJrIjoiMjgwZTllMjAtYjQ0MC00ZDQ4LTk1ZGQtMDBkZjZhMTY5YTNiIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
#    'OneDrive - V20076': 'http://34.201.37.74:8000/login/',
    'V20087 - CON - MT': 'https://app.powerbi.com/view?r=eyJrIjoiZjE4NGI0NGMtNTM1Ni00ZjkxLWIwM2QtYjE5ZGU2YzdmZTg0IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V20087': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ErHAIyrd4qBMlWaCs4L45ooBxIBilplL5APQqKqxIwXfjg?e=7lDMQu',
    'V20099 - CON - MT': 'https://app.powerbi.com/view?r=eyJrIjoiNTczNjUwMDgtMmY1OC00YTM1LTliYmItZjllYmIxNTdiMDQzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V20099': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ElQgXKkqqpBAvjsrFxcfJvgB6jOHI1_F76cZ1nojDfUuQQ?e=qcRifA',
    'V20114 - CON - MT': 'https://app.powerbi.com/view?r=eyJrIjoiMmQzYTJlY2ItMWZhNS00OTE4LWEzOWUtMWRmODI2NDllM2EyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V20114': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EgFFfHbes99EgJlgVVmx08ABp8GOByUu34MIkrweq1RpoQ?e=zRU0Nd',
    
    'ASSISTENTE - CONSUMO': 'https://app.powerbi.com/view?r=eyJrIjoiZjMxNzU0NzktYjIwMy00MzYzLWI4NjAtYzk2ZGRjYjMzNTNhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - CONSUMO': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Eo46Tcxg0qZHtYAO5Y3F7koB3F9yF70tnDooNcOGHT7ViQ?e=d35j9r',
    'ASSISTENTE - REV MS': 'https://app.powerbi.com/view?r=eyJrIjoiN2I3MDVlMDUtNDg5My00NGJiLTkwN2YtODI2YmM4ZDdlZGZiIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - REV MS': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuFlaGpkDTtIg_RJdj-gBl0Bgd2zBfv55nG9W1L7n9hKyg?e=SO1Qgr',
    'ASSISTENTE - REV MT': 'https://app.powerbi.com/view?r=eyJrIjoiMGI5NjNhZjQtNDJkMS00ZDQ2LTllZTMtOTgyODk3MmY4MDhhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - REV MT': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsdC19yakbxCsVK2eFM3qj4Bhgj83ONMyPZ4zZVZAW0Z8Q?e=M86puY',
    'ISR02 - INSIDE': 'https://app.powerbi.com/view?r=eyJrIjoiMTg4MjBjZGQtMDVjYi00YzA2LThhYmQtNmY0YTU2OTU1OWEyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - ISR02': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ElkKW78BlSFEhr09HQ0GOtQBkiYXxJJhb4JXylCK6Vt1ug?e=vDk8VA',
    'ISR03 - INSIDE': 'https://app.powerbi.com/view?r=eyJrIjoiNDhlY2M1NDItZWI4OS00YTMwLWI4NzktYjBmOWE4MDRjYzgwIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - ISR03': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EgcO1UBgS2ZFqFaPmjB1KN8Bva0HRxnuLzp-h6XWAtb-eQ?e=Oasx8H',
    'ISR04 - INSIDE': 'https://app.powerbi.com/view?r=eyJrIjoiNmIwNTExOGMtMTk0ZS00ZDI2LTkyODYtNzI5NDc0N2M5NjZmIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - ISR04': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ElrD9iqYDEtKrqL4UqrDV_EBXrJGJbaAU6u_dHwB5iTc4w?e=dzU73m',
    'ISR07 - INSIDE': 'https://app.powerbi.com/view?r=eyJrIjoiN2JlNDAwZGUtYzM0Mi00YjU1LTg3NjgtNTAyODEwNDMyYmM4IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - ISR07': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsgllcZpbZ1JsgHBHF9gVr4Bt4gX7ejkdl3u9lQR5vUZCw?e=X8Mf2g',
    'ISR08 - INSIDE': 'https://app.powerbi.com/view?r=eyJrIjoiOTk1MjlhYzUtNzMxYi00ODY5LTllYjEtMTBkNjM3MGM5ZDEzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - ISR08': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EkWEf1EHmyFAhJd0_fF4DlEBo9OHGof1HtuqVArXMm-I3Q?e=x0LA3u',

  
    'R10001 - REV - MS': 'https://app.powerbi.com/view?r=eyJrIjoiZjg5YjZmOGMtMmZjNi00NTkyLWJiNzUtMzAwZjU5NGU3MWNkIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R10001': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EkMh3Oi0OdNEqJz3p8DrPcgBK23QSG4N7Hs8fhm5aq-0fQ?e=8S8Swj',
    'R10002 - REV - MS': 'https://app.powerbi.com/view?r=eyJrIjoiMmFhZTBiNmQtNTYxMS00NTQ0LWE1ZmQtOTk0YzcxOGEyM2MxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R10002': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EnluWqlKR39OpfUVDxVtw8cBibD0LtNtNiM2eKAcjfz-5g?e=hayzcg',
    'R10004 - REV - MS': 'https://app.powerbi.com/view?r=eyJrIjoiYjg3NjcwMjEtODg2Mi00M2MyLTgzMGUtNTcxMWVmMjMyZTUxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R10004': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EnAd-sIoj6dOlRACCc5SC3QBgln1GKmOhu09tzwJ85n2OQ?e=fZgrbY',
    'R10005 - REV - MS': 'https://app.powerbi.com/view?r=eyJrIjoiZjk1YzQ0NzItMTQwMi00NDQxLWE4NTktMjFlODU4ZWUwYTlkIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R10005': ' https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Enk0Erdw7RtInSYNr0gImFUBMfPaJ6Vf4vVG_ro45Y-ZAA?e=5OmACa',
    'R10006 - REV - MS': 'https://app.powerbi.com/view?r=eyJrIjoiNTNjYmE3NDItNjA4Mi00ZGE3LWFjYzQtZTYyMTJjMWM2OGE4IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R10006': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EthcrSt_zI9PrDAFwfS_7LQBHH-W8OAaXEPIpGHEfEUI0A?e=hIaVIQ',
    'R10007 - REV - MS': 'https://app.powerbi.com/view?r=eyJrIjoiMTVjOWNjZGUtMDExNC00ODJhLTk1NjEtZjlkYWVmZjM1YjhiIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R10007': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ElAhsT9mlylLr4EmpcHiwh8B08XCXNZc0uiEUjDDWtBxgw?e=nNd8ts',
    'R10008 - REV - MS': 'https://app.powerbi.com/view?r=eyJrIjoiNDg0MGE3ZjctMWU4NS00ZGQ1LThiN2UtNDdlMjg5ZGIwNjBkIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R10008': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EmBMR65N8lNDoBLO5YZp5X4B4Od22y3TKXx76GohJJyCRQ?e=yu5skA',
    'R10010 - REV - MS': 'https://app.powerbi.com/view?r=eyJrIjoiMjYxNjRhNjktNGUyZC00MDU0LWJmNjUtM2M1ZTVjMjliMzNhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R10010': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ej6W9_81pphBpBjz4UqdKWcBuEZ2nDE-6NyXlwAhmyvfZQ?e=Hsm8IZ',
    'V10098 - REV - MS': 'https://app.powerbi.com/view?r=eyJrIjoiOTNkN2YxZWMtZTM2MS00Yzc2LTliNGEtN2JmY2VhMDFjYWQyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V10098': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ej6W9_81pphBpBjz4UqdKWcBuEZ2nDE-6NyXlwAhmyvfZQ?e=Hsm8IZ',
    'V10112 - REV - MS': 'https://app.powerbi.com/view?r=eyJrIjoiZDU2MmVjZWEtYThkOS00YWJlLWE1ODUtOTY1NWE1NDM3Yjk4IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - V10112': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuyJp5oQYEJGrw4fH-i-dGEB-HB1BFdsKbkBF-yg6zhKQA?e=1WOuVt',
    'R10001 - Cliente Sem Compra': 'https://app.powerbi.com/view?r=eyJrIjoiYmFmOTY0ZWUtMDZjNC00ZTEyLTkxMTItYWJlNzdhZDA4OGZjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'R10004 - Cliente Sem Compra': 'https://app.powerbi.com/view?r=eyJrIjoiYmY4ZjJmOWItMzY4ZC00OTRjLWE0NjQtNDU5NjI5MzgxMjdiIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'R10008 - Cliente Sem Compra': 'https://app.powerbi.com/view?r=eyJrIjoiODFjZGJkYTEtNjRmZS00Yzk4LWFjYzItODYzNDQwMDMxMzliIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',


    'R20005 - REV - MT': 'https://app.powerbi.com/view?r=eyJrIjoiMjU3YTAwMzAtNWY2OC00MjE3LTlkODQtOTBlYmI0NGM1MzQ0IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R20005': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuWu-RP9Hv9OorYpaKhgF4IBxW2cownGJUD_lR_RPMfcPQ?e=xpTC8P',
    'R20009 - REV - MT': 'https://app.powerbi.com/view?r=eyJrIjoiMjUzYTU3YWMtNmE1ZC00OWVhLTgyNzItMmM5OTY5OWY5ODk4IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R20009': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EnUUqka05eRPhW4MEG8bHVYB_EGBc3I8vjm2Gv-V9XDT5w?e=RDzhpw',
    'R20010 - REV - MT': 'https://app.powerbi.com/view?r=eyJrIjoiYjYyZDYyYzUtOWQ3Yi00MzBiLWE3ZmQtOWQ5Y2JiY2RjMWYyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R20010': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EliQPazGsAdAn5RhVxmC5joBGluzCJco1aG3Iy2XRE-xoA?e=whDMDj',
    'R20011 - REV - MT': 'https://app.powerbi.com/view?r=eyJrIjoiMmRlNWJhMDgtYjA4ZC00Mzg1LThmZmUtY2I1MWJlOTU4YmUwIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R20011': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Et1wCwDeceNDqCphdZHDbwwBGwiLiE5aLTQyqD81KtpS1w?e=cc82VL',
    'R20014 - REV - MT': 'https://app.powerbi.com/view?r=eyJrIjoiY2VjOWRiYzctNzY2NC00OGVlLTk2MDktZDFhYjc2Mjc4MzQ1IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R20014': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ek5XdS-uvFhGmU_l7v4zNIIBgzancotPv1A4NDQ9OeAwyA?e=ZheoJo',
    'R20039 - REV - MT': 'https://app.powerbi.com/view?r=eyJrIjoiMWVmMzYwYmYtOTdhMy00NzRmLWI5ODQtYzE2NGVkZGVhMGFlIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R20039': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ElGuJWEjmXpLlwF-qrXOif8BYR0v5byIBG_F5IUQUFwNJw?e=NoQqPu',    
   
    'R20001 - REV - MT': 'https://app.powerbi.com/view?r=eyJrIjoiZDQ5YmU4NDQtNTE3YS00M2ViLWE4MjMtZDI4N2ZhZmRlMjVlIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R20001': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EgzzGixFt-hBiSLhdxnty-YB0mYRpCFH4P3JsOlJsrXjWA?e=6fPewa',
    'R20003 - REV - MT': 'https://app.powerbi.com/view?r=eyJrIjoiNWUyYWJiOGQtNDJkNi00ODM0LWFlMzQtOTM0NWQzMWZkOGVjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R20003': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EpMs_G202JlEoUu6i2e8gL4Bo_XFV62pfgujDSurxfWotg?e=gkMskT',
    'R20006 - REV - MT': 'https://app.powerbi.com/view?r=eyJrIjoiNGIzNTUyYTItNmNjMC00ZmU1LThjZmUtNDI3YTk5MmZlNjZiIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R20006': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/En2UBW0CmJdKmH15I22cGoUB0Qyb9LWb1KVmTxkmco621g?e=Rgdo8k',
    'R20008 - REV - MT': 'https://app.powerbi.com/view?r=eyJrIjoiMmJiYTAxZTUtM2Y3MS00YTVhLWI2MjUtYzczMzk3ZjEwOWNjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R20008': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuyeW0hHebdEmZiS32CAP-wBpbwYqgdOM6dw8kZmUgNusw?e=fsgbCi',
    'R20012 - REV - MT': 'https://app.powerbi.com/view?r=eyJrIjoiOTU1NGNiNjYtMGE1NC00YWRkLTg4ZDQtMzg5YTdlMDdhYjY0IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R20012': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EvIWf2A3tg5NprlBWt63CNEBnpyCUdR7s1jgj9Z1MrFw8A?e=tXmurI',
    'R20015 - REV - MT': 'https://app.powerbi.com/view?r=eyJrIjoiNTNmZTM1M2ItNjliZS00ZWNlLTg1OWQtZDQzMWU2M2RmNjAwIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
    'OneDrive - R20015': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EvCgjCAlsWpLgPbtVRorJsUB9uutEbrbJo3FkhdqHZIFSw?e=iqKu1o',  
    
}

def verificar_credenciais(usuario, senha):
    try:
        user = Usuario.objects.get(usuario=usuario, senha=senha)
        if user.acesso:
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
            request.session.set_expiry(14400)  # Expira a sessão em 4 horas

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
    if not request.session.get('usuario'):  # Verifica se a sessão ainda é válida
        return redirect('login')

    usuario = request.session['usuario']
    relatorios = request.session.get('relatorios', [])
    relatorios_disponiveis = [{'nome': r, 'url': relatorios_urls.get(r, '#')} for r in relatorios]

    # Obter o relatório selecionado
    relatorio_nome = request.GET.get('relatorio')
    relatorio_selecionado = relatorios_urls.get(relatorio_nome) if relatorio_nome in relatorios else None

    return render(request, 'relatorios.html', {
        'relatorios': relatorios_disponiveis,
        'relatorio_selecionado': relatorio_selecionado,
        'usuario': usuario,  # Adiciona o nome do usuário ao contexto
    })

def logout_view(request):
    logout(request)
    return redirect('login')
