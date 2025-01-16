import requests

base_url = "https://pokeapi.co/api/v2"

def get_pokemon_name(api_id):
    """
        Get a pokemon name from the API pokeapi
    """
    return get_pokemon_data(api_id)['name']

def get_pokemon_stats(api_id):
    """
        Get pokemon stats from the API pokeapi
    """
    return False

def get_pokemon_data(api_id):
    """
        Get data of pokemon name from the API pokeapi
    """
    return requests.get(f"{base_url}/pokemon/{api_id}", timeout=10).json()


def battle_pokemon(first_api_id, second_api_id):
    """
        Do battle between 2 pokemons
    """
    premier_pokemon = get_pokemon_data(first_api_id)
    second_pokemon = get_pokemon_data(second_api_id)
    battle_result = 0
    return premier_pokemon if battle_result > 0 else second_pokemon if battle_result < 0 else {'winner': 'draw'}


def battle_compare_stats(first_pokemon_stats, second_pokemon_stats):
    """
        Compare given stat between two pokemons
    """
    stats_1 = first_pokemon_stats['stats']
    stats_2 = second_pokemon_stats['stats']
    result = 0
    for stat_1, stat_2 in zip(stats_1, stats_2):
        if stat_1['base_stat'] > stat_2['base_stat']:
            result += 1
        elif stat_1['base_stat'] < stat_2['base_stat']:
            result -= 1
    return result