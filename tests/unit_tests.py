import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.create_pokemon import add_pokemon
from app import models, schemas
from app.sqlite import Base, engine, SessionLocal

class TestPokemonCreation:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Configure la base de données pour les tests"""
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()
        
        yield
        
        self.db.close()
        Base.metadata.drop_all(bind=engine)

    def test_add_new_pokemon(self):
        """Test l'ajout d'un nouveau Pokémon"""
        # Arrange
        class ExtendedPokemonCreate(schemas.PokemonCreate):
            trainer_id: int = 1

        pokemon_data = ExtendedPokemonCreate(
            api_id=25,
            custom_name="Pikachu"
        )
        
        try:
            # Act
            pokemon = add_pokemon(self.db, pokemon_data)
            
            # Assert
            assert pokemon.api_id == 25
            assert pokemon.custom_name == "Pikachu"
            assert pokemon.name == "Pikachu"
            assert pokemon.trainer_id == 1

        except HTTPException as e:
            pytest.fail(f"Le test a échoué avec l'erreur: {str(e)}")

    def test_get_pokemon(self):
        """Test la récupération d'un Pokémon"""
        # Arrange - Créer d'abord un Pokémon
        class ExtendedPokemonCreate(schemas.PokemonCreate):
            trainer_id: int = 1

        pokemon_data = ExtendedPokemonCreate(
            api_id=25,
            custom_name="Pikachu"
        )
        
        try:
            # Créer le Pokémon
            created_pokemon = add_pokemon(self.db, pokemon_data)
            
            # Act - Récupérer le Pokémon
            found_pokemon = self.db.query(models.Pokemon).filter(
                models.Pokemon.api_id == pokemon_data.api_id
            ).first()
            
            # Assert
            assert found_pokemon is not None
            assert found_pokemon.api_id == 25
            assert found_pokemon.custom_name == "Pikachu"
            assert found_pokemon.name == "Pikachu"
            assert found_pokemon.trainer_id == 1

        except HTTPException as e:
            pytest.fail(f"Le test a échoué avec l'erreur: {str(e)}")

class TestPokemonBattle:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Configure la base de données pour les tests"""
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()
        
        yield
        
        self.db.close()
        Base.metadata.drop_all(bind=engine)

    def test_compare_pokemon_stats(self):
        """Test la comparaison des stats entre deux Pokémons"""
        from app.routers.battle import compare_pokemon_stats  # Import local si nécessaire
        
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
            assert result["pokemon_1_score"] == 1  # Pikachu gagne en vitesse
            assert result["pokemon_2_score"] == 5  # Bulbasaur gagne en HP, Def, SpA, SpD
            assert result["winner"] == "bulbasaur"  # Le nom est en minuscules dans l'API

        except Exception as e:
            pytest.fail(f"Le test a échoué avec l'erreur: {str(e)}")

    def test_compare_pokemon_stats_draw(self):
        """Test un match nul entre deux Pokémons"""
        from app.routers.battle import compare_pokemon_stats  # Import local si nécessaire
        
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