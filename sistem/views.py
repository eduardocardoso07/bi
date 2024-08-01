# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Usuario, Acesso
import logging

logger = logging.getLogger(__name__)

relatorios_urls = {
'Acompanhamento Gerentes': 'https://app.powerbi.com/view?r=eyJrIjoiYmZlNmNlZjYtZmNhZS00MDE4LTliMWQtYmExNWQ4NGZlZTlkIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Acompanhamento Gerentes - Consumo': 'https://app.powerbi.com/view?r=eyJrIjoiNTE0ZWQ5MjYtNWIwZC00MWZmLWIzYTgtZjcyNzdkNGE5NWRjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Acompanhamento Gerentes - Revenda': 'https://app.powerbi.com/view?r=eyJrIjoiOTczMjM5MDYtODhiZC00OTcyLWFlNWYtMjFjNzJhMDg4ZjA5IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',

'Acompanhamento Diario': 'https://app.powerbi.com/view?r=eyJrIjoiNGE3MWQ5NjgtMzc1Ny00MGZmLWEzMDMtYTU1MTNmMzUwZDMxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Acompanhamento Diario - Consumo': 'https://app.powerbi.com/view?r=eyJrIjoiYjQ0NDY4OWMtMDM5YS00MGYzLTg1ZjAtMWE2YzM0ZWE1NTFhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Acompanhamento Diario - Revenda': 'https://app.powerbi.com/view?r=eyJrIjoiMGFkMjkzNTktMzEzYS00ZTJjLThmZTctMTE2MDMyOGJkNzJhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Acompanhamento Diario - REVENDA - MT Norte': 'https://app.powerbi.com/view?r=eyJrIjoiZDRkMmVmZjktNDkxMC00OGI0LTllNmMtOGU1NmY0NjY1NDc1IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Acompanhamento Diario - REVENDA - MS': 'https://app.powerbi.com/view?r=eyJrIjoiOGI5YzQyMTAtOTgxMy00NWExLTg5ZmEtNmE5NjlhOWRlOTRmIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Acompanhamento Diario - REVENDA - MT Sul': 'https://app.powerbi.com/view?r=eyJrIjoiYjkzZThkZDgtYzA2NC00N2E4LTk4N2ItMjBkYTVlNjBlY2E2IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Acompanhamento Diario - CONSUMO - MS': 'https://app.powerbi.com/view?r=eyJrIjoiNzBiYTAwMDgtMzI5OS00NzZjLWExN2UtZjE3NDJjMjhlMjdlIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Acompanhamento Diario - CONSUMO - MT': 'https://app.powerbi.com/view?r=eyJrIjoiZTM0NWY3YmUtZmMyZS00OTIwLWJhZmQtNTAwMzc4MTdlYzZmIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Acompanhamento Diario - CONSUMO AGRI - MS': 'https://app.powerbi.com/view?r=eyJrIjoiNzRiZTQ3OGItY2M5ZS00NGE5LTgzYzEtMmNlNjRkMmQ0NTBkIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Acompanhamento Diario - INSIDE':"https://app.powerbi.com/view?r=eyJrIjoiY2VkZWM2OTItMDhkOC00MDA5LTk0ZTctMGVjZjQyMjYxNmU4IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9",

'DAP KPI - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiZjI1NGY3NTktYTllMC00OGFmLThmYzctYjk5NGU1MWI4YzA0IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'DAP KPI Consumo - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiODU5OTZhODItY2NiYS00YmQ3LWJjNzgtMjI1YzEzY2MxZjE5IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'DAP KPI Revenda - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiMTE5NGVmOWItZDU5MS00NzRhLTkyNWQtYWM3Y2M3MDljMDJjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'DAP KPI Revenda MS - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiZDlkYjI2MTItYWU2Ni00MTRhLTllOGUtMjNlMjRiMmU0YTdhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'DAP KPI Revenda MT Norte - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiZTAxNDg5OTEtOTk3ZC00OGVkLTg0MWQtNjlmNWYxMjk1NzllIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'DAP KPI Revenda MT Sul - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiOTNiMjg1MTgtNTgyNC00MDQ2LThmNmQtZDhjYmQyNDg2ZWU3IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'DAP KPI Consumo Agri MS - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiYjRjYmM4OTYtZTk2NS00MDU3LTk5NzItMjVhMjBkYTFmZWE3IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'DAP KPI Consumo MS - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiNzY3MDc3YWYtMGQyNy00ZmYyLWFlZTYtZjUzM2I4N2Y4YWY5IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'DAP KPI Consumo MT - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiZThmNDE4ZjAtODRlNS00MmNlLTgzODYtNmI5OThjODI4NjQ4IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'DAP KPI Inside Sales - Mensal': 'https://app.powerbi.com/view?r=eyJrIjoiYTYzMGIzMTItYTllZC00ODhmLWIwNTEtYTliNzBhM2NlY2YyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',

'Performance CO': 'https://app.powerbi.com/view?r=eyJrIjoiODRmZDQ2ZjQtZTdkMS00ZDI3LWE4NzQtZjMyMWI0NGUzMzZmIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Performance Gerente Revenda':'https://app.powerbi.com/view?r=eyJrIjoiMDIxNDNmMmMtOTQ2ZC00OTYxLTgyZjEtZDJiMGI4ZTgzMzYxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Performance Gerente Consumo':'https://app.powerbi.com/view?r=eyJrIjoiZDRkMGY1ZDktMTgzMy00MTJiLThlZDYtNDRjZjQxOGMwYWYxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Performance Coordenador -CONSUMO AGRI - MS': 'https://app.powerbi.com/view?r=eyJrIjoiNjE4YzUwNGMtMzFjZi00Mzk5LTkwNGItODA2NTU4MDI1NThhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Performance Coordenador - REVENDA - MS':'https://app.powerbi.com/view?r=eyJrIjoiNWUxNjFkZWQtNTE4MS00NjgwLWJjMGYtNTcyMzY5NGIxMTg1IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Performance Coordenador - CONSUMO - MS':'https://app.powerbi.com/view?r=eyJrIjoiMjI1YTU3MTEtYzQ1NS00ZWIwLThmM2YtZTAzYWUyMTI2ODM5IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Performance Coordenador - REVENDA - MT Norte':'https://app.powerbi.com/view?r=eyJrIjoiYzRjYjY2ZDMtZTQ0MC00Yjk4LTllZWItMjlkZmExZjFlMTIyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Performance Coordenador - REVENDA - MT Sul':'https://app.powerbi.com/view?r=eyJrIjoiMWQyMzhiOGUtOWVmNy00ZWQzLTlkMGUtMmE2MDBhOTllODA3IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Performance Coordenador - CONSUMO - MT': 'https://app.powerbi.com/view?r=eyJrIjoiYmVhMWMxODgtZTQ2ZC00ZjNlLTg5Y2EtZWJiNDA3OWFlNjMzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'Performance Coordenador - INSIDE': 'https://app.powerbi.com/view?r=eyJrIjoiNDM1YTczMTEtNGVlZS00MGVkLTkzN2YtNTBlMTJhODZlN2RjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',

'ISR02 - INSIDE':'https://app.powerbi.com/view?r=eyJrIjoiNGQwOWFhOGEtNDc2NS00YzRmLTgwYjgtZjYwYmY4MTZlZDZiIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'ISR03 - INSIDE':'https://app.powerbi.com/view?r=eyJrIjoiZDMxZjM2ZDktNDBkZC00NjM5LTk4MjctMzVjMDY4MzZmYjU3IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'ISR04 - INSIDE':'https://app.powerbi.com/view?r=eyJrIjoiYmUxNzA1ZTYtODkyNC00ZDk0LTg3MjItNDBiNTVlOWVmMmZiIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'ISR07 - INSIDE':'https://app.powerbi.com/view?r=eyJrIjoiYmRlMzMzODktMTBmNy00ZDRjLTk2MzctYTEzYWIyODZkMGVhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'ISR08 - INSIDE':'https://app.powerbi.com/view?r=eyJrIjoiZTkyMmQ4NGMtMjQ0ZS00NTgyLTgyNTctMDI0Y2I1YzQwYjA4IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',

'ASSISTENTE - CONSUMO':'https://app.powerbi.com/view?r=eyJrIjoiYTc1MGIzNGUtMzg3NC00ZDU3LWIyY2QtOGE2MmMzNjdiODVjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'ASSISTENTE - REV MS':'https://app.powerbi.com/view?r=eyJrIjoiNDY5MjdjMDQtZmVkMi00NmEyLWEwYjQtNjY5NjMwOGQyZTAzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'ASSISTENTE - REV MT':'https://app.powerbi.com/view?r=eyJrIjoiNzBlNWIyYzktNmM3Yi00YWI0LWFiOTAtNmE3NjBiYTY5NTgxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',

'V10097 - CON - AGRI - MS':'https://app.powerbi.com/view?r=eyJrIjoiNGJkZDdlYTEtYzU0Yy00OTM0LWEyNzUtMTI0ZDVhZGU3OTUzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V10113 - CON - AGRI - MS':'https://app.powerbi.com/view?r=eyJrIjoiNjk0NTFmNTAtMjU1NC00Njk3LTljZGYtNjQ1NDQ4ZjA2MTc0IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V10094 - CON - AGRI - MS':'https://app.powerbi.com/view?r=eyJrIjoiNjNjYTI1NTAtMWI3MC00OWY3LWIwZmQtODE2YTJjNjhkMzIzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V10096 - CON - AGRI - MS':'https://app.powerbi.com/view?r=eyJrIjoiYzJiMTY4Y2YtY2E1OS00MzI0LTgxNWMtNWRjYjYyNDMwZDAyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',

'R20001 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiZjFhYjU0YmQtN2Q4OS00NzMwLTk3ZDktZDA0NjEwNjMyOWViIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R20008 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiMjE1NzVkNzYtYjRjYS00OWNmLWE3MjAtYTVhZmU1MTYxMzRjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R20015 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiYjRjZmQzNWMtNjg4OC00ZmQ1LWJiMGMtNWZlN2M3OTdiZjc3IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R20002 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiOTk2OTc2NzQtZWZjYy00YWZmLWJmYWYtNmE5MDQwYWJjNjQ5IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R20012 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiZWRmMWE5ZTEtOWJhYi00Y2E3LTlhOWEtMzJjZmFjN2YxMjhlIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R20006 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiNDQ3ZjE5M2YtOTNhMy00YjE3LWI3YTEtZGVkNGI2YWZjODI0IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R20003 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiODYzODM3N2QtMDMyNy00MWUyLWJiNzEtYTlhN2NiMDg2NmNhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',

'V10111 - CON - MS':'https://app.powerbi.com/view?r=eyJrIjoiN2YyMWEwM2EtMGFiMS00MzI1LWExMjctMzFhZTE5NzZmNTg4IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V20113 - CON - MS':'https://app.powerbi.com/view?r=eyJrIjoiNjg0NjdiYmUtMzYzNi00Nzc0LWI0ZmQtYThlNDJmNjFjNjljIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V20048 - CON - MS':'https://app.powerbi.com/view?r=eyJrIjoiYjUwNWY1ZTYtMzUyNi00Yzk3LTg1ODctYmJmNTQ3ZTViZjA4IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V20086 - CON - MS':'https://app.powerbi.com/view?r=eyJrIjoiYTljNjE4NTctOTE2OS00OWFkLThiOTItZGNkZjA0NWRjNThlIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V10099 - CON - MS':'https://app.powerbi.com/view?r=eyJrIjoiYmFiNzgyMTktOTk4OS00MGMzLThlMGItMDdkMGRhNTQxMjgwIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',

'R20011 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiMzgyNzdhMmUtMjdhMC00OWFjLWI2ZGMtOTVlMWY5YmRhYzIwIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R20010 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiOWY5NjViNzUtY2RkOS00OTA2LTgyYWMtMzk2OTFmZTg1ZjRhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R20014 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiMTM1N2JiMDEtNjlmOC00YWVmLWIxMjAtMTM0OGNlNmI3M2QzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R20005 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiMjJkNDIzM2MtNmM0Ny00ZmRiLWExNWItMjRjOTc4NGNiYWUzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R20009 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiMmFhNjAzY2QtZjE4ZS00YTI0LTg4MjgtMWViOWM2NGRkNGU2IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',

'V20099 - CON - MT':'https://app.powerbi.com/view?r=eyJrIjoiZmZiYWIwMTctNGM1Yy00YjhhLTk4YTMtOTNhY2U4OTlhYjE4IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V20114 - CON - MT':'https://app.powerbi.com/view?r=eyJrIjoiZjkzMzdkZDktMTA4Zi00NTgzLTg5YjItYjI5YTRhNDRjY2RlIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V20033 - CON - MT':'https://app.powerbi.com/view?r=eyJrIjoiMGY2NjIxMjctMmIzZi00YjFjLWI3MWMtZDdkNjliNTFjZDUzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V20054 - CON - MT':'https://app.powerbi.com/view?r=eyJrIjoiZWJhYTdlYTQtZjFlYy00NmVlLWIxMmUtMGZkMGQ0MTRlNTVjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V20076 - CON - MT':'https://app.powerbi.com/view?r=eyJrIjoiMmIzMTc3YmUtZjcyMy00N2ZjLTkzOWQtZjRlZTIyODU0NWUwIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V20045 - CON - MT':'https://app.powerbi.com/view?r=eyJrIjoiNjc5ZDJhYjUtNTM4MC00Mjg2LWJkYWItYmI4NmIwZTQ4MzFkIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V20052 - CON - MT':'https://app.powerbi.com/view?r=eyJrIjoiNmVhYTcwNWUtODlmZC00Yjc1LWExZGYtNGFmNTY5MmM4YjQ4IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V20050 - CON - MT':'https://app.powerbi.com/view?r=eyJrIjoiYmI5OTZjMGEtODVkNy00NDhkLWI4ODctNzNkZjY2ZjQ3MTdjIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V20087 - CON - MT':'https://app.powerbi.com/view?r=eyJrIjoiZTgxZjBmODMtYzEyZC00OWZlLWExZjgtZjYzNDEzYTFiNGUwIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',

'R10007 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiYjA4ZmMxY2UtZTc2Zi00Mzk4LWI5ZmQtNmE4YTQ3YWM0M2U4IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V10112 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiMzM2NTNmNDktZjk3OC00ZjJlLTk1MmEtMzQ1ZjMwMWU1OTQzIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'ESP101 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiZjg0YTcwZjctYmJhOS00MWVjLWEwM2YtYWMwMDQ1OGQ4MjdkIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R10010 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiODQ4ZTIwMTEtZjg2NS00YzYwLThjNjctMWMzOWIyNWQxYzYyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R10001 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiMjdhMGJmNDctMTA4MS00YzFhLWEyYmQtNmZkNWIwY2Y3OGUyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R10002 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiYzE3OTBiYzMtOTkwOS00YzE0LTljMTItZTdjZTRkNzM0OGJlIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'V10098 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiZDI4MjE0YjAtNWNiYS00YWIxLTgxZjktMTQxYzljZjM3ODA5IiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R10008 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiMTBmMmNkZDMtNDQyNC00NzQ4LWI0MTUtMmFhMjc0YzM3MDUyIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R10004 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiZjYyMzMwYWUtOWYxNS00YjU1LWFhMGUtN2UyNGI4MmI2MTEwIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R10005 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiYjUyYWVmYTgtOWE3MC00N2ExLWIxNTMtNGRjMWU4MGIzZWZhIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',
'R10006 - REV - MS':'https://app.powerbi.com/view?r=eyJrIjoiNzE2ZGM2ZjctODNjMS00MGUyLTg3M2UtMmIyMmUzYTBjZjYxIiwidCI6ImFjN2Q4YTcyLTBhOGItNDRjZS05NmZjLTdkMWFhMGVjZmMzMSJ9',

'OneDrive - ISR02':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ElkKW78BlSFEhr09HQ0GOtQBkiYXxJJhb4JXylCK6Vt1ug?e=vDk8VA',
'OneDrive - ISR03':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EgcO1UBgS2ZFqFaPmjB1KN8Bva0HRxnuLzp-h6XWAtb-eQ?e=Oasx8H',
'OneDrive - ISR04':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ElrD9iqYDEtKrqL4UqrDV_EBXrJGJbaAU6u_dHwB5iTc4w?e=dzU73m',
'OneDrive - ISR07':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsgllcZpbZ1JsgHBHF9gVr4Bt4gX7ejkdl3u9lQR5vUZCw?e=X8Mf2g',
'OneDrive - ISR08':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EkWEf1EHmyFAhJd0_fF4DlEBo9OHGof1HtuqVArXMm-I3Q?e=x0LA3u',
'OneDrive - REV MT':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsdC19yakbxCsVK2eFM3qj4Bhgj83ONMyPZ4zZVZAW0Z8Q?e=M86puY',
'OneDrive - REV MS':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuFlaGpkDTtIg_RJdj-gBl0Bgd2zBfv55nG9W1L7n9hKyg?e=SO1Qgr',
'OneDrive - CONSUMO':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Eo46Tcxg0qZHtYAO5Y3F7koB3F9yF70tnDooNcOGHT7ViQ?e=d35j9r',
'OneDrive - V10097':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsPyXkbVChxOs_enTLBLDF4BmTkQV9ZlPeffhFif9flerQ?e=7vS8PR',
'OneDrive - V10113':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsbzMMlq1gJHhIThsQDPwSABX9UJUx12MMUWVEIiuLBokw?e=CUAupe',
'OneDrive - V10094':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EkD67IqV0OdEr03LLz1sUW4BVLcvkUaKa_gXAPMRtFF-8w?e=iHrXPX',
'OneDrive - V10096':'',
'OneDrive - R20001':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EgzzGixFt-hBiSLhdxnty-YB0mYRpCFH4P3JsOlJsrXjWA?e=6fPewa',
'OneDrive - R20008':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuyeW0hHebdEmZiS32CAP-wBpbwYqgdOM6dw8kZmUgNusw?e=fsgbCi',
'OneDrive - R20015':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EvCgjCAlsWpLgPbtVRorJsUB9uutEbrbJo3FkhdqHZIFSw?e=iqKu1o',
'OneDrive - R20002':'',
'OneDrive - R20012':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EvIWf2A3tg5NprlBWt63CNEBnpyCUdR7s1jgj9Z1MrFw8A?e=tXmurI',
'OneDrive - R20006':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/En2UBW0CmJdKmH15I22cGoUB0Qyb9LWb1KVmTxkmco621g?e=Rgdo8k',
'OneDrive - R20003':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EpMs_G202JlEoUu6i2e8gL4Bo_XFV62pfgujDSurxfWotg?e=gkMskT',
'OneDrive - V10111':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EheXU-iH46lDlJlx8ZqQ9m8B1r8fmcWHlXq1jJxXuziV0Q?e=hTUvuB',
'OneDrive - V20113':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuzP6mPqo9JGtvtC6FL1wPcB7zBqsjAdVbMWTX6yO6XItA?e=ZKe6yL',
'OneDrive - V20048':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Etg47nS1nqtCrHDzekwBVq0BMitMOAfxp7IYupzMZ6yZ9Q?e=mS7LnU',
'OneDrive - V20086':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EvacKj79cd1KjEJXHcgGEz8B6PHo8q9pwMbZScCl2uj8Xg?e=9xdc9o',
'OneDrive - V10099':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Erd_k9lYmJdDowWCNPvRlrIBps3BDtA2s-iZzAHkmtDEcA?e=8ajVRX',
'OneDrive - R20011':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Et1wCwDeceNDqCphdZHDbwwBGwiLiE5aLTQyqD81KtpS1w?e=cc82VL',
'OneDrive - R20010':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EliQPazGsAdAn5RhVxmC5joBGluzCJco1aG3Iy2XRE-xoA?e=whDMDj',
'OneDrive - R20014':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ek5XdS-uvFhGmU_l7v4zNIIBgzancotPv1A4NDQ9OeAwyA?e=ZheoJo',
'OneDrive - R20005':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuWu-RP9Hv9OorYpaKhgF4IBxW2cownGJUD_lR_RPMfcPQ?e=xpTC8P',
'OneDrive - R20009':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EnUUqka05eRPhW4MEG8bHVYB_EGBc3I8vjm2Gv-V9XDT5w?e=RDzhpw',
'OneDrive - V20099':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ElQgXKkqqpBAvjsrFxcfJvgB6jOHI1_F76cZ1nojDfUuQQ?e=H9G8vl',
'OneDrive - V20114':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EgFFfHbes99EgJlgVVmx08ABp8GOByUu34MIkrweq1RpoQ?e=zRU0Nd',
'OneDrive - V20033':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EiZW75iV3HpMof4ICXd03kcBJV4y6bcHt385GJbhFpLZ1g?e=5pmiii',
'OneDrive - V20054':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EkUEwYay18NDnCDbbW8p3mYBZIBPVT4phKZSHvu7RLrEUA?e=yCpLLy',
'OneDrive - V20076':'',
'OneDrive - V20045':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ErlO_rGLHoRFs3b9mZBNtGsBnndBE2BBwJkbCjYLAlkxXA?e=Di0hCr',
'OneDrive - V20052':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EvTwwXbK0RtFngov0SpO5A0BG8nK_aGM2IhAbjX62PbwrA?e=KhVtJB',
'OneDrive - V20050':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ErDkwWM6VRJNm09gRIDYbZgBKdm_4txZPfMtbKryNME88A?e=qS70j5',
'OneDrive - V20087':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ErHAIyrd4qBMlWaCs4L45ooBxIBilplL5APQqKqxIwXfjg?e=7lDMQu',
'OneDrive - R10007':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ElAhsT9mlylLr4EmpcHiwh8B08XCXNZc0uiEUjDDWtBxgw?e=nNd8ts',
'OneDrive - V10112':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuyJp5oQYEJGrw4fH-i-dGEB-HB1BFdsKbkBF-yg6zhKQA?e=1WOuVt',
'OneDrive - ESP101':'',
'OneDrive - R10010':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ej6W9_81pphBpBjz4UqdKWcBuEZ2nDE-6NyXlwAhmyvfZQ?e=Hsm8IZ',
'OneDrive - R10001':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EkMh3Oi0OdNEqJz3p8DrPcgBK23QSG4N7Hs8fhm5aq-0fQ?e=8S8Swj',
'OneDrive - R10002':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EnluWqlKR39OpfUVDxVtw8cBibD0LtNtNiM2eKAcjfz-5g?e=hayzcg',
'OneDrive - V10098':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ej6W9_81pphBpBjz4UqdKWcBuEZ2nDE-6NyXlwAhmyvfZQ?e=Hsm8IZ',
'OneDrive - R10008':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EmBMR65N8lNDoBLO5YZp5X4B4Od22y3TKXx76GohJJyCRQ?e=yu5skA',
'OneDrive - R10004':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EnAd-sIoj6dOlRACCc5SC3QBgln1GKmOhu09tzwJ85n2OQ?e=fZgrbY',
'OneDrive - R10005': 'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Enk0Erdw7RtInSYNr0gImFUBMfPaJ6Vf4vVG_ro45Y-ZAA?e=5OmACa',
'OneDrive - R10006':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EthcrSt_zI9PrDAFwfS_7LQBHH-W8OAaXEPIpGHEfEUI0A?e=hIaVIQ',

'OneDrive - Business Intelligence':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ein-hXyOGLFCh-FVwHmmHucBVpWVBOoGh5nSMg4w_g2j7w?e=BnvepW',
'OneDrive - Diretor e Gerente Geral':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ein-hXyOGLFCh-FVwHmmHucBVpWVBOoGh5nSMg4w_g2j7w?e=VBBIZH',
'OneDrive - Diretor e Gerente Geral':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Ein-hXyOGLFCh-FVwHmmHucBVpWVBOoGh5nSMg4w_g2j7w?e=VBBIZH',
'One Drive Gerente Consumo':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Euf-04YEZqxIrNmm3nL6yMQBr_bS2sKZ8VCP6rxbThErVQ',
'OneDrive - COORD CONSUMO - MT':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/En408h0ED8hMkcdiZP-6xMEBwOj8w-kEtdyIcfmnQWbztg?e=oYDgba',
'OneDrive - COORD CONSUMO - MS':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EsV1cc3j85hCv2YOtlOqftoBRAqXSJ2waNgAUK2gd1VcEA?e=7zG7r8',
'OneDrive Gerente Revenda':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/ErVC3-SlUBBEu_HbSujA6i0BASo3cHxFps8p3YdD8-erwA',
'OneDrive - COORD REVENDA - MS':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Enjok5klGqpEjKVFGhazJbgBrfcf7bNAcUunO6MVdgNajA?e=j0zX5y',
'OneDrive - COORD REVENDA - MT Sul':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EggYms1nftdPpnzoAsmMI28BJcXreG9CnoAXctcAIj-IKQ',
'OneDrive - COORD REVENDA - MT Norte':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/EuAddOfY2c5DmoW80Gr4rrcBocXpRhF4xQSP2RkHFrut8A?e=Fh4rjE',
'OneDrive - INSIDE':'https://colubrificantes-my.sharepoint.com/:f:/g/personal/sabrina_manzoli_colubrificantes_com_br/Eh10RGR4UMpLhi-KtcA6xh0B-20RwZMoCZK5TOn6OP5gjQ?e=HF5GPt',
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
        manter_conectado = 'manter_conectado' in request.POST

        relatorios, acesso_liberado = verificar_credenciais(usuario, senha)
        if acesso_liberado:
            request.session['usuario'] = usuario
            request.session['relatorios'] = relatorios
            if manter_conectado:
                request.session.set_expiry(0)

            # Registrar o último login e o acesso
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

@login_required
def relatorios_view(request):
    usuario = request.session['usuario']
    relatorios = request.session.get('relatorios', [])
    relatorios_disponiveis = [{'nome': r, 'url': relatorios_urls.get(r, '#')} for r in relatorios]

    for relatorio in relatorios:
        logger.info(f'Usuário {usuario} acessou o relatório {relatorio} em {timezone.now()}')

    # Adicionar o link do OneDrive
    user_obj = Usuario.objects.get(usuario=usuario)
    onedrive_link = user_obj.onedrive_link

    return render(request, 'relatorios.html', {'relatorios': relatorios_disponiveis, 'onedrive_link': onedrive_link})

def logout_view(request):
    logout(request)
    return redirect('login')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            usuario = Usuario.objects.get(usuario=username)
            usuario.last_login = timezone.now()
            usuario.save()

            Acesso.objects.create(
                usuario=usuario,
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            ...
    else:
        return render(request, 'login.html')