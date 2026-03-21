from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI(
    title="API de Validação de CPF",
    description="Valida CPFs brasileiros com base nos dígitos verificadores.",
    version="1.0.0",
)


class CPFRequest(BaseModel):
    cpf: str

    @field_validator("cpf")
    @classmethod
    def cpf_deve_ter_digitos_suficientes(cls, v: str) -> str:
        limpo = ''.join(filter(str.isdigit, v))
        if len(limpo) != 11:
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos.")
        return v


class CPFResponse(BaseModel):
    cpf_sem_formatacao: str
    cpf_formatado: str
    valido: bool


def formatar_cpf(cpf: str) -> str:
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def validar_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))

    # Rejeita CPFs com todos os dígitos iguais
    if cpf == cpf[0] * 11:
        return False

    # Validação do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10

    # Validação do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10

    return cpf[-2:] == f"{digito1}{digito2}"


@app.post("/cpf/validar", response_model=CPFResponse, summary="Valida um CPF")
def validar(data: CPFRequest):
    
    cpf_limpo = ''.join(filter(str.isdigit, data.cpf))
    return CPFResponse(
        cpf_sem_formatacao=data.cpf,
        cpf_formatado=formatar_cpf(cpf_limpo),
        valido=validar_cpf(data.cpf),
    )