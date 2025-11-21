import time
import sys
import random
import gc
import math

# Imports das estruturas
from matriz_esparsa1 import MatrizEsparsa1
from matriz_esparsa2 import MatrizEsparsa2

# --- FUNÇÕES AUXILIARES ---
def get_deep_size(obj, seen=None):
    size = sys.getsizeof(obj)
    if seen is None: seen = set()
    obj_id = id(obj)
    if obj_id in seen: return 0
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_deep_size(v, seen) + get_deep_size(k, seen) for k, v in obj.items()])
    elif hasattr(obj, '__dict__'):
        size += get_deep_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_deep_size(i, seen) for i in obj])
    return size

def measure_memory(obj):
    return get_deep_size(obj)

def generate_coords(n, sparsity_fraction):
    total_positions = n * n
    num_elements = int(total_positions * sparsity_fraction)
    if num_elements == 0: num_elements = 1
    coords = set()
    while len(coords) < num_elements:
        coords.add((random.randint(0, n-1), random.randint(0, n-1)))
    return list(coords)

def get_sparsity_scenarios(n):
    i = int(math.log10(n))
    if i < 4: return [0.01, 0.05, 0.10, 0.20]
    else: return [1.0/(10**(i+4)), 1.0/(10**(i+3)), 1.0/(10**(i+2))]

def run_test_routine(n, sp, struct_name, MatrizClass, coords_A, coords_B):
    # 1. Criação
    start = time.perf_counter()
    mat_a = MatrizClass()
    for r, c in coords_A: mat_a.inserir(r, c, random.random())
    mat_b = MatrizClass()
    for r, c in coords_B: mat_b.inserir(r, c, random.random())
    t_create = time.perf_counter() - start
    
    mem = measure_memory(mat_a)
    print(f"{n:<8} | {sp:<10.2g} | {struct_name:<12} | {'Create':<10} | {t_create:<10.6f} | {mem:<10}")

    # 2. Soma
    start = time.perf_counter()
    mat_a.soma(mat_b)
    t_sum = time.perf_counter() - start
    print(f"{n:<8} | {sp:<10.2g} | {struct_name:<12} | {'Sum':<10} | {t_sum:<10.6f} | {'-':<10}")

    # 3. Multiplicação Escalar (NOVO)
    start = time.perf_counter()
    mat_a.multiplicar_escalar(2.5)
    t_esc = time.perf_counter() - start
    print(f"{n:<8} | {sp:<10.2g} | {struct_name:<12} | {'Escalar':<10} | {t_esc:<10.6f} | {'-':<10}")

    # 4. Transposta (NOVO)
    start = time.perf_counter()
    mat_a.transpor()
    t_trans = time.perf_counter() - start
    print(f"{n:<8} | {sp:<10.2g} | {struct_name:<12} | {'Transp':<10} | {t_trans:<10.6f} | {'-':<10}")

    # 5. Multiplicação Matriz (Apenas se N for razoável ou muito esparso)
    # Para Árvore em N grande e esparsidade alta, isso pode demorar muito.
    if n == 1000 and sp >= 0.1:
        print(f"{n:<8} | {sp:<10.2g} | {struct_name:<12} | {'Mult':<10} | {'SKIP':<10} | {'-':<10}")
    else:
        start = time.perf_counter()
        mat_a.multiplicar(mat_b)
        t_mult = time.perf_counter() - start
        print(f"{n:<8} | {sp:<10.2g} | {struct_name:<12} | {'Mult':<10} | {t_mult:<10.6f} | {'-':<10}")

    del mat_a, mat_b
    gc.collect()

# --- MOTOR PRINCIPAL ---
def benchmark_engine():
    # Configure aqui até onde quer ir: [100, 1000, 10000, 100000, 1000000]
    sizes = [100, 1000, 10000, 100000, 1000000] 
    
    print(f"{'N':<8} | {'Sparsity':<10} | {'Structure':<12} | {'Op':<10} | {'Time (s)':<10} | {'Mem (Bytes)':<10}")
    print("-" * 80)
    
    for n in sizes:
        sparsities = get_sparsity_scenarios(n)
        for sp in sparsities:
            coords_A = generate_coords(n, sp)
            coords_B = generate_coords(n, sp)
            
            # Teste Estrutura 1 (Hash)
            run_test_routine(n, sp, "Hash+Lista", MatrizEsparsa1, coords_A, coords_B)
            
            # Teste Estrutura 2 (Árvore)
            run_test_routine(n, sp, "BinTree", MatrizEsparsa2, coords_A, coords_B)
            
            # Teste Estrutura 3 (Densa) - Cuidado com N grande
            if n <= 10000:
                start = time.perf_counter()
                dense_a = [[0.0] * n for _ in range(n)]
                for r, c in coords_A: dense_a[r][c] = random.random()
                dense_b = [[0.0] * n for _ in range(n)]
                for r, c in coords_B: dense_b[r][c] = random.random()
                t_create = time.perf_counter() - start
                mem_dense = sys.getsizeof(dense_a) + sum(sys.getsizeof(row) for row in dense_a)
                print(f"{n:<8} | {sp:<10.2g} | {'Dense':<12} | {'Create':<10} | {t_create:<10.6f} | {mem_dense:<10}")

                start = time.perf_counter()
                _ = [[dense_a[i][j] + dense_b[i][j] for j in range(n)] for i in range(n)]
                t_sum = time.perf_counter() - start
                print(f"{n:<8} | {sp:<10.2g} | {'Dense':<12} | {'Sum':<10} | {t_sum:<10.6f} | {'-':<10}")
                
                del dense_a, dense_b
                gc.collect()

benchmark_engine()