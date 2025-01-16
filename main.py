from fastapi import FastAPI
from app.routers import trainers, pokemons, items, battle

# Création de l'application FastAPI
app = FastAPI()

# Inclure le routeur des entraîneurs avec le préfixe '/trainers'
@app.get("/trainers")
def include_trainers_router():
    """
    Inclut les routes pour les entraîneurs dans l'application.
    Ce routeur gère les actions relatives aux entraîneurs, telles que la création, la gestion et la consultation des dresseurs de Pokémon.

    Le préfixe pour toutes les routes d'entraîneur sera '/trainers'.
    """
    app.include_router(trainers.router, prefix="/trainers")

# Inclure le routeur des objets avec le préfixe '/items'
@app.get("/items")
def include_items_router():
    """
    Inclut les routes pour les objets dans l'application.
    Ce routeur gère les actions relatives aux objets, permettant aux entraîneurs de les gérer ou de les utiliser.

    Le préfixe pour toutes les routes d'objets sera '/items'.
    """
    app.include_router(items.router, prefix="/items")

# Inclure le routeur des pokémons avec le préfixe '/pokemons'
@app.get("/pokemons")
def include_pokemons_router():
    """
    Inclut les routes pour les Pokémons dans l'application.
    Ce routeur gère les actions liées aux Pokémons, telles que l'ajout, la modification et la consultation des Pokémon d'un dresseur.

    Le préfixe pour toutes les routes de Pokémon sera '/pokemons'.
    """
    app.include_router(pokemons.router, prefix="/pokemons")

# Inclure le routeur des combats avec le préfixe '/battle'
@app.get("/battle")
def include_battle_router():
    """
    Inclut les routes pour les combats de Pokémon dans l'application.
    Ce routeur gère les actions liées aux combats entre les Pokémons des dresseurs.

    Le préfixe pour toutes les routes de combat sera '/battle'.
    """
    app.include_router(battle.router, prefix="/battle")