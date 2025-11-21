import json
from typing import List, Dict, Tuple

# ===================================================================
# CARREGAMENTO DOS DADOS DO ARQUIVO JSON
# ===================================================================
# Esta função lê o arquivo JSON com o catálogo de cursos e retorna uma lista
# de dicionários, onde cada dicionário representa um curso com nome, horas,
# impacto, categoria, etc.
def load_courses(filename: str = "courses_reskilling.json") -> List[Dict]:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            courses = json.load(file)
        print(f"Catálogo carregado com sucesso! {len(courses)} cursos encontrados.\n")
        return courses
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado!")
        exit(1)
    except json.JSONDecodeError:
        print("Erro: O arquivo JSON está mal formatado.")
        exit(1)


# ===================================================================
# ALGORITMO 1: KNAPSACK COM MEMOIZAÇÃO (TOP-DOWN)
# ===================================================================
# Abordagem recursiva com cache (memoization) para evitar recomputação
# de subproblemas já resolvidos. Mais elegante e próximo da definição matemática.
# ===================================================================
def knapsack_memoization(courses: List[Dict], capacity: int) -> Tuple[int, List[Dict]]:
    n = len(courses)
    memo = {}

    def dp(i: int, w: int) -> int:
        if i == 0 or w == 0:
            return 0
        if (i, w) in memo:
            return memo[(i, w)]

        course = courses[i-1]
        if course["hours"] > w:
            result = dp(i - 1, w)
        else:
            without = dp(i - 1, w)
            with_course = course["impact"] + dp(i - 1, w - course["hours"])
            result = max(without, with_course)
        memo[(i, w)] = result
        return result

    max_value = dp(n, capacity)

    # RECONSTRUÇÃO CORRIGIDA E ROBUSTA (igual ao bottom-up em confiabilidade)
    selected = []
    w = capacity
    i = n

    while i > 0:
        if w <= 0:
            break
        course = courses[i-1]
        
        # Se o curso couber E incluir ele dá o valor atual registrado no memo
        if (course["hours"] <= w and 
            (i-1, w - course["hours"]) in memo and 
            memo[(i-1, w - course["hours"])] + course["impact"] == memo[(i, w)]):
            
            selected.append(course)
            w -= course["hours"]
        # Caso contrário, apenas passamos para o próximo curso
        i -= 1

    selected.reverse()
    return max_value, selected


# ===================================================================
# ALGORITMO 2: KNAPSACK COM TABULAÇÃO (BOTTOM-UP)
# ===================================================================
# Abordagem iterativa usando uma matriz DP. Mais eficiente em memória em alguns casos
# e mais fácil de reconstruir a solução.
def knapsack_tabulation(courses: List[Dict], capacity: int) -> Tuple[int, List[Dict]]:
    n = len(courses)
    
    # dp[i][w] = valor máximo de impacto usando os primeiros i cursos com capacidade w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Matriz auxiliar para saber quais itens foram incluídos (facilita reconstrução)
    keep = [[False for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Preenchimento da tabela DP
    for i in range(1, n + 1):
        hours = courses[i-1]["hours"]
        impact = courses[i-1]["impact"]
        
        for w in range(0, capacity + 1):
            # Opção 1: não incluir o curso atual
            dp[i][w] = dp[i-1][w]
            
            # Opção 2: incluir o curso (se couber)
            if hours <= w:
                value_if_taken = impact + dp[i-1][w - hours]
                if value_if_taken > dp[i][w]:
                    dp[i][w] = value_if_taken
                    keep[i][w] = True  # Marcamos que o curso i foi incluído nessa capacidade

    max_value = dp[n][capacity]

    # ===================================================================
    # RECONSTRUÇÃO DA SOLUÇÃO A PARTIR DA MATRIZ KEEP
    # ===================================================================
    selected_courses = []
    w = capacity
    i = n

    while i > 0 and w > 0:
        if keep[i][w]:  # Este curso foi incluído na solução ótima
            course = courses[i-1]
            selected_courses.append(course)
            w -= course["hours"]  # Volta no tempo
        i -= 1

    selected_courses.reverse()
    return max_value, selected_courses


# ===================================================================
# FUNÇÕES DE EXIBIÇÃO (INTERFACE NO CONSOLE)
# ===================================================================
def print_catalog(courses: List[Dict]):
    print("CATÁLOGO DE CURSOS PARA REQUALIFICAÇÃO")
    print("=" * 80)
    print(f"{'Nome do Curso':35} {'Horas':>6} {'Impacto':>8} {'Categoria'}")
    print("-" * 80)
    for c in courses:
        print(f"{c['name']:35} {c['hours']:6} {c['impact']:8}  {c['category']}")
    print("-" * 80)

def print_solution(title: str, value: int, courses_selected: List[Dict], total_hours: int):
    print(f"\n{title}")
    print(f"Impacto Máximo Alcançado: {value} pontos")
    print(f"Horas utilizadas: {total_hours}h")
    print("Cursos recomendados:")
    print("-" * 50)
    for c in courses_selected:
        print(f"  • {c['name']} ({c['hours']}h) → Impacto: {c['impact']} | {c['category']}")
    print("-" * 50)


# ===================================================================
# FUNÇÃO PRINCIPAL (MAIN)
# ===================================================================
def main():
    print("=" * 70)
    print("   GLOBAL SOLUTION - O FUTURO DO TRABALHO")
    print("   Otimizador de Requalificação com Programação Dinâmica")
    print("   Problema da Mochila 0/1 - Duas Abordagens")
    print("=" * 70)

    # 1. Carrega os cursos
    courses = load_courses()

    # 2. Exibe catálogo
    print_catalog(courses)

    # 3. Solicita tempo disponível
    while True:
        try:
            capacity = int(input("\nQuantas horas você tem disponíveis para estudar? "))
            if capacity <= 0:
                print("Por favor, informe um número positivo.")
            else:
                break
        except ValueError:
            print("Digite um número inteiro válido!")

    print(f"\nCalculando a melhor combinação para {capacity} horas de estudo...")

    # 4. Executa os dois algoritmos
    value_memo, selected_memo = knapsack_memoization(courses, capacity)
    value_tab, selected_tab = knapsack_tabulation(courses, capacity)

    # Calcula total de horas usadas
    hours_memo = sum(c["hours"] for c in selected_memo)
    hours_tab = sum(c["hours"] for c in selected_tab)

    # 5. Exibe resultados
    print_solution("RESULTADO - MEMOIZAÇÃO (Top-Down)", value_memo, selected_memo, hours_memo)
    print_solution("RESULTADO - TABULAÇÃO (Bottom-Up)", value_tab, selected_tab, hours_tab)

    # 6. Verificação final de equivalência
    print("\nVERIFICAÇÃO DE CONSISTÊNCIA")
    print("=" * 60)
    if value_memo == value_tab and hours_memo == hours_tab:
        # Compara pelos IDs para garantir mesma seleção
        ids_memo = sorted([c["id"] for c in selected_memo])
        ids_tab = sorted([c["id"] for c in selected_tab])
        if ids_memo == ids_tab:
            print("SUCESSO! Ambos os algoritmos retornaram a MESMA solução ótima!")
            print("Programação Dinâmica comprovadamente correta.")
        else:
            print("ATENÇÃO: Valores iguais, mas cursos diferentes (improvável no 0/1 knapsack correto).")
    else:
        print("ERRO: Os dois métodos divergiram! Revisar implementações.")

    print("\nObrigado por usar o Otimizador de Carreira do Futuro!")

# ===================================================================
# EXECUÇÃO
# ===================================================================
if __name__ == "__main__":
    main()