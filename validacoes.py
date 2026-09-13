# validacoes.py
import re

def validar_cpf(cpf):
    """Valida CPF de acordo com as regras da Receita Federal"""
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    def calcular_digito(cpf, peso):
        soma = sum(int(n) * (peso + 1 - i) for i, n in enumerate(cpf[:peso]))
        return 0 if (resto := soma % 11) < 2 else 11 - resto
    
    digito1 = calcular_digito(cpf, 9)
    digito2 = calcular_digito(cpf, 10)
    
    return cpf[-2:] == f"{digito1}{digito2}"

def formatar_cpf(cpf):
    """Formata CPF no padrão XXX.XXX.XXX-XX"""
    cpf_limpo = re.sub(r'[^0-9]', '', cpf)
    return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:11]}"
