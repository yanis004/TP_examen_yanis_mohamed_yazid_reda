from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from .sqlite import Base

class Trainer(Base):
    """
    Représente un dresseur de Pokémon.

    Attributs:
        id (int): L'identifiant unique du dresseur dans la base de données.
        name (str): Le nom du dresseur.
        birthdate (date): La date de naissance du dresseur.
        inventory (list): Liste des objets appartenant au dresseur (relation avec la classe Item).
        pokemons (list): Liste des Pokémons appartenant au dresseur (relation avec la classe Pokemon).
    """
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    birthdate = Column(Date)

    # Relation avec les objets (Items)
    inventory = relationship("Item", back_populates="trainer")
    # Relation avec les Pokémons
    pokemons = relationship("Pokemon", back_populates="trainer")

class Pokemon(Base):
    """
    Représente un Pokémon.

    Attributs:
        id (int): L'identifiant unique du Pokémon dans la base de données.
        api_id (int): L'ID du Pokémon provenant de l'API PokeAPI.
        name (str): Le nom du Pokémon.
        custom_name (str): Le nom personnalisé du Pokémon, si défini par l'utilisateur.
        trainer_id (int): L'identifiant du dresseur auquel ce Pokémon appartient.
        trainer (Trainer): L'objet dresseur auquel ce Pokémon est lié (relation avec la classe Trainer).
    """
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(Integer, index=True)
    name = Column(String, index=True)
    custom_name = Column(String, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))

    # Relation avec le dresseur (Trainer)
    trainer = relationship("Trainer", back_populates="pokemons")

class Item(Base):
    """
    Représente un objet appartenant à un dresseur de Pokémon.

    Attributs:
        id (int): L'identifiant unique de l'objet.
        name (str): Le nom de l'objet.
        description (str): La description de l'objet.
        trainer_id (int): L'identifiant du dresseur auquel cet objet appartient.
        trainer (Trainer): L'objet dresseur auquel cet objet est lié (relation avec la classe Trainer).
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))

    # Relation avec le dresseur (Trainer)
    trainer = relationship("Trainer", back_populates="inventory")