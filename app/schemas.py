from datetime import date
from typing import  List, Optional, Union
from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel

#
#  ITEM
#
class ItemBase(BaseModel):
    name: str
    description: Union[str, None] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    trainer_id: int

    class Config:
        orm_mode = True

#
#  POKEMON
#
class PokemonBase(BaseModel):
    api_id: int
    custom_name: Optional[str] = None

class PokemonCreate(PokemonBase):
    api_id: int
    custom_name: Optional[str]
    trainer_id: int  

class Pokemon(PokemonBase):
    id: int
    name: str
    trainer_id: int

    class Config:
        orm_mode = True
#
#  TRAINER
#
class TrainerBase(BaseModel):
    name: str
    birthdate: date

class TrainerCreate(TrainerBase):
    pass

class Trainer(TrainerBase):
    id: int
    inventory: List[Item] = []
    pokemons: List[Pokemon] = []

    class Config:
        orm_mode = True

class Stat(BaseModel):
    stat_name: str
    base_stat: int

class PokemonWithStats(BaseModel):
    name: str
    api_id: int
    trainer_id: int
    stats: List[Stat]

    class Config:
        orm_mode = True