import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuração de Estilo
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'figure.figsize': (10, 6), 
    'figure.dpi': 120,
    'axes.titlesize': 14,
    'axes.labelsize': 12
})

def preparar_dados():
    try:
        df = pd.read_csv('tabela_final_excel.csv', sep=';', decimal=',')
        print("Dados carregados com sucesso!")
    except FileNotFoundError:
        print("ERRO: 'tabela_final_excel.csv' não encontrado. Rode o gerar_csv.py antes.")
        return None

    # Conversão forçada para numérico
    df['N'] = pd.to_numeric(df['N'])
    df['Time (s)'] = pd.to_numeric(df['Time (s)'], errors='coerce')
    df['Memory (Bytes)'] = pd.to_numeric(df['Memory (Bytes)'], errors='coerce')
    df['Sparsity (%)'] = df['Sparsity'] * 100
    
    # Cria pasta para salvar gráficos
    if not os.path.exists('graficos_output'):
        os.makedirs('graficos_output')
        
    return df

def plotar_generico(df, x_col, y_col, titulo, nome_arquivo, log_scale=True, hue='Structure'):
    if df.empty:
        print(f"Aviso: Sem dados para gerar {nome_arquivo}")
        return

    plt.figure()
    ax = sns.lineplot(
        data=df, 
        x=x_col, 
        y=y_col, 
        hue=hue, 
        style=hue, 
        markers=True, 
        dashes=False, 
        linewidth=2.5,
        palette='viridis' # Paleta de cores profissional
    )
    
    if log_scale:
        ax.set_xscale('log')
        ax.set_yscale('log')
        titulo += " (Escala Log)"
    
    plt.title(titulo)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    caminho = os.path.join('graficos_output', nome_arquivo)
    plt.savefig(caminho, bbox_inches='tight')
    plt.close()
    print(f"Gerado: {caminho}")

def gerar_todos_graficos():
    df = preparar_dados()
    if df is None: return

    # 1. GRÁFICO DE MEMÓRIA (Todas as estruturas)
    # Filtra operação Create pois é onde medimos memória
    df_mem = df[df['Operation'] == 'Create'].copy()
    df_mem['Memory (MB)'] = df_mem['Memory (Bytes)'] / (1024 * 1024)
    plotar_generico(
        df_mem, 'N', 'Memory (MB)', 
        'Comparativo de Consumo de Memória', 
        'Grafico_1_Memoria_vs_N.png'
    )

    # 2. GRÁFICOS DE TEMPO POR OPERAÇÃO (N no Eixo X)
    operacoes = [
        ('Mult', 'Grafico_2_Tempo_Mult_vs_N.png'),
        ('Sum', 'Grafico_3_Tempo_Soma_vs_N.png'),
        ('Create', 'Grafico_4_Tempo_Criacao_vs_N.png'),
        ('Transp', 'Grafico_5_Tempo_Transposta_vs_N.png'),
        ('Escalar', 'Grafico_6_Tempo_Escalar_vs_N.png')
    ]

    for op, arquivo in operacoes:
        df_op = df[df['Operation'] == op].dropna(subset=['Time (s)'])
        plotar_generico(
            df_op, 'N', 'Time (s)', 
            f'Tempo de Execução: {op}', 
            arquivo
        )

    # 3. GRÁFICO DE IMPACTO DA ESPARSIDADE (Focando em um N fixo)
    # Tenta pegar N=100 ou N=200 onde temos variação de 1% a 20%
    for n_target in [100, 200, 500]:
        if n_target in df['N'].unique():
            df_sp = df[(df['N'] == n_target) & (df['Operation'] == 'Mult')].copy()
            
            # Plot linear aqui para ver a inclinação da curva
            plt.figure()
            sns.lineplot(
                data=df_sp, x='Sparsity (%)', y='Time (s)', 
                hue='Structure', marker='o', linewidth=2.5
            )
            plt.title(f'Impacto da Esparsidade na Multiplicação (N={n_target})')
            plt.xticks([1, 5, 10, 20])
            plt.grid(True, alpha=0.3)
            
            caminho = os.path.join('graficos_output', f'Grafico_7_Impacto_Esparsidade_N{n_target}.png')
            plt.savefig(caminho, bbox_inches='tight')
            plt.close()
            print(f"Gerado: {caminho}")
            break # Gera só para o primeiro N válido que achar

gerar_todos_graficos()