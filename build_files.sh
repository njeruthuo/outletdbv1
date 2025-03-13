# build_files.sh

echo "Checking if Python is installed..."
if ! command -v python3 &>/dev/null; then
    echo "Python3 not found, installing..."
    apt-get update && apt-get install -y python3 python3-pip
fi

echo "INSTALLING REQUIREMENTS....."

python3 -m pip install --upgrade pip

python3 -m pip install -r requirements.txt

echo "Installing requirements Done..."

echo "collect static begins...."

python3 manage.py collectstatic --noinput

echo "collect static done...."
