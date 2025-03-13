# build_files.sh

# Install pip if not available
if ! command -v pip &> /dev/null; then
    echo "Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
fi

echo "INSTALLING REQUIREMENTS....."

python3 -m pip install --upgrade pip

python3 -m pip install -r requirements.txt

echo "Installing requirements Done..."

# echo "collect static begins...."

# python3 manage.py collectstatic --noinput

# echo "collect static done...."
