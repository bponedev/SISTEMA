from dataclasses import dataclass

@dataclass
class User:
    id: int
    nome: str
    email: str
    senha: str

@dataclass
class Registro:
    id: int
    titulo: str
    descricao: str
    data: str
