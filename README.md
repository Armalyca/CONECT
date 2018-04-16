# **Projet CONECT : Récupération des données**

**Contexte : Opérations d’Urgences de la Croix Rouge Française**  
Aujourd’hui la Croix Rouge Française s’appuie sur un réseau de volontaires formés et entraînés, présent sur l'ensemble du territoire , permettant une mobilisation et une mutualisation quasi-immédiates quel que soit le lieu de la catastrophe.  

La récolte et la transmission de l’information restent un enjeu essentiel de ces situations d’urgences. C’est en effet en fonction de la connaissance de la situation que l’état-major de crise prend les décisions qui seront mises en œuvre sur les lieux d’intervention. Les mesures engagées et leurs résultats font ensuite l’objet d’une évaluation, dont les conclusions serviront à leur tour de fondement pour de nouvelles prises de décision.  

A l’ère du numérique les dispositifs de gestion des risques et des crises doivent de plus en plus considérer les nouvelles technologies comme source d’information. C’est ainsi que s’est développé le concept de Médias Sociaux en Gestion d’Urgence qui décrit l’utilisation de ces nouveaux modes de communication pour pour crowdsourcer l’information.  

**CONECT**  
Le Centre des Opérations Numériques d’Écoute des Communications et Transmissions (CONECT) mis en place par la délégation départementale du Val-de-Marne de la Croix Rouge est  une « plate-forme de surveillance des médias sociaux » dédiée à l'aide humanitaire en cas de catastrophe sur le département.  

Le centre des opérations numériques est conçu pour repérer les tendances au cours d'une situation de catastrophe ou d'urgence en écoutant et en suivant des conversations en ligne sur Facebook, Twitter,les blogs et autres plates-formes afin d’identifier de manière proactive les besoins des sinistrés ou de leur famille.  
 
Les avantages de cette plate-forme incluent la possibilité d'interagir en temps réel et directement avec les communautés affectées afin de leur fournir des réponses aux questions, des informations en temps opportun, mais également de soutenir les équipes de secouristes sur le terrain selon les besoins.  

Aujourd’hui assurée par des bénévoles, cette veille informationnelle est donc limitée au temps et à la capacité de traitement des informations dont ils disposent. Aussi la nécessité d’automatiser ce processus s’est imposée.  

**Notre projet**  
Dans le cadre de ce projet global notre équipe s’attachera à la récupération des informations et de leur métadonnées sur les réseaux sociaux (Twitter dans un premier temps) en vu des les analyser (l’analyse sera réalisée par une seconde équipe). Le but est de récupérer des informations et des photos potentiellement pertinentes de par la présence de mots clés, leur émetteur(comptes vérifiés, compte de services publiques) et la localisation(ville/département/région/pays) de l'émetteur.
![](https://framapic.org/rvHX0fChK5lD/0tzYcNtoqzN0)
Le projet se décomposera donc ainsi :
* une interface de paramétrage des mots clés
  *interface web
  *base de donnée des mots clés
* le connecteur effectuant les requêtes vers Twitter
* mise en base des résultats de requêtes

Le projet utilisera plusieurs technologies :
* interface web en Flask
* le connecteur en python et s’appuiera sur tweep
* la base de données sera en MongoDB

Dans l'ordre nos objectifs sont:
1. développer le connecteur
2. développer un outil en ligne de commande
3. développer l'interface web
4. aider dans leur travail leur groupe en charge de l'analyse de la base de donné OU développer de nouveaux connecteurs pour d'autres réseaux sociaux
