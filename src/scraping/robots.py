import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser

def respectRobots(url, user_agent):
    rp = RobotFileParser()
    base = url.split("/", 3)[:3]
    robots_url = "/".join(base) + "/robots.txt"
    rp.set_url(robots_url)
    rp.read()

    if not rp.can_fetch(user_agent, url):
        print(f"Acceso no permitido por robots.txt: {url}")
        return None

    try:
        resp = requests.get(url, timeout=10, headers={'User-Agent': user_agent})
        if resp.status_code != 200:
            print(f"Error {resp.status_code}: {url}")
            return None

        return BeautifulSoup(resp.text, "lxml")

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return None
