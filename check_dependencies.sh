#!/bin/bash
# Check and Install 8825 System Dependencies

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== 8825 Dependency Check ===${NC}"
echo ""

missing_deps=0
installed_deps=0

# Function to check Python package
check_python_package() {
    local package=$1
    local import_name=${2:-$1}
    
    if python3 -c "import $import_name" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $package"
        installed_deps=$((installed_deps + 1))
        return 0
    else
        echo -e "${RED}✗${NC} $package (missing)"
        missing_deps=$((missing_deps + 1))
        return 1
    fi
}

# Function to install Python package
install_python_package() {
    local package=$1
    echo -e "${YELLOW}Installing $package...${NC}"
    pip3 install "$package" --quiet
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $package installed${NC}"
        return 0
    else
        echo -e "${RED}✗ Failed to install $package${NC}"
        return 1
    fi
}

echo "Checking Python packages..."
echo ""

# Core Python packages (standard library - should always be present)
echo "Standard Library:"
check_python_package "pathlib" "pathlib"
check_python_package "json" "json"
check_python_package "datetime" "datetime"
check_python_package "hashlib" "hashlib"
check_python_package "shutil" "shutil"
check_python_package "typing" "typing"

echo ""
echo "Third-Party Packages:"

# Third-party packages that need installation
# Format: "package_name:import_name"
packages=(
    "python-docx:docx"
    "watchdog:watchdog"
    "flask:flask"
    "flask-cors:flask_cors"
    "python-dotenv:dotenv"
    "google-auth:google.auth"
    "google-auth-oauthlib:google_auth_oauthlib"
    "google-api-python-client:googleapiclient"
    "pillow:PIL"
    "pytesseract:pytesseract"
    "pillow-heif:pillow_heif"
)

for pkg_info in "${packages[@]}"; do
    IFS=':' read -r package import_name <<< "$pkg_info"
    if ! check_python_package "$package" "$import_name"; then
        # Try to install if missing
        install_python_package "$package"
    fi
done

echo ""
echo "Checking system commands..."
echo ""

# Check for required system commands
commands=("rsync" "find" "grep" "python3" "bash")

for cmd in "${commands[@]}"; do
    if command -v "$cmd" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $cmd"
        installed_deps=$((installed_deps + 1))
    else
        echo -e "${RED}✗${NC} $cmd (missing)"
        missing_deps=$((missing_deps + 1))
    fi
done

echo ""
echo -e "${BLUE}=== Summary ===${NC}"
echo ""
echo "Installed: $installed_deps"
echo "Missing: $missing_deps"
echo ""

if [ $missing_deps -eq 0 ]; then
    echo -e "${GREEN}✓ All dependencies satisfied!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠ Some dependencies are missing${NC}"
    echo ""
    echo "To install missing Python packages:"
    echo "  pip3 install -r requirements.txt"
    echo ""
    echo "Or install individually:"
    echo "  pip3 install python-docx watchdog flask flask-cors python-dotenv"
    echo "  pip3 install google-auth google-auth-oauthlib google-api-python-client"
    echo "  pip3 install pillow pytesseract pillow-heif"
    exit 1
fi
