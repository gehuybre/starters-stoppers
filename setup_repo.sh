#!/bin/bash
# Setup script voor nieuwe dashboard repository

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Dashboard Repository Setup ===${NC}\n"

# Check if we're in the right directory
if [ ! -d "dashboard-provincies" ]; then
    echo -e "${YELLOW}⚠️  Zorg dat je dit script uitvoert vanuit de fin-gez root directory${NC}"
    exit 1
fi

# Ask for repository name and location
read -p "Naam van de nieuwe repository (zonder .git): " REPO_NAME
read -p "Locatie waar de repo moet komen (default: ../): " REPO_LOCATION
REPO_LOCATION=${REPO_LOCATION:-"../"}

# Create full path
REPO_PATH="${REPO_LOCATION}${REPO_NAME}"

echo -e "\n${BLUE}Repository wordt aangemaakt in: ${REPO_PATH}${NC}\n"

# Create directory structure
echo -e "${GREEN}✓${NC} Aanmaken directory structuur..."
mkdir -p "${REPO_PATH}/data"
mkdir -p "${REPO_PATH}/css"
mkdir -p "${REPO_PATH}/js"
mkdir -p "${REPO_PATH}/assets"
mkdir -p "${REPO_PATH}/.github/workflows"

# Copy dashboard files
echo -e "${GREEN}✓${NC} Kopiëren dashboard files..."
cp dashboard-provincies/index.html "${REPO_PATH}/"
cp dashboard-provincies/.gitignore "${REPO_PATH}/"
cp dashboard-provincies/.github/workflows/deploy.yml "${REPO_PATH}/.github/workflows/"

# Copy CSS files
echo -e "${GREEN}✓${NC} Kopiëren CSS files..."
cp dashboard-provincies/css/*.css "${REPO_PATH}/css/"

# Copy JS files
echo -e "${GREEN}✓${NC} Kopiëren JavaScript files..."
cp dashboard-provincies/js/*.js "${REPO_PATH}/js/"

# Copy assets
echo -e "${GREEN}✓${NC} Kopiëren assets..."
cp dashboard-provincies/assets/* "${REPO_PATH}/assets/" 2>/dev/null || echo -e "${YELLOW}  (geen assets gevonden)${NC}"

# Copy data files
echo -e "${GREEN}✓${NC} Kopiëren data files..."
cp -r data/data-grafieken "${REPO_PATH}/data/"

# Copy README
echo -e "${GREEN}✓${NC} Kopiëren README..."
cp dashboard-provincies/DASHBOARD_REPO_README.md "${REPO_PATH}/README.md"

# Initialize git repository
echo -e "\n${BLUE}Git repository initialiseren...${NC}"
cd "${REPO_PATH}"
git init
git add .
git commit -m "Initial commit: Dashboard setup"

echo -e "\n${GREEN}✅ Repository succesvol aangemaakt!${NC}"
echo -e "\n${BLUE}Volgende stappen:${NC}"
echo -e "1. cd ${REPO_PATH}"
echo -e "2. Maak een nieuwe repository op GitHub: ${YELLOW}https://github.com/new${NC}"
echo -e "3. Voeg remote toe en push:"
echo -e "   ${YELLOW}git remote add origin git@github.com:GEBRUIKER/${REPO_NAME}.git${NC}"
echo -e "   ${YELLOW}git branch -M main${NC}"
echo -e "   ${YELLOW}git push -u origin main${NC}"
echo -e "4. Ga naar GitHub repo Settings > Pages"
echo -e "5. Selecteer 'GitHub Actions' als Source"
echo -e "6. De site wordt automatisch gepubliceerd op: ${YELLOW}https://GEBRUIKER.github.io/${REPO_NAME}/${NC}"
echo -e "\n${GREEN}Klaar!${NC} 🎉\n"
