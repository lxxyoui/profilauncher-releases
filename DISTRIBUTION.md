# Profilauncher — distribution

Support : https://discord.gg/bN5ZThamDj

Ce dépôt héberge le petit catalogue `channel.json`, signé par l’éditeur, et le
moniteur des versions Chromium. Il ne contient aucun profil ni identifiant.

## État réel

Le client source v1.10 vérifie la signature, la date et la progression des révisions
avant d’importer une recette. Le moteur Brave officiel est ensuite téléchargé et
testé localement avant activation. Un contrôle récent est réutilisé pendant cinq
minutes pour éviter les requêtes répétées. Hors ligne, la version publiée est
**non vérifiée**, et le moteur installé doit réussir les contrôles locaux.

Ce n’est pas encore un installateur EXE autonome ni un Chromium personnalisé.
Un JSON ne peut pas ajouter des fonctions natives absentes du navigateur.
CPU/RAM annoncés arbitraires et bruits personnalisés audio/WebGL natifs ne sont
pas implémentés par ce canal. Aucune garantie « zéro fuite » ou de passage des anti-bots.

## Notifications de l’éditeur

Le workflow compare toutes les six heures environ la recette publiée au canal
Chrome stable Windows. En cas de retard et si `DISCORD_WEBHOOK_URL` est configuré
dans **Settings → Secrets and variables → Actions**, il envoie uniquement les
versions sur Discord et ouvre une issue de suivi pour éviter de répéter l’alerte.
Il ne télécharge ni ne compile Chromium. Un écart de version n’est pas une fuite.
Une interruption entre l’envoi et l’enregistrement peut occasionner un doublon.
Les horaires GitHub sont indicatifs ; GitHub peut retarder/désactiver les tâches
planifiées, notamment après une longue inactivité du dépôt public.

Régénérez tout webhook partagé dans une conversation avant de l’enregistrer.
Ni le webhook ni une clé privée ne doivent être commités.

## Publication d’une recette

L’éditeur signe localement une recette compatible et publie le nouveau `channel.json`
sur la branche `main`, avec un numéro de séquence strictement croissant.
La clé privée est protégée par Windows DPAPI sur le poste de l’éditeur ; elle
n’est pas portable telle quelle vers un autre compte Windows. Prévoir une
sauvegarde sécurisée du poste et une procédure de rotation avant diffusion large.
La clé publique embarquée doit être distribuée avec le client initial de confiance :
ne jamais remplacer automatiquement cette clé depuis ce dépôt.

Le catalogue expire après 30 jours : republier périodiquement même si le moteur
ne change pas. Un manifeste signé ne remplace jamais les tests de qualification.
Le contrôle anti-retour en arrière repose sur l’état local ; supprimer cet état
supprime cet historique. Le JSON public n’est pas une mise à jour du code applicatif.

Documentation :
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule
- https://docs.discord.com/developers/resources/webhook
