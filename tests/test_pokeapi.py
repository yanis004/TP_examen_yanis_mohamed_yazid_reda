import pytest
from unittest.mock import patch
import requests
from app.utils.pokeapi import get_pokemon_data, battle_pokemon, get_pokemon_name

def test_get_pokemon_data():
    mock_pokemon_data = {
        "name": "pikachu",
        "stats": [
            {"base_stat": 35, "stat": {"name": "hp"}},
            {"base_stat": 55, "stat": {"name": "attack"}}
        ]
    }
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_pokemon_data
        result = get_pokemon_data(25)
        
        assert result["name"] == "pikachu"
        assert len(result["stats"]) == 2
        mock_get.assert_called_once_with("https://pokeapi.co/api/v2/pokemon/25", timeout=10)

def test_battle_pokemon():
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

def test_get_pokemon_name():
    mock_pokemon_data = {"name": "bulbasaur"}
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_pokemon_data
        name = get_pokemon_name(1)
        
        assert name == "bulbasaur"
        mock_get.assert_called_once_with("https://pokeapi.co/api/v2/pokemon/1", timeout=10)

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
        
        assert result['winner'] == 'draw'

def test_get_pokemon_data_timeout():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout
        with pytest.raises(requests.exceptions.Timeout):
            get_pokemon_data(25)