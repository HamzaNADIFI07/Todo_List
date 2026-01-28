#!/bin/bash

# --- Configuration des couleurs pour les logs ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Arrêt du script dès qu'une erreur survient
set -e

echo -e "${YELLOW}Début de la procédure de réinitialisation...${NC}"

# 1. Arrêt et suppression des conteneurs, réseaux et VOLUMES (-v)
echo -e "${YELLOW}Suppression de l'ancienne stack et des volumes...${NC}"
docker compose down --volumes --remove-orphans

# 2. Re-build et démarrage en mode détaché
echo -e "${YELLOW}Redémarrage des services...${NC}"
docker compose -f docker-compose.dev.yml up -d --build

# Boucle pour vérifier l'état "healthy" du service "db"
# On boucle tant que le status n'est pas "healthy"
until [ "$(docker inspect -f {{.State.Health.Status}} $(docker compose ps -q db))" == "healthy" ]; do
    echo -n "."
    sleep 2
done

echo "" # Saut de ligne
echo -e "${GREEN}✅  Base de données prête et accessible !${NC}"
echo -e "${GREEN}✨  Reset terminé avec succès. L'API est disponible sur http://localhost:5000/api/tasks${NC}"