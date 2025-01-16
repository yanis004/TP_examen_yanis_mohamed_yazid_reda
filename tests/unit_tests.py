<<<<<<< HEAD
from unittest.mock import patch
from app.utils import battle_pokemon  # Assurez-vous que le chemin est correct

def test_battle_pokemon_winner():
    # Simulez une bataille entre deux Pokémon
    result = battle_pokemon(25, 79)
    # Vérifiez que le gagnant est bien "pikachu"
    assert result["winner"] == "pikachu"

def test_battle_pokemon_first_not_found():
    # Simulez le cas où le premier Pokémon n'est pas trouvé
    with patch('app.utils.pokeapi.get_pokemon_data', side_effect=[None, {"name": "slowpoke"}]):
        result = battle_pokemon(999, 79)
        # Vérifiez que le résultat contient une erreur appropriée
        assert "error" in result
        assert result["error"] == "First Pokémon not found"

def test_battle_pokemon_second_not_found():
    # Simulez le cas où le second Pokémon n'est pas trouvé
    with patch('app.utils.pokeapi.get_pokemon_data', side_effect=[{"name": "pikachu"}, None]):
        result = battle_pokemon(25, 999)
        # Vérifiez que le résultat contient une erreur appropriée
        assert "error" in result
        assert result["error"] == "Second Pokémon not found"

def test_battle_pokemon_both_not_found():
    # Simulez le cas où aucun des deux Pokémon n'est trouvé
    with patch('app.utils.pokeapi.get_pokemon_data', side_effect=[None, None]):
        result = battle_pokemon(999, 888)
        # Vérifiez que le résultat contient une erreur appropriée
        assert "error" in result
        assert result["error"] == "Both Pokémons not found"
=======
import pytest
from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, actions
from app.sqlite import Base, engine, SessionLocal
from app.create_pokemon import add_pokemon
from app.routers.battle import compare_pokemon_stats

class TestPokemonCreation:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Configure la base de données pour les tests"""
        Base.metadata.drop_all(bind=engine)  
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()
        
        yield
        
        self.db.close()
        Base.metadata.drop_all(bind=engine)

    def test_add_new_pokemon(self):
        """Test l'ajout d'un nouveau Pokémon"""
        # Arrange
        trainer_data = schemas.TrainerCreate(
            name="Ash",
            birthdate=date(2000, 1, 1)
        )
        trainer = actions.create_trainer(self.db, trainer_data)

        pokemon_data = schemas.PokemonCreate(
            api_id=25,
            custom_name="Pikachu",
            trainer_id=trainer.id 
        )
        
        try:
            # Act
            pokemon = add_pokemon(self.db, pokemon_data)
            
            # Assert
            assert pokemon.api_id == 25
            assert pokemon.custom_name == "Pikachu"
            assert pokemon.name == "Pikachu"
            assert pokemon.trainer_id == trainer.id  # Vérifie que le trainer_id est correct

        except HTTPException as e:
            pytest.fail(f"Le test a échoué avec l'erreur: {str(e)}")

class TestPokemonBattle:
    def test_compare_pokemon_stats(self):
        """Test la comparaison des stats entre deux Pokémons"""
        # Arrange
        pokemon_1 = {
            "name": "Pikachu",
            "stats": [
                {"base_stat": 35},  # HP
                {"base_stat": 55},  # Attack
                {"base_stat": 40},  # Defense
                {"base_stat": 50},  # Sp. Attack
                {"base_stat": 50},  # Sp. Defense
                {"base_stat": 90}   # Speed
            ]
        }

        pokemon_2 = {
            "name": "Bulbasaur",
            "stats": [
                {"base_stat": 45},  # HP
                {"base_stat": 49},  # Attack
                {"base_stat": 49},  # Defense
                {"base_stat": 65},  # Sp. Attack
                {"base_stat": 65},  # Sp. Defense
                {"base_stat": 45}   # Speed
            ]
        }

        try:
            # Act
            result = compare_pokemon_stats(pokemon_1, pokemon_2)

            # Assert
            assert isinstance(result, dict)
            assert "pokemon_1_score" in result
            assert "pokemon_2_score" in result
            assert "winner" in result
            assert result["pokemon_1_score"] == 2  # Pikachu gagne en Attack et Speed
            assert result["pokemon_2_score"] == 4  # Bulbasaur gagne en HP, Defense, Sp.Attack, Sp.Defense
            assert result["winner"].lower() == "bulbasaur"  # Comparaison insensible à la casse

        except Exception as e:
            pytest.fail(f"Le test a échoué avec l'erreur: {str(e)}")

    def test_compare_pokemon_stats_draw(self):
        """Test un match nul entre deux Pokémons"""
        # Arrange
        pokemon_1 = {
            "name": "Pikachu",
            "stats": [
                {"base_stat": 50},
                {"base_stat": 50},
                {"base_stat": 50}
            ]
        }

        pokemon_2 = {
            "name": "Bulbasaur",
            "stats": [
                {"base_stat": 50},
                {"base_stat": 50},
                {"base_stat": 50}
            ]
        }

        try:
            # Act
            result = compare_pokemon_stats(pokemon_1, pokemon_2)

            # Assert
            assert result["pokemon_1_score"] == 0
            assert result["pokemon_2_score"] == 0
            assert result["winner"] == "Draw"

        except Exception as e:
            pytest.fail(f"Le test a échoué avec l'erreur: {str(e)}")

class TestTrainers:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Configure la base de données pour les tests"""
        Base.metadata.drop_all(bind=engine) 
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()
        yield
        self.db.close()
        Base.metadata.drop_all(bind=engine)

    def test_create_trainer(self):
        """Test la création d'un dresseur"""
        # Arrange
        trainer_data = schemas.TrainerCreate(
            name="Ash Ketchum",
            birthdate=date(2000, 1, 1)
        )

        try:
            # Act
            trainer = actions.create_trainer(self.db, trainer_data)

            # Assert
            assert trainer.name == "Ash Ketchum"
            assert trainer.birthdate == date(2000, 1, 1)
            assert isinstance(trainer.id, int)
            assert hasattr(trainer, 'pokemons')
            assert len(trainer.pokemons) == 0

        except HTTPException as e:
            pytest.fail(f"Le test a échoué avec l'erreur: {str(e)}")

    def test_get_trainers(self):
        """Test la récupération de tous les dresseurs"""
        # Arrange
        trainers_data = [
            schemas.TrainerCreate(name="Ash", birthdate=date(2000, 1, 1)),
            schemas.TrainerCreate(name="Misty", birthdate=date(2000, 2, 2)),
            schemas.TrainerCreate(name="Brock", birthdate=date(2000, 3, 3))
        ]

        for trainer_data in trainers_data:
            actions.create_trainer(self.db, trainer_data)

        try:
            # Act
            trainers = actions.get_trainers(self.db, skip=0, limit=100)

            # Assert
            assert len(trainers) == 3
            assert trainers[0].name == "Ash"
            assert trainers[1].name == "Misty"
            assert trainers[2].name == "Brock"

        except HTTPException as e:
            pytest.fail(f"Le test a échoué avec l'erreur: {str(e)}")
>>>>>>> e36988e419528aacb858ba4297f51a4bc098a785
