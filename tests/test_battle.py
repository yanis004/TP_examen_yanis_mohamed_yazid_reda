import pytest
from unittest.mock import patch
from app.utils.pokeapi import battle_pokemon

def test_battle_pokemon_winner():
    mock_pokemon1 = {
        "name": "pikachu",
        "stats": [{"base_stat": 60, "stat": {"name": "speed"}}]
    }
    mock_pokemon2 = {
        "name": "slowpoke",
        "stats": [{"base_stat": 30, "stat": {"name": "speed"}}]
    }

    with patch('app.utils.pokeapi.get_pokemon_data') as mock_get:
        mock_get.side_effect = [mock_pokemon1, mock_pokemon2]
        result = battle_pokemon(25, 79)
        
        assert result["winner"] == "pikachu"

def test_battle_pokemon_draw():
    mock_pokemon1 = {
        "name": "pikachu",
        "stats": [{"base_stat": 50, "stat": {"name": "speed"}}]
    }
    mock_pokemon2 = {
        "name": "charmander",
        "stats": [{"base_stat": 50, "stat": {"name": "speed"}}]
    }

    with patch('app.utils.pokeapi.get_pokemon_data') as mock_get:
        mock_get.side_effect = [mock_pokemon1, mock_pokemon2]
        result = battle_pokemon(25, 4)
        
        assert result["winner"] == "draw"

def test_battle_pokemon_first_not_found():
    with patch('app.utils.pokeapi.get_pokemon_data', side_effect=[None, {"name": "slowpoke"}]):
        result = battle_pokemon(999, 79)
        
        assert result["error"] == "First Pokémon not found"

def test_battle_pokemon_second_not_found():
    with patch('app.utils.pokeapi.get_pokemon_data', side_effect=[{"name": "pikachu"}, None]):
        result = battle_pokemon(25, 999)
        
        assert result["error"] == "Second Pokémon not found"