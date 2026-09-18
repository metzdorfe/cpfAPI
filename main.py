import random

from fastapi import FastAPI
from pydantic import BaseModel, field_validator

app = FastAPI(
    title="API de Validação de CPF",
    description="Valida CPFs brasileiros com base nos dígitos verificadores.",
    version="1.0.0",
)


class CPF:
    #Representa um CPF, cuidando de limpeza, formatação e validação dos dígitos verificadores

    TAMANHO = 11

    def __init__(self, valor: str):
        self._numeros = self._limpar(valor)
        if len(self._numeros) != self.TAMANHO:
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos.")

    @staticmethod
    def _limpar(valor: str) -> str:
        return ''.join(filter(str.isdigit, valor))

    @staticmethod
    def _calcular_digito(digitos: str) -> int:
        tamanho = len(digitos)
        soma = sum(int(d) * (tamanho + 1 - i) for i, d in enumerate(digitos))
        return (soma * 10 % 11) % 10

    @property
    def numeros(self) -> str:
        return self._numeros

    @property
    def formatado(self) -> str:
        n = self._numeros
        return f"{n[:3]}.{n[3:6]}.{n[6:9]}-{n[9:]}"

    @property
    def valido(self) -> bool:
        cpf = self._numeros

        # Rejeita CPFs com todos os dígitos iguais
        if cpf == cpf[0] * self.TAMANHO:
            return False

        digito1 = self._calcular_digito(cpf[:9])
        digito2 = self._calcular_digito(cpf[:9] + str(digito1))
        return cpf[-2:] == f"{digito1}{digito2}"

    def __str__(self) -> str:
        return self.formatado

    @classmethod
    def gerar(cls) -> "CPF":
        # Gera um CPF numericamente válido, útil para testes de formulários
        base = ''.join(str(random.randint(0, 9)) for _ in range(9))
        digito1 = cls._calcular_digito(base)
        digito2 = cls._calcular_digito(base + str(digito1))
        return cls(base + str(digito1) + str(digito2))


class CPFRequest(BaseModel):
    cpf: str

    @field_validator("cpf")
    @classmethod
    def cpf_deve_ter_digitos_suficientes(cls, v: str) -> str:
        CPF(v)
        return v


class CPFResponse(BaseModel):
    cpf_sem_formatacao: str
    cpf_formatado: str
    valido: bool


@app.post("/cpf/validar", response_model=CPFResponse, summary="Valida um CPF")
def validar(data: CPFRequest):
    cpf = CPF(data.cpf)
    return CPFResponse(
        cpf_sem_formatacao=data.cpf,
        cpf_formatado=cpf.formatado,
        valido=cpf.valido,
    )


@app.get("/cpf/gerar", response_model=CPFResponse, summary="Gera um CPF válido aleatório")
def gerar():
    cpf = CPF.gerar()
    return CPFResponse(
        cpf_sem_formatacao=cpf.numeros,
        cpf_formatado=cpf.formatado,
        valido=cpf.valido,
    )
