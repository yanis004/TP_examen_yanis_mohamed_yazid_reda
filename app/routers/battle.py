from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.pokeapi import get_pokemon_data 
from app.utils.utils import get_db

router = APIRouter()

def compare_pokemon_stats(pokemon_1: dict, pokemon_2: dict):
    """
    Compare les stats des 2 Pokémons et détermine le gagnant
    """
    stats_1 = pokemon_1['stats']
    stats_2 = pokemon_2['stats']
    
    winner = 0 
    

    for stat_1, stat_2 in zip(stats_1, stats_2):
        if stat_1['base_stat'] > stat_2['base_stat']:
            winner += 1
        elif stat_1['base_stat'] < stat_2['base_stat']:
            winner -= 1


    return winner


@router.get("/battle/{pokemon_1_id}/{pokemon_2_id}")
def battle_pokemons(pokemon_1_id: int, pokemon_2_id: int, _database: Session = Depends(get_db)):
    """
    Effectuer un combat entre 2 Pokémons en comparant leurs statistiques
    """
    pokemon_1_data = get_pokemon_data(pokemon_1_id)
    pokemon_2_data = get_pokemon_data(pokemon_2_id)

    battle_result = compare_pokemon_stats(pokemon_1_data, pokemon_2_data)

    if battle_result > 0:
        return {"winner": pokemon_1_data['name'], "status": "Victory", "details": pokemon_1_data}
    elif battle_result < 0:
        return {"winner": pokemon_2_data['name'], "status": "Victory", "details": pokemon_2_data}
    else:
        return {"winner": "Draw", "status": "Draw", "details": None}