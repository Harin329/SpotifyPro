# SpotifyPro

## Messy Library No More!
My spotify library was a mess. It included every song I knew, filling up a playlist with over 15k+ songs. I started to split off older songs that are overplayed into playlists by release year. This project runs on a Raspberry Pi and allows me to run an Apple shortcut to move the currently playing song to the correct place and then skip it.

## Stack
- Flask, Web Server & REST API Endpoints
- Gunicorn, Production Deployment
- Systemd, Manage Services on Pi
- Nginx, Proxy
- Ansible, Automated Deployment onto Pi

## Installation & Deployment

### Local Development
1. Create virtual environment using ```python -m venv <envName>```
2. ```pip install -r requirements.txt```
3. Create .env file by copying .env.example and insert environment variables & secrets
4. Edit all occurences of ```REDIRECT_URI``` and replace with ```REDIRECT_URI_DEV```
5. ```flask run```

### Deployment
1. Install ansible
2. Create id_rsa or any other ssh key to allow secure connection to server
3. Create .env file by copying .env.example and insert environment variables & secrets
4. Edit all occurences of ```REDIRECT_URI_DEV``` and replace with ```REDIRECT_URI```
5. Run ```ansible-playbook -v site.yaml```
