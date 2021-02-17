# Créez une plateforme pour amateurs de Nutella

*Parcours développeur d'application Python : OpenClassrooms Projet n°8

### Sujet du projet

La startup Pur Beurre, avec laquelle vous avez déjà travaillé, souhaite développer une plateforme web à destination de ses clients. Ce site permettra à quiconque de trouver un substitut sain à un aliment considéré comme "Trop gras, trop sucré, trop salé" (même si nous savons tous que le gras c'est la vie).

Pour mener à bien ce projet, un cahier des charges fourni par la Startup PurBeurre est mis à disposition. Celui-ci indique principalement les attentes du client concernant l'aspect graphique de l'application et certaines indications sur son fonctionnement. 

## Structure du projet

Concernant la mise en place de ce projet, il était demandé de créer une application Web permettant à un utilisateur de rechercher un aliment de son choix et de lui proposer en retour, des substituts considérés comme étant meilleurs pour la santé. L'utilisateur s'il le souhaite, a également la possibilité d'enregistrer dans ses produits favoris, les aliments qu'il juge intéressant.
A savoir que pour utiliser cette application, l'utilisateur doit préalablement s'enregistrer puis s'authentifier.

L'application devait être développée en Python en utilisant notamment le framework Django. Un template Bootstrap était imposé dans le cahier des charges, il a donc fallut l'intégrer au projet. 
HTML5, CSS3 et Bootstrap4 ont été utilisés pour, entre autres, la partie graphique de l'application.

Lors de l'ouverture de l'application, l'utilisateur se retrouve face à la page d'accueil dans laquelle il est indiqué qu'il est nécessaire de s'authentifier pour utiliser l'application. 

* Users : 

L'utilisateur est invité à s'enregistrer puis une fois le formulaire saisie et valide, il est redirigé vers la page d'accueil en étant automatiquement connecté. Cette fonctionnalité est parfaitement intégrée à Django et se met très facilement en place. Elle permet notamment de vérifier aisément qu'un utilisateur est connecté et d'interagir avec le modèle User (intégré par défaut dans Django). Dans le projet, cette partie est traitée par l'application Users.

* Products : 

L'application Products est en quelque sorte le coeur du projet. C'est ici que sont gérées toutes les parties faisant références aux produits, catégories etc…
Une fois l'utilisateur authentifié, il a la possibilité de rechercher un produit. Une fois le produit de son choix sélectionné, l'application lui propose différents substituts ayant un nutriscore au moins équivalent ou meilleur. 
L'utilisateur a alors la possibilité d'enregistrer ce produit ou de consulter les fiches "détail" de ces produits. 

* Favorites : 

Lors d'une recherche produit et de la consultation des substituts proposés, l'utilisateur a la possibilité d'enregistrer le substituts pour l'ajouter à ses favoris. Il peut ensuite, dans un espace nommé "Mes produits", consulter tous les produits qui ont déjà été ajoutés aux favoris. Il peut ensuite, s'il le souhaite, consulter les fiches détaillés de ces produits, voir directement sur le site OpenFoodFacts qui fournit la base de données de l'application.  

* Remplissage de la base de données : 

Pour fonctionner, l'application exploite une base de données (PostgreSQL), dont un script de remplissage permet de fournir les tables Category et Product de la base. Ces deux scripts peuvent être appelés grâce à la commande python manage.py fill_db_categories et python manage.py fill_db_products.
La première va donc permettre d'ajouter des catégories dans notre base en se basant sur des conditions définies dans le script (voir documentation du script pour plus de détail). La seconde permet, pour sa part, d'ajouter des produits dans les catégories précédemment enregistrées dans la base (voir documentation du script pour plus de détail).

## Installation du projet

Pour la mise en place du projet, il est recommandé de créer un environnement virtuel python. Les commandes ci-dessous sont à adapter selon le système d'exploitation utilisé. Il faut également avoir préalablement installé les dépendances éventuellement nécessaires.

A savoir que le projet a été testé sur des versions 3.6 et 3.7 de Python. Il est donc recommandé de créer un environnement virtuel basé sur une version compatible.

1. Installation de l'environnement virtuel : 

        Python -m venv (nom_environnement)

2. Clonage du projet à l'intérieur de l'environnement virtuel :

        Git clone git@github.com:Eidocode/OC_Project8.git
        
3. Activation de l'environnement virtuel depuis la racine :

        ./Scripts/activate
        
4. Installation des dépendances (à adapter selon l'OS) :

        pip install -r requirements.txt
        
5. Configuration de l'application :

    Pour fonctionner 


        

      


