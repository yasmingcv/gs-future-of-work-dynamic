import json
from typing import List, Dict, Tuple


# Carregamento de dados do catálogo de cursos
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


# Knapsack com memoização (top-down)
def knapsack_memoization(courses: List[Dict], capacity: int) -> Tuple[int, List[Dict]]:
    n = len(courses)  # Número total de cursos disponíveis
    
    # Dicionário para armazenar resultados já calculados (memoização)
    # Chave: (índice_curso, capacidade_restante) -> Valor: impacto_máximo_possível
    memo = {}

    # Função recursiva que calcula o impacto máximo possível
    # i: número de cursos considerados (1 a n)
    # w: capacidade restante da mochila (horas disponíveis)
    def dp(i: int, w: int) -> int:        
        
        # Se não há cursos para considerar ou se não há tempo restantw
        if i == 0 or w == 0:
            return 0  # Impacto = 0
        
        # VERIFICAÇÃO DO CACHE (MEMOIZAÇÃO)
        # Se já calculamos este subproblema antes, reutilizamos o resultado
        if (i, w) in memo:
            return memo[(i, w)]

        # ANÁLISE DO CURSO ATUAL
        course = courses[i-1]  # Curso atual (índice i-1 porque contamos de 1..n)
        
        # DECISÃO: INCLUIR OU NÃO O CURSO
        if course["hours"] > w:
            # CASO 1: O curso não cabe na mochila (horas > capacidade restante)
            # Única opção: pular este curso e considerar os próximos
            result = dp(i - 1, w)
        else:
            # CASO 2: O curso cabe na mochila - temos duas opções:
            
            # Opção A: NÃO incluir o curso atual
            without = dp(i - 1, w)
            
            # Opção B: INCLUIR o curso atual
            # Ganhamos o impacto do curso + o melhor que conseguimos com o resto
            with_course = course["impact"] + dp(i - 1, w - course["hours"])
            
            # Escolhemos a melhor das duas opções
            result = max(without, with_course)
        
        # ARMAZENAMENTO NO CACHE
        # Guardamos o resultado para evitar recalcular este subproblema
        memo[(i, w)] = result
        return result

    # CHAMADA INICIAL
    # Calcula o impacto máximo considerando todos os n cursos com capacidade total
    max_value = dp(n, capacity)

    # RECONSTRUÇÃO DA SOLUÇÃO: Descobrir quais cursos foram selecionados
    
    selected = []  # Lista para armazenar os cursos selecionados
    w = capacity   # Capacidade atual (vai diminuindo conforme "voltamos no tempo")
    i = n         # Índice atual do curso (vai de n até 1)

    # Percorremos de trás para frente, reconstruindo as decisões ótimas
    while i > 0:
        # Se não há mais capacidade, paramos
        if w <= 0:
            break
            
        course = courses[i-1]  # Curso atual sendo analisado
        
        # TESTE: Este curso foi incluído na solução ótima?
        # Verificamos se incluir este curso resulta no valor ótimo armazenado
        
        # Condições para o curso ter sido incluído:
        # 1. O curso deve caber na capacidade atual
        # 2. Deve existir solução para o estado "sem este curso"
        # 3. Impacto do curso + solução sem ele = solução atual (prova que foi incluído)
        if (course["hours"] <= w and 
            (i-1, w - course["hours"]) in memo and 
            memo[(i-1, w - course["hours"])] + course["impact"] == memo[(i, w)]):
            
            # Este curso foi incluído na solução ótima!
            selected.append(course)
            w -= course["hours"]  # "Consumimos" as horas deste curso
            
        # Caso contrário, este curso NÃO foi incluído
        # Simplesmente passamos para o próximo curso
        i -= 1

    # Invertemos a lista porque construímos de trás para frente
    selected.reverse()
    
    return max_value, selected

