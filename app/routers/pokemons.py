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
    try:
        # Récupérer tous les Pokémons de la base de données
        pokemons = database.query(models.Pokemon).all()

        if not pokemons:
            raise HTTPException(status_code=404, detail="Aucun Pokémon disponible dans la base de données.")

        # Sélectionner aléatoirement 3 Pokémons (ou moins si la base contient moins de 3 entrées)
        random_pokemons = random.sample(pokemons, min(len(pokemons), 3))

        # Récupérer les statistiques des Pokémons depuis l'API
        result = []
        for pokemon in random_pokemons:
            pokemon_data = get_pokemon_data(pokemon.api_id)
            
            if not pokemon_data:
                print(f"Impossible de récupérer les données pour le Pokémon ID {pokemon.api_id}")
                continue  # Passer au Pokémon suivant

            # Extraire et formater les statistiques
            stats = pokemon_data.get('stats', [])
            stats_formatted = [{"stat_name": stat["stat"]["name"], "base_stat": stat["base_stat"]} for stat in stats]

            pokemon_with_stats = {
                "name": pokemon.name,
                "api_id": pokemon.api_id,
                "trainer_id": pokemon.trainer_id,
                "stats": stats_formatted
            }
            result.append(pokemon_with_stats)

        if not result:
            raise HTTPException(status_code=500, detail="Les statistiques des Pokémons n'ont pas pu être récupérées.")

        return result

    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des Pokémons : {str(e)}")