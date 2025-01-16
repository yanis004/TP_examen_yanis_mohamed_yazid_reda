from locust import HttpUser, task, between
import random

class PokemonUser(HttpUser):
    wait_time = between(1, 5)  # Temps d'attente entre chaque requête (1 à 5 secondes)

    @task(1)
    def get_random_pokemons(self):
        """
        Test de l'endpoint `/pokemons/random` qui retourne 3 Pokémons aléatoires avec leurs statistiques.
        """
        response = self.client.get("/pokemons/random")
        
        # Vérification de la réponse (code 200 OK)
        if response.status_code == 200:
            print("Pokémons récupérés avec succès !")
        else:
            print(f"Erreur lors de la récupération des Pokémons: {response.status_code}")

    @task(2)
    def get_pokemons(self):
        """
        Une tâche supplémentaire pour tester un autre endpoint, comme `/pokemons/`.
        """
        response = self.client.get("/pokemons/")
        if response.status_code != 200:
            print(f"Erreur lors de la récupération des Pokémons : {response.status_code}")
