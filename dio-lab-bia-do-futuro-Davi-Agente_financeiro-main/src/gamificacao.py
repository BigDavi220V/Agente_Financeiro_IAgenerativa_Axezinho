def calcular_nivel(perfil):
    """
    Calcula a porcentagem de progresso para o próximo nível.
    Retorna um float entre 0.0 e 1.0.
    """
    xp_atual = perfil.get('xp_atual', 0)
    xp_prox = perfil.get('xp_proximo_nivel', 100)
    
    if xp_prox == 0: return 1.0
    
    progresso = xp_atual / xp_prox
    return min(progresso, 1.0)

def verificar_conquista(perfil, nova_xp):
    """
    Simula o ganho de XP e verifica se subiu de nível.
    """
    perfil['xp_atual'] += nova_xp
    
    # Lógica simples de Level Up
    if perfil['xp_atual'] >= perfil['xp_proximo_nivel']:
        perfil['titulo'] = "Mestre da Economia 🌟"
        perfil['xp_atual'] = perfil['xp_atual'] - perfil['xp_proximo_nivel']
        perfil['xp_proximo_nivel'] = int(perfil['xp_proximo_nivel'] * 1.5) # Próximo nível fica mais difícil
        return True, perfil # Retorna True se subiu de nível
        
    return False, perfil