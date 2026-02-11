# Hvordan installere
## 1. Last ned repoet
```sh
git clone https://github.com/kegma1/Pi-board.git
```
## 2. Set opp venv og installer pakker
```sh
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
```sh
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
```
### Utvikler modus
Hvis du ønsker å kjøre programmet i utviklermodus må du også installere tkinter
```sh
sudo apt install python3-tk
```
## 3. Kjør programmet
```sh
python __init__.py
```
