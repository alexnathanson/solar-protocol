git clone https://github.com/alexnathanson/solar-protocol
pushd solar-protocol
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
cp -r local ../
cp backend/data/deviceListTemplate.json backend/data/deviceList.json
