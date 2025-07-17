# BlackBox Tools - Dashboard de Pentest

## 📋 Description

BlackBox Tools est un dashboard web personnel pour l'exécution et le suivi de scripts de pentest. Cette application permet d'exécuter des outils de sécurité dans une interface centralisée avec un design moderne inspiré du monde de la cybersécurité.

## ✨ Fonctionnalités

### 🔐 Sécurité
- Authentification administrateur sécurisée
- Sessions chiffrées
- Filtrage des entrées utilisateur
- Protection contre les injections de commandes

### 🛠️ Outils Intégrés
- **Nmap** : Scan de ports et détection d'OS
- **Whois** : Informations DNS et propriétaire de domaine
- **Dig** : Énumération DNS avancée
- **Traceroute** : Traçage de route réseau
- **Hydra** : Brute-force SSH/FTP (désactivé par sécurité)

### 📊 Interface
- Design moderne avec thème sombre
- Interface responsive (desktop/mobile)
- Console de résultats en temps réel
- Animations et effets visuels
- Horloge en temps réel
- Indicateurs de statut

### 📈 Historique
- Sauvegarde automatique des résultats
- Historique complet des exécutions
- Téléchargement de rapports (.txt)
- Statistiques d'utilisation

## 🚀 Installation et Utilisation

### Prérequis
```bash
# Installation des outils de pentest
sudo apt update
sudo apt install -y nmap whois dnsutils traceroute

# Python 3 et Flask
pip3 install flask
```

### Lancement
```bash
cd blackbox_tools
python3 app.py
```

L'application sera accessible sur : http://127.0.0.1:5000

### Connexion
- **Nom d'utilisateur** : `admin`
- **Mot de passe** : `admin_password`

⚠️ **Important** : Changez le mot de passe par défaut dans le fichier `app.py` ligne 13 pour un usage en production !

## 🎯 Utilisation

1. **Connexion** : Utilisez les identifiants admin pour accéder au dashboard
2. **Sélection de cible** : Entrez une adresse IP ou un nom de domaine
3. **Choix d'outil** : Sélectionnez l'outil de pentest à utiliser
4. **Paramètres** : Ajoutez des paramètres optionnels si nécessaire
5. **Exécution** : Cliquez sur "Lancer l'exécution"
6. **Résultats** : Consultez les résultats dans la console
7. **Historique** : Accédez à l'historique pour revoir les exécutions passées

## 🎨 Fonctionnalités Avancées

### Raccourcis Clavier
- `Ctrl + Entrée` : Exécuter le script sélectionné
- `Échap` : Effacer la console
- Double-clic sur la console : Copier le contenu

### Actions Rapides
- Effacement de la console
- Téléchargement direct des résultats
- Copie automatique vers le presse-papiers

## 📁 Structure du Projet

```
blackbox_tools/
├── app.py                 # Application Flask principale
├── database.db           # Base de données SQLite (créée automatiquement)
├── requirements.txt       # Dépendances Python
├── app/
│   ├── templates/        # Templates HTML
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── history.html
│   │   └── history_detail.html
│   └── static/          # Fichiers statiques
│       ├── style.css    # Styles personnalisés
│       └── script.js    # JavaScript interactif
└── README.md            # Ce fichier
```

## ⚠️ Avertissements de Sécurité

1. **Usage Autorisé Uniquement** : N'utilisez ces outils que sur des systèmes que vous possédez ou pour lesquels vous avez une autorisation explicite.

2. **Responsabilité** : L'utilisateur est entièrement responsable de l'usage qu'il fait de ces outils.

3. **Sécurité du Mot de Passe** : Changez immédiatement le mot de passe par défaut.

4. **Accès Réseau** : L'application écoute sur toutes les interfaces (0.0.0.0). En production, limitez l'accès.

5. **Logs** : Les exécutions sont enregistrées dans la base de données locale.

## 🔧 Personnalisation

### Modification du Mot de Passe
Éditez le fichier `app.py` ligne 13 :
```python
ADMIN_PASSWORD_HASH = hashlib.sha256('VOTRE_NOUVEAU_MOT_DE_PASSE'.encode()).hexdigest()
```

### Ajout d'Outils
Pour ajouter de nouveaux outils de pentest, modifiez :
1. La liste déroulante dans `dashboard.html`
2. La logique d'exécution dans `app.py` (fonction `execute_script`)

### Personnalisation du Design
Modifiez les fichiers CSS et JavaScript dans le dossier `app/static/`.

## 📝 Changelog

### Version 1.0
- Interface de connexion sécurisée
- Dashboard principal avec 5 outils
- Système d'historique complet
- Design moderne et responsive
- Sécurité renforcée
- Documentation complète

## 🤝 Support

Pour toute question ou amélioration, consultez la documentation ou modifiez le code selon vos besoins.

---

**BlackBox Tools** - Dashboard de Pentest Professionnel
Développé avec ❤️ pour la communauté cybersécurité

