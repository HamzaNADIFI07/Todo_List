# --- Commandes Principales ---

## Démarre l'application en arrière-plan
dev:
	docker compose -f docker-compose.dev.yml up -d --build

## Démarre l'environnement de PRODUCTION (image figée)
prod:
	docker compose -f docker-compose.prod.yml up -d --build

## Arrête l'application (peu importe l'environnement)
down:
	docker compose -f docker-compose.dev.yml down
	docker compose -f docker-compose.prod.yml down 2>/dev/null || true

## Affiche les logs (Ciblé sur le fichier dev par défaut)
logs:
	docker compose -f docker-compose.dev.yml logs -f

## Réinitialise tout (Supprime données + Redémarre)
reset:
	./reset.sh

## Nettoie tout (Arrêt + Suppression volumes) sans redémarrer
clean:
	docker compose down -v --remove-orphans