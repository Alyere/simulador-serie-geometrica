"""
Back-End API em Python Puro — Simulador de Séries Geométricas (Grupo 6)
Disciplina: Cálculo Diferencial e Integral II — UNIESP
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import math
from pathlib import Path
import threading
import webbrowser

DIRETORIO_BASE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class EtapaSimulacao:
    etapa: int
    termo_atual: float
    soma_analitica: float
    soma_iterativa: float
    percentual_teto: float | None


def calcular_soma_parcial_analitica(a: float, r: float, k: int) -> float:
    if k <= 0:
        return 0.0
    if math.isclose(r, 1.0, rel_tol=1e-12):
        return k * a
    return a * (1.0 - (r ** k)) / (1.0 - r)


def processar_simulacao(a: float, r: float, n: int, unidade: str = "GB") -> dict:
    if n <= 0 or n > 300:
        raise ValueError("O número de etapas (n) deve estar entre 1 e 300.")
    if not (math.isfinite(a) and math.isfinite(r)):
        raise ValueError("O primeiro termo (a) e a razão (r) devem ser números reais finitos.")

    converge = (a == 0.0) or (abs(r) < 1.0)
    soma_infinita: float | None = None
    if converge:
        soma_infinita = 0.0 if a == 0.0 else a / (1.0 - r)

    termos_acumulados: list[float] = []
    etapas: list[dict] = []

    try:
        for k in range(1, n + 1):
            termo_k = a * (r ** (k - 1))
            termos_acumulados.append(termo_k)

            soma_iter = math.fsum(termos_acumulados)
            soma_analit = calcular_soma_parcial_analitica(a, r, k)

            percentual: float | None = None
            if soma_infinita is not None and not math.isclose(soma_infinita, 0.0):
                percentual = (soma_analit / soma_infinita) * 100.0

            etapas.append(
                asdict(
                    EtapaSimulacao(
                        etapa=k,
                        termo_atual=termo_k,
                        soma_analitica=soma_analit,
                        soma_iterativa=soma_iter,
                        percentual_teto=percentual,
                    )
                )
            )
    except OverflowError as exc:
        raise ValueError("Os valores excedem o limite numérico suportado. Reduza n ou r.") from exc

    soma_final = etapas[-1]["soma_analitica"]
    margem = (soma_infinita - soma_final) if soma_infinita is not None else None

    return {
        "parametros": {
            "primeiro_termo": a,
            "razao": r,
            "num_termos": n,
            "unidade": unidade.strip() or "GB",
        },
        "etapas": etapas,
        "soma_n_analitica": soma_final,
        "soma_n_iterativa": etapas[-1]["soma_iterativa"],
        "converge": converge,
        "soma_infinita": soma_infinita,
        "margem_restante": margem,
    }


class ApiSerieHandler(SimpleHTTPRequestHandler):
    """Serve o Front-End (index.html) e responde às requisições JSON da API."""

    def log_message(self, format: str, *args) -> None:
        pass

    def _enviar_json(self, status: HTTPStatus, payload: dict) -> None:
        corpo = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_POST(self) -> None:
        if self.path != "/api/simular":
            self._enviar_json(HTTPStatus.NOT_FOUND, {"erro": "Rota não encontrada."})
            return

        try:
            tamanho = int(self.headers.get("Content-Length", 0))
            dados_brutos = self.rfile.read(tamanho).decode("utf-8")
            body = json.loads(dados_brutos)

            a = float(body.get("primeiro_termo", 10))
            r = float(body.get("razao", 0.5))
            n = int(body.get("num_termos", 5))
            unidade = str(body.get("unidade", "GB"))

            resultado = processar_simulacao(a, r, n, unidade)
            self._enviar_json(HTTPStatus.OK, resultado)

        except (ValueError, TypeError, json.JSONDecodeError) as err:
            self._enviar_json(HTTPStatus.BAD_REQUEST, {"erro": str(err)})


def criar_servidor_porta_livre(porta_inicial: int = 8000, tentativas: int = 10) -> tuple[ThreadingHTTPServer, int]:
    """Encontra automaticamente uma porta livre caso a 8000 já esteja em uso."""
    handler = partial(ApiSerieHandler, directory=str(DIRETORIO_BASE))
    for porta in range(porta_inicial, porta_inicial + tentativas):
        try:
            servidor = ThreadingHTTPServer(("127.0.0.1", porta), handler)
            return servidor, porta
        except OSError:
            continue
    raise RuntimeError("Nenhuma porta livre encontrada entre 8000 e 8009.")


def iniciar_servidor() -> None:
    servidor, porta = criar_servidor_porta_livre()
    url = f"http://localhost:{porta}"

    print("=" * 68)
    print(" SERVIDOR WEB INICIADO — CÁLCULO II (GRUPO 6)")
    print(f" Acesse no navegador: {url}")
    print(" Pressione Ctrl+C no terminal para encerrar.")
    print("=" * 68)

    threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado com sucesso.")
        servidor.server_close()


if __name__ == "__main__":
    iniciar_servidor()