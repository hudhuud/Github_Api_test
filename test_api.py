import requests
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
REPO_NAME = os.getenv("REPO_NAME")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",  # Заголовок авторизации с токеном
    "Accept": "application/vnd.github.v3+json",  # Указываем версию API GitHub
}

def create_repo(repo_name):
    """
    Создание нового публичного репозитория на GitHub.
    """
    url = "https://api.github.com/user/repos"
    data = {
        "name": repo_name,  # Имя репозитория
        "private": False,  # Публичный репозиторий
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"Репозиторий '{repo_name}' успешно создан.")
    else:
        print(f"Не удалось создать репозиторий: {response.status_code}, {response.json()}")

def list_repos():
    """
    Получение списка репозиториев пользователя.
    """
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        return [repo['name'] for repo in repos]  # Возвращаем список имен репозиториев
    else:
        print(f"Не удалось получить список репозиториев: {response.status_code}, {response.json()}")
        return []

def delete_repo(repo_name):
    """
    Удаление репозитория на GitHub.
    """
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Репозиторий '{repo_name}' успешно удален.")
    else:
        print(f"Не удалось удалить репозиторий: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    # Создаем репозиторий
    create_repo(REPO_NAME)

    # Проверяем его наличие в списке репозиториев
    repos = list_repos()
    if REPO_NAME in repos:
        print(f"Репозиторий '{REPO_NAME}' присутствует в списке репозиториев.")
    else:
        print(f"Репозиторий '{REPO_NAME}' не найден.")

    # Удаляем репозиторий
    delete_repo(REPO_NAME)
