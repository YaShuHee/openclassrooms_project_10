# [EN] OpenClassrooms - Project 10 : LITReview
An app to ask and to post books reviews.

## How to run the application
### Installation
1. Install [Python 3.10](https://www.python.org/downloads/).
2. Download the sources or clone this repository : ```git clone https://github.com/YaShuHee/openclassrooms_project_10```.
3. Go at the project root : ```cd openclassrooms_project_10```.
4. Create a virtual environment :
    - on Windows : ```py -3 -m venv env```,
    - on Linux/macOS : ```python -m venv env```.
5. Activate the virtual environment :
    - on windows (from [PowerShell](https://docs.microsoft.com/fr-fr/powershell/)): ```. .\env\Scripts\activate```,
    - on Linux/macOS : ```. ./env/bin/activate```.
6. Install the project dependencies in the virtual environment : ```pip install -r requirements.txt```.
7. You can now activate the virtual environment you just created each time you need to run the app.
When you have finished using it, you can run ```deactivate``` to exit the virtual environment.

### Execution
1. Follow the previous installation steps.
2. Go at the root of the project (.../openclassrooms_project_10/).
3. Activate the virtual environment.
4. Run ```python ./manage.py makemigrations```
5. Run ```python ./manage.py migrate```
6. Run ```python ./manage.py runserver```.
7. You can now consult send request to the API at the address [http://localhost:8000/api/](http://localhost:8000/api/).
8. The endpoints can be found in my [Postman API documentation](https://documenter.getpostman.com/view/17882904/UV5ZBbkc).


# [FR] OpenClassrooms - Projet 10 : LITReview
Une application pour demander et poster des critiques de livres.

## Comment lancer l'application
### Installation
1. Installez [Python 3.10](https://www.python.org/downloads/).
2. Téléchargez le code ou clone le dépôt : ```git clone https://github.com/YaShuHee/openclassrooms_project_10```.
3. Allez à la racine du projet : ```cd openclassrooms_project_10```.
4. Créez un environnement virtuel :
    - sur Windows : ```py -3 -m venv env```,
    - sur Linux/macOS : ```python -m venv env```.
5. Activez l'environnement virtuel :
    - sur windows (dans [PowerShell](https://docs.microsoft.com/fr-fr/powershell/)): ```. .\env\Scripts\activate```,
    - sur Linux/macOS : ```. ./env/bin/activate```.
6. Installez les dépendances du projet dans l'environnement virtuel : ```pip install -r requirements.txt```.
7. Vous pouvez maintenant activer l'environnement virtuel que vous venez de créer à chaque fois que vous avez besoin d'exécuter l'application.
Quand vous avez fini de l'utiliser, vous pouvez désactiver l'environnement virtuel avec la commande  ```deactivate```.

### Exécution
1. Suivez les étapes d'installation.
2. Allez à la racine du projet (.../openclassrooms_project_10/).
3. Activez l'environnement virtuel.
4. Lancez la commande ```python ./manage.py makemigrations```.
5. Lancez la commande ```python ./manage.py migrate```.
6. Lancez la commande ```python ./manage.py runserver```.
7. Vous pouvez maintenant envoyer des requêtes à l'API à l'adresse [http://localhost:8000/api/](http://localhost:8000/api/).
8. Pour connaître les endpoints, vous pouvez consulter la [documentation Postman de mon API](https://documenter.getpostman.com/view/17882904/UV5ZBbkc).
