"""Grupo 5 — Planejador de caminhos."""

from copy import deepcopy


mapa = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B", "G"],
    "E": ["B", "F", "G"],
    "F": ["C", "E"],
    "G": ["D", "E"],
    "H": [],  # ponto isolado
}


def buscar_caminho_original(origem, destino):
    """Busca em largura usando uma fila."""
    if origem not in mapa or destino not in mapa:
        return None

    fila = [[origem]]
    visitados = {origem}
    while fila:
        caminho = fila.pop(0)
        atual = caminho[-1]
        if atual == destino:
            return caminho

        for vizinho in mapa[atual]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(caminho + [vizinho])
    return None


def explorar_fila(grafo, fila, visitados, destino):
    """Busca em largura usando recursão."""
    if not fila:
        return None

    caminho = fila[0]
    atual = caminho[-1]

    if atual == destino:
        return list(caminho)

    # Evita voltar aos pontos já visitados e repetir ciclos.
    novos_caminhos = tuple(
        caminho + (vizinho,)
        for vizinho in grafo[atual]
        if vizinho not in visitados
    )

    # Os caminhos novos entram no fim da fila para manter a busca em largura.
    nova_fila = fila[1:] + novos_caminhos
    # A união cria outro conjunto, sem alterar os visitados da chamada anterior.
    novos_visitados = visitados.union(
        novo_caminho[-1] for novo_caminho in novos_caminhos
    )

    return explorar_fila(grafo, nova_fila, novos_visitados, destino)


def buscar_caminho(origem, destino):
    if origem not in mapa or destino not in mapa:
        return None

    return explorar_fila(
        mapa,
        fila=((origem,),),
        visitados=frozenset({origem}),
        destino=destino,
    )


def comparar_implementacoes():
    """Compara os resultados das duas buscas."""
    # Esta cópia permite conferir se o mapa foi alterado.
    mapa_antes = deepcopy(mapa)
    total = 0

    for origem in mapa:
        for destino in mapa:
            original = buscar_caminho_original(origem, destino)
            recursivo = buscar_caminho(origem, destino)
            if original != recursivo:
                raise AssertionError(
                    f"Resultados diferentes para {origem} -> {destino}: "
                    f"{original} e {recursivo}"
                )
            total += 1

    if mapa != mapa_antes:
        raise AssertionError("O mapa original foi alterado durante as buscas.")

    print(f"Comparação das versões: {total}/{total} resultados iguais.")
    print("Mapa original preservado: Sim.")


def main():
    print("=== PLANEJADOR DE CAMINHOS ===")
    comparar_implementacoes()
    print("Pontos disponíveis:", ", ".join(sorted(mapa)))

    while True:
        origem = input("\nOrigem (ou 0 para sair): ").strip().upper()
        if origem == "0":
            break
        destino = input("Destino: ").strip().upper()
        caminho = buscar_caminho(origem, destino)
        if caminho is None:
            print("Não foi encontrado um caminho válido.")
        else:
            print("Caminho:", " -> ".join(caminho))
            print("Quantidade de conexões:", len(caminho) - 1)


if __name__ == "__main__":
    main()
