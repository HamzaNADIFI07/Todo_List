# --- Commandes Principales ---

## Démarre l'application en arrière-plan
up:
	docker compose up -d

## Arrête l'application
down:
	docker compose down

## Affiche les logs en temps réel
logs:
	docker compose logs -f

## Réinitialise tout (Supprime données + Redémarre)
reset:
	./reset.sh

## Nettoie tout (Arrêt + Suppression volumes) sans redémarrer
clean:
	docker compose down -v --remove-orphans