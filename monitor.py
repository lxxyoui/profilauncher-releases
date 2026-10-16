"""Surveillance GitHub Actions légère ; aucune donnée des utilisateurs."""
import json
import os
import re
import urllib.parse
import urllib.request

MAX_BYTES = 1024 * 1024


def request(url, token=None, payload=None):
    headers = {'User-Agent': 'Profilauncher-upstream-monitor', 'Accept': 'application/vnd.github+json'}
    if token:
        headers['Authorization'] = 'Bearer '+token
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers['Content-Type'] = 'application/json'
    # Ne pas transmettre les secrets à une cible de redirection.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            raise ValueError('Redirection refusée')
    opener = urllib.request.build_opener(NoRedirect())
    with opener.open(urllib.request.Request(url, data=data, headers=headers), timeout=20) as response:
        raw = response.read(MAX_BYTES+1)
    if len(raw) > MAX_BYTES:
        raise ValueError('Réponse trop grande')
    return json.loads(raw) if raw else None


def version(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d+\.\d+\.\d+\.\d+', value):
        raise ValueError('Version invalide')
    return tuple(map(int, value.split('.')))


def monitor(channel, repository, token, webhook):
    if repository != 'lxxyoui/profilauncher-releases':
        raise ValueError('Dépôt inattendu')
    stable = request('https://versionhistory.googleapis.com/v1/chrome/platforms/win/channels/stable/versions?pageSize=1')['versions'][0]['version']
    published = channel['payload']['recipe']['engine']['chromium']
    if version(published) >= version(stable):
        return 'La recette publiée ne présente pas de retard Chromium détecté.'
    if not webhook:
        return 'Retard détecté, mais DISCORD_WEBHOOK_URL absent : aucune notification envoyée.'
    parsed = urllib.parse.urlsplit(webhook)
    if (parsed.scheme != 'https' or parsed.netloc != 'discord.com' or parsed.query or parsed.fragment
            or not re.fullmatch(r'/api/webhooks/\d+/[\w-]+', parsed.path)):
        raise ValueError('Destination Discord invalide')
    title = f'[monitor] Chromium {stable} : recette {published}'
    api = f'https://api.github.com/repos/{repository}/issues'
    issues = request(api+'?state=all&per_page=100', token)
    if any(item.get('title') == title for item in issues):
        return 'Version déjà signalée ; aucune nouvelle notification.'
    # Aucun ping, profil, proxy, log local ou identifiant utilisateur.
    request(webhook+'?wait=true', payload={'content': f'Profilauncher : Chromium stable {stable}, recette publiée {published}. Une nouvelle recette doit être préparée et testée. https://github.com/{repository}',
        'allowed_mentions': {'parse': []}})
    request(api, token, {'title': title, 'body': 'Notification Discord envoyée. Ceci signale un écart de version, pas une fuite ni un résultat de test. Préparer, tester et signer la prochaine recette avant publication.'})
    return 'Nouvelle version signalée sur Discord et enregistrée dans une issue.'


def main():
    try:
        with open('channel.json', encoding='utf-8') as source:
            channel = json.load(source)
        print(monitor(channel, os.environ['GITHUB_REPOSITORY'], os.environ['GH_TOKEN'], os.environ.get('DISCORD_WEBHOOK_URL', '')))
        return 0
    except Exception:
        # Ne jamais afficher une exception urllib pouvant inclure l’URL secrète.
        print('Surveillance non aboutie : vérifier les services, droits et secrets. Aucun secret affiché.')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