# Knapsack com tabulação (bottom-up)
def knapsack_tabulation(courses: List[Dict], capacity: int) -> Tuple[int, List[Dict]]:
    n = len(courses)  # Número total de cursos disponíveis
    
    # INICIALIZAÇÃO DAS TABELAS
    
    # Tabela principal de programação dinâmica
    # dp[i][w] = máximo impacto possível usando os primeiros i cursos com w horas
    # Dimensões: (n+1) x (capacity+1) para incluir casos base (0 cursos, 0 horas)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Tabela auxiliar para rastrear decisões (facilita reconstrução da solução)
    # keep[i][w] = True se o curso i foi incluído na solução ótima com w horas
    keep = [[False for _ in range(capacity + 1)] for _ in range(n + 1)]

    # PREENCHIMENTO DA TABELA DP (BOTTOM-UP)
    
    # Iteramos sobre todos os cursos (de 1 a n)
    for i in range(1, n + 1):
        # Dados do curso atual
        hours = courses[i-1]["hours"]    # Horas necessárias
        impact = courses[i-1]["impact"]  # Impacto na carreira
        
        # Para cada capacidade possível (de 0 a capacity)
        for w in range(0, capacity + 1):
            
            # OPÇÃO 1: NÃO INCLUIR o curso atual
            # Herdamos o melhor resultado dos primeiros (i-1) cursos
            dp[i][w] = dp[i-1][w]
            
            # OPÇÃO 2: INCLUIR o curso atual (se couber)
            if hours <= w:
                # Calculamos o valor se incluírmos este curso:
                # Impacto do curso atual + melhor solução com capacidade reduzida
                value_if_taken = impact + dp[i-1][w - hours]
                
                # Se incluir o curso é melhor que não incluir
                if value_if_taken > dp[i][w]:
                    dp[i][w] = value_if_taken    # Atualizamos o valor ótimo
                    keep[i][w] = True           # Marcamos que este curso foi incluído

    # O resultado final está em dp[n][capacity]: todos os cursos, capacidade total
    max_value = dp[n][capacity]

    # RECONSTRUÇÃO DA SOLUÇÃO: Identificar cursos selecionados
    
    selected_courses = []  # Lista para armazenar cursos da solução ótima
    w = capacity          # Capacidade atual (diminui conforme reconstruímos)
    i = n                # Índice do curso atual (vai de n até 1)

    # Percorremos a tabela de trás para frente, seguindo as decisões ótimas
    while i > 0 and w > 0:
        
        # VERIFICAÇÃO: Este curso foi incluído?
        # Consultamos a matriz 'keep' que marcou as decisões durante o preenchimento
        if keep[i][w]:
            # Este curso foi incluído na solução ótima!
            
            course = courses[i-1]  # Obtemos os dados do curso
            selected_courses.append(course)  # Adicionamos à solução
            
            # "Voltamos no tempo": reduzimos a capacidade pelo que foi usado
            w -= course["hours"]
            
        # Passamos para o curso anterior (independente se foi incluído ou não)
        i -= 1

    # Como construímos a lista de trás para frente, precisamos inverter
    # para ter a ordem cronológica correta dos cursos
    selected_courses.reverse()
    
    return max_value, selected_courses


# Funções de exibição dos resultados
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


def main():
    print("=" * 70)
    print("   GLOBAL SOLUTION - O FUTURO DO TRABALHO")
    print("   Otimizador de Requalificação com Programação Dinâmica")
    print("   Problema da Mochila 0/1 - Duas Abordagens")
    print("=" * 70)

    # Carrega os cursos
    courses = load_courses()

    # Exibe catálogo
    print_catalog(courses)

    # Solicita tempo disponível
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

    # Executa os dois algoritmos
    value_memo, selected_memo = knapsack_memoization(courses, capacity)
    value_tab, selected_tab = knapsack_tabulation(courses, capacity)

    # Calcula total de horas usadas
    hours_memo = sum(c["hours"] for c in selected_memo)
    hours_tab = sum(c["hours"] for c in selected_tab)

    # Exibe resultados
    print_solution("RESULTADO - MEMOIZAÇÃO (Top-Down)", value_memo, selected_memo, hours_memo)
    print_solution("RESULTADO - TABULAÇÃO (Bottom-Up)", value_tab, selected_tab, hours_tab)

    # Verificação final de equivalência
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

if __name__ == "__main__":
    main()