# UE-AD-A1-MIXTE

### Zuoyu Zhang & Maxime Garnier

#### nous avons faites le TP vert pour TP MISTE, nous allons expliquer comment démarrer notre application dans Docker: 

nécessité : 
- Docker
- Docker compose
- Git 

**Note:** Older versions of Docker Compose used the `docker-compose` command. Newer versions use `docker compose`.

**Optionnel:** Pour accélérer le processus de construction, téléchargez les images Docker préconstruites depuis GitHub :

```
docker pull zzy2524/microservicestpmixte-movie:latest
docker pull zzy2524/microservicestpmixte-showtime:latest
docker pull zzy2524/microservicestpmixte-booking:latest
docker pull zzy2524/microservicestpmixte-user:latest
```

Processus :

1. Allez d'abord sur le site GitHub et téléchargez tout le code dont vous avez besoin à l'aide de la commande : `git clone https://github.com/maxime-cool/microservices-TP-mixte.git`

2. Allez dans le dossier du code téléchargé dans le terminal : `cd microservices-TP-mixte`

3. (Vous pouvez sauter cette étape si vous avez déjà retiré les images ci-dessus) Dans le répertoire de projet, exécutez la commande `docker-compose build` pour construire les images Docker pour les services. Cette commande construira les images en fonction des fichiers Dockerfile spécifiés dans le fichier `docker-compose.yml`.

4. Lancer vos services : Une fois que les images sont construites, vous pouvez lancer vos services avec Docker Compose en utilisant la commande `docker-compose up`. Si vous souhaitez exécuter les services en arrière-plan, utilisez l'option `-d` : `docker-compose up -d`

5. Vérifiez l'état de vos services : Utilisez `docker-compose ps` pour vérifier l'état de vos services en cours d'exécution.

6. Vous pouvez arrêter les conteneurs avec `docker compose stop` ou les détruire avec `docker compose down`.
