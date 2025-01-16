from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import actions, models, schemas
from app.utils.utils import get_db
from app.utils.pokeapi import get_pokemon_data
from typing import List
import random

router = APIRouter()

@router.get("/", response_model=List[schemas.Pokemon])
def get_pokemons(skip: int = 0, limit: int = 100, database: Session = Depends(get_db)):
    """
    Retourne tous les Pokémons depuis la base de données.
    """
    pokemons = database.query(models.Pokemon).all()  
    print(f"Pokémons récupérés : {pokemons}")
    return pokemons

@router.get("/random", response_model=List[schemas.PokemonWithStats])
def get_random_pokemons(database: Session = Depends(get_db)):
    """
    Retourne 3 Pokémons aléatoires avec leurs statistiques.
    
    Returns:
        List[schemas.PokemonWithStats]: Liste de 3 Pokémons avec leurs statistiques.
    """
    try:
        # Récupérer tous les Pokémons de la base de données
        pokemons = database.query(models.Pokemon).all()

        # Sélectionner 3 Pokémons aléatoires
        random_pokemons = random.sample(pokemons, 3)

        # Récupérer les statistiques des Pokémons
        result = []
        for pokemon in random_pokemons:
            pokemon_data = get_pokemon_data(pokemon.api_id)
            
            if not pokemon_data:
                print(f"Impossible de récupérer les données pour le Pokémon ID {pokemon.api_id}")
                continue  # Passer au Pokémon suivant

            stats = pokemon_data.get('stats', [])
            stats_formatted = [{"stat_name": stat["stat"]["name"], "base_stat": stat["base_stat"]} for stat in stats]

            pokemon_with_stats = {
                "name": pokemon.name,
                "api_id": pokemon.api_id,
                "trainer_id": pokemon.trainer_id,
                "stats": stats_formatted
            }
            result.append(pokemon_with_stats)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des Pokémons : {str(e)}")