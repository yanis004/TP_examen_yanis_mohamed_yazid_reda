import os
import sys
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.utils.utils import get_db
from app import models, schemas


def add_pokemon(database: Session, pokemon_data: schemas.PokemonCreate):
    """
    Ajoute un Pokémon à la base de données.

    Args:
        database (Session): Session de la base de données.
        pokemon_data (schemas.PokemonCreate): Les données du Pokémon à ajouter.

    Returns:
        models.Pokemon: Le Pokémon ajouté.
    """
    try:
        # Vérifier si un Pokémon avec le même api_id existe déjà dans la base
        existing_pokemon = database.query(models.Pokemon).filter(models.Pokemon.api_id == pokemon_data.api_id).first()
        if existing_pokemon:
            raise HTTPException(status_code=400, detail=f"Le Pokémon avec l'ID {pokemon_data.api_id} existe déjà.")

        # Créer un nouvel objet Pokémon
        db_pokemon = models.Pokemon(
            name=pokemon_data.custom_name or "Default Name",  # Si custom_name est NULL, utiliser "Default Name"
            api_id=pokemon_data.api_id,  # api_id fourni par l'utilisateur
            custom_name=pokemon_data.custom_name,  # Assigner le nom personnalisé (si donné)
            trainer_id=pokemon_data.trainer_id  # Assigner trainer_id
        )
        # Ajouter le Pokémon à la base de données
        database.add(db_pokemon)
        database.commit()
        database.refresh(db_pokemon)
        return db_pokemon
    except Exception as e:
        # Gérer toute exception qui pourrait survenir pendant l'insertion
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'ajout du Pokémon : {str(e)}")

def create_pokemons():
    """
    Crée et ajoute plusieurs Pokémons à la base de données.
    """
    try:
        # Utilisation d'un contexte de session pour garantir la gestion correcte de la session
        with next(get_db()) as database:
            # Liste des Pokémons à créer
            pokemons_data = [
                {"api_id": 25, "custom_name": "Pikachu", "trainer_id": 1},
                {"api_id": 1, "custom_name": "Bulbasaur", "trainer_id": 1},
                {"api_id": 4, "custom_name": "Charmander", "trainer_id": 1},
                {"api_id": 7, "custom_name": "Squirtle", "trainer_id": 2},
                {"api_id": 23, "custom_name": "Eevee", "trainer_id": 2},
            ]
            
            # Ajouter chaque Pokémon à la base de données
            for pokemon_data in pokemons_data:
                add_pokemon(database, schemas.PokemonCreate(**pokemon_data))
        
            print("Pokémons ajoutés avec succès !")
    except Exception as e:
        print(f"Erreur lors de l'ajout des Pokémons: {str(e)}")

create_pokemons()