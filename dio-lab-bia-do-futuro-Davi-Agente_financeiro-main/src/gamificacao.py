def calcular_progresso_nivel(perfil):
    """
    Retorna a % de progresso para o próximo nível (0.0 a 1.0)
    """
    xp_atual = perfil.get('xp_atual', 0)
    xp_prox = perfil.get('xp_proximo_nivel', 100)
    
    if xp_prox == 0: return 1.0
    return min(xp_atual / xp_prox, 1.0)

def calcular_progresso_meta(perfil):
    """
    Retorna a % de progresso da meta financeira
    """
    guardado = perfil['meta_atual']['guardado']
    custo = perfil['meta_atual']['custo']
    
    if custo == 0: return 1.0
    return min(guardado / custo, 1.0)