
# Créez une plateforme pour amateurs de Nutella

*Parcours développeur d'application Python : OpenClassrooms Projet n°8*

### Sujet du projet

La startup **Pur Beurre**, avec laquelle vous avez déjà travaillé, souhaite développer une plateforme web à destination de ses clients. Ce site permettra à quiconque de trouver un substitut sain à un aliment considéré comme "*Trop gras, trop sucré, trop salé*" (même si nous savons tous que le gras c'est la vie).

Pour mener à bien ce projet, un cahier des charges fourni par la startup **PurBeurre** est mis à disposition. Celui-ci indique principalement les attentes du client concernant l'aspect graphique de l'application et certaines indications sur son fonctionnement. 

## Structure du projet

Concernant la mise en place de ce projet, il était demandé de créer une application Web permettant à un utilisateur de rechercher un aliment de son choix et de lui proposer en retour, des substituts considérés comme étant meilleurs pour la santé. L'utilisateur s'il le souhaite, a également la possibilité d'enregistrer dans ses produits favoris, les aliments qu'il juge intéressant.
A savoir que pour utiliser cette application, l'utilisateur doit préalablement s'enregistrer puis s'authentifier.

L'application devait être développée en **Python** en utilisant notamment le **framework Django**. Un **template Bootstrap** était imposé dans le cahier des charges, il a donc fallut l'intégrer au projet. 
**HTML5, CSS3 et Bootstrap4** ont été utilisés pour, entre autres, la partie graphique de l'application.

Lors de l'ouverture de l'application, l'utilisateur se retrouve face à la page d'accueil dans laquelle il est indiqué qu'il est nécessaire de s'authentifier pour utiliser l'application. 

* **Users** : 

L'utilisateur est invité à s'enregistrer puis une fois le formulaire saisie et valide, il est redirigé vers la page d'accueil en étant automatiquement connecté. Cette fonctionnalité est parfaitement intégrée à Django et se met très facilement en place. Elle permet notamment de vérifier aisément qu'un utilisateur est connecté et d'interagir avec le modèle **User** (intégré par défaut dans Django). Dans le projet, cette partie est traitée par l'application **Users**.

* **Products** : 

L'application **Products** est en quelque sorte le coeur du projet. C'est ici que sont gérées toutes les parties faisant références aux produits, catégories etc…
Une fois l'utilisateur authentifié, il a la possibilité de rechercher un produit. Une fois le produit de son choix sélectionné, l'application lui propose différents substituts ayant un **nutriscore** au moins équivalent ou meilleur. 
L'utilisateur a alors la possibilité d'enregistrer ce produit ou de consulter les fiches "détail" de ces produits. 

* **Favorites** : 

Lors d'une recherche produit et de la consultation des substituts proposés, l'utilisateur a la possibilité d'enregistrer le substituts pour l'ajouter à ses favoris. Il peut ensuite, dans un espace nommé **"Mes produits"**, consulter tous les produits qui ont déjà été ajoutés aux favoris. Il peut ensuite, s'il le souhaite, consulter les fiches détaillés de ces produits, voir directement sur le site **OpenFoodFacts** qui fournit la base de données de l'application.  

* **Remplissage de la base de données** : 

Pour fonctionner, l'application exploite une base de données (**PostgreSQL**), dont un script de remplissage permet de fournir les tables **Category** et **Product** de la base. Ces deux scripts peuvent être appelés grâce aux commandes :

        python manage.py fill_db_categories
        python manage.py fill_db_products

La première va donc permettre d'ajouter des catégories dans notre base en se basant sur des conditions définies dans le script (*voir documentation du script pour plus de détail*). La seconde permet, pour sa part, d'ajouter des produits dans les catégories précédemment enregistrées dans la base (*voir documentation du script pour plus de détail*).

## Installation du projet

Pour la mise en place du projet, il est recommandé de créer un **environnement virtuel python**. Les commandes ci-dessous sont à adapter selon le système d'exploitation utilisé. Il faut également avoir préalablement installé les dépendances éventuellement nécessaires.

A savoir que le projet a été testé sur des versions **3.6** et **3.7** de **Python**. Il est donc recommandé de créer un environnement virtuel basé sur une version compatible.

1. **Installation de l'environnement virtuel** : 

        Python -m venv (nom_environnement)

2. **Clonage du projet à l'intérieur de l'environnement virtuel** :

        Git clone git@github.com:Eidocode/OC_Project8.git
        
3. **Activation de l'environnement virtuel depuis la racine** :

        ./Scripts/activate
        
4. **Installation des dépendances (à adapter selon l'OS)** :

        pip install -r requirements.txt
        
5. **Configuration de l'application** :

Pour fonctionner, l'application utilise des variables d'environnement qui sont appelées dans le fichier de configuration du projet **[setting.py](https://github.com/Eidocode/OC_Project8/blob/main/purbeurre_project/settings.py)**.
Une première variable **['SECRET_KEY']** qui doit être générée aléatoirement et liée uniquement à l'installation en cours du projet. Il est indispensable que cette clé ne soit pas visible ou facilement accessible.
Pour la générer, il est possible de le faire directement depuis une **console Python** de la façon suivante : 

        >>> import random, string
        >>> "".join(random.choice(string.printable) for _ in range(24))

Une seconde variable **['ENV']** aura comme valeur **'PRODUCTION'** si le déploiement a lieu sur un serveur de production. Cela dans le but d'avoir un seul fichier de configuration quelque soit le type d'environnement dans lequel l'application est installé.

6. **Execution de l'environnement Django** :

        python manage.py runserver

L'application **Django** est alors exécutée. Il ne reste qu'à ouvrir un navigateur et se rendre à l'adresse **127.0.0.1:8000** ou **localhost:8000**


## Déploiement de l'application

L'application a été déployée sur la plateforme d'hébergement **Heroku**, nous pouvons la retrouver à l'adresse suivante : [https://app-purbeurre.herokuapp.com/](https://app-purbeurre.herokuapp.com/)

Pour effectuer ce déploiement, il suffit de suivre, simplement, la documentation fournit à ce sujet. Elle est consultable à l'adresse suivante [https://devcenter.heroku.com/articles/getting-started-with-python](https://devcenter.heroku.com/articles/getting-started-with-python)

Certaines précisions sont apportées pour les applications **Django** à l'adresse suivante : [https://devcenter.heroku.com/articles/deploying-python](https://devcenter.heroku.com/articles/deploying-python)

Concernant les variables d'environnement, elles sont nommées **Config Vars** sur **Heroku**. C'est précisément ce que l'on utilisera pour configurer nos variables d'environnement précédemment citées.
Il suffit donc de déclarer ces variables (dans l'environnement **Heroku**) de la façon suivante : 
***A savoir qu'il est également possible de le faire depuis le dashboard du projet***

        heroku config:set SECRET_KEY=(Valeur de la variable)
        heroku config:set ENV=(Valeur de la variable)

Comme indiqué précédemment, ces variables d'environnement sont appelées dans le fichier **[settings.py](https://github.com/Eidocode/OC_Project8/blob/main/purbeurre_project/settings.py)** de l'application, de la façon suivante : 

        import os
        
        SECRET_KEY = os.environ['SECRET_KEY']
        ENV = os.environ.get('ENV')

## Tests unitaires et fonctionnels

Des tests unitaires et fonctionnels sont disponibles dans le répertoire **[./products/tests](https://github.com/Eidocode/OC_Project8/tree/main/products/tests)** ainsi qu'à la racine de l'application **[Users](https://github.com/Eidocode/OC_Project8/tree/main/users)**

**[test_forms.py](https://github.com/Eidocode/OC_Project8/blob/main/products/tests/test_forms.py)** : Tests unitaires des formulaires

**[test_models.py](https://github.com/Eidocode/OC_Project8/blob/main/products/tests/test_models.py)** : Tests unitaires des modèles

**[test_views.py](https://github.com/Eidocode/OC_Project8/blob/main/products/tests/test_views.py)** : Tests unitaires des vues

Un test fonctionnel nommée **[test_user_experience.py](https://github.com/Eidocode/OC_Project8/blob/main/users/test_user_experience.py)** est également disponible à la racine du répertoire **Users**. Il permet notamment de tester le parcours d'un utilisateur sur l'application. En commençant par l'inscription, l'authentification, la recherche d'un produit, l'ajout d'un substitut dans les favoris, la suppression d'un favoris puis la déconnexion. 
Cela afin de s'assurer que les différents éléments fonctionnent correctement ensemble.
