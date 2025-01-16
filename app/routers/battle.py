from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.pokeapi import get_pokemon_data
from app.utils.utils import get_db

router = APIRouter()

def compare_pokemon_stats(pokemon_1: dict, pokemon_2: dict) -> int:
    stats_1 = pokemon_1["stats"]
    stats_2 = pokemon_2["stats"]

    score_1 = 0
    score_2 = 0

    # Comparaison des statistiques une par une
    for stat_1, stat_2 in zip(stats_1, stats_2):
        if stat_1["base_stat"] > stat_2["base_stat"]:
            score_1 += 1
        elif stat_1["base_stat"] < stat_2["base_stat"]:
            score_2 += 1

    return {
        "pokemon_1_score": score_1,
        "pokemon_2_score": score_2,
        "winner": (
            pokemon_1["name"] if score_1 > score_2
            else pokemon_2["name"] if score_2 > score_1
            else "Draw"
        )
    }

@router.get("/{pokemon_1_id}/{pokemon_2_id}")
def battle_pokemons(pokemon_1_id: int, pokemon_2_id: int, database: Session = Depends(get_db)):
    pokemon_1_data = get_pokemon_data(pokemon_1_id)
    pokemon_2_data = get_pokemon_data(pokemon_2_id)

    if not pokemon_1_data or not pokemon_2_data:
        raise HTTPException(status_code=404, detail="Un ou plusieurs Pokémons introuvables dans PokeAPI.")

    # Comparer les stats des deux Pokémons
    result = compare_pokemon_stats(pokemon_1_data, pokemon_2_data)

    return {
        "pokemon_1": pokemon_1_data["name"],
        "pokemon_2": pokemon_2_data["name"],
        "pokemon_1_score": result["pokemon_1_score"],
        "pokemon_2_score": result["pokemon_2_score"],
        "winner": result["winner"]
    }