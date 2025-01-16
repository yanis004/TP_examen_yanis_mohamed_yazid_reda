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