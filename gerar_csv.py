import pandas as pd

def parse_results(filename):
    data = []
    
    # Variável para guardar a memória do bloco atual
    current_memory_val = None
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        # Pula linhas de cabeçalho, separadores ou vazias
        if "Sparsity" in line or "---" in line or not line.strip():
            continue
            
        # Quebra a linha pelo separador '|'
        parts = [p.strip() for p in line.split('|')]
        
        # Verifica se a linha tem o número certo de colunas (6 colunas)
        if len(parts) >= 6:
            try:
                n = int(parts[0])
                sparsity = float(parts[1])
                structure = parts[2]
                op = parts[3]
                time_str = parts[4]
                mem_str = parts[5]
                
                # --- LÓGICA DE TEMPO ---
                time_val = None
                if time_str != 'SKIP' and time_str != '-':
                    time_val = float(time_str)
                
                # --- LÓGICA DE MEMÓRIA (PROPAGAÇÃO) ---
                # Se for a operação de Criação, capturamos a memória real
                if op == 'Create':
                    if mem_str != '-' and mem_str != 'None':
                        current_memory_val = int(mem_str)
                    else:
                        current_memory_val = None
                    
                    mem_val = current_memory_val
                
                # Se for outra operação (Soma, Mult, etc.), usamos a memória capturada no Create anterior
                else:
                    mem_val = current_memory_val

                data.append({
                    'N': n,
                    'Sparsity': sparsity,
                    'Structure': structure,
                    'Operation': op,
                    'Time (s)': time_val,
                    'Memory (Bytes)': mem_val
                })
            except ValueError:
                continue # Pula linhas com formato inesperado ou erros de conversão

    df = pd.DataFrame(data)
    return df

# --- EXECUÇÃO ---
filename = 'resultados.txt' # Certifique-se que este arquivo existe

try:
    df = parse_results(filename)

    # Salva em CSV (formato ponto e vírgula para Excel em português)
    df.to_csv('tabela_final_excel.csv', index=False, sep=';', decimal=',')
    print("Arquivo 'tabela_final_excel.csv' criado com sucesso!")
    print("A memória foi propagada das linhas 'Create' para as demais operações.")

    # Prévia para conferência
    print("\nPrévia (Mostrando como a memória foi preenchida nas outras ops):")
    # Mostra as 10 primeiras linhas onde N=100 para verificar se a memória repetiu
    print(df[df['N']==100].head(10))

except FileNotFoundError:
    print(f"Erro: O arquivo '{filename}' não foi encontrado. Rode o benchmark.py primeiro.")