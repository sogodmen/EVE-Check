import subprocess
import sys
import json
from pathlib import Path

def is_package_installed(package_name):
    try:
        if sys.version_info >= (3, 8):
            from importlib.metadata import distribution
            distribution(package_name)
        else:
            import pkg_resources
            pkg_resources.get_distribution(package_name)
        return True
    except:
        return False

def load_packages_from_json(json_path="install_packages.json"):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("packages", [])
    except FileNotFoundError:
        print(f"⚠ Файл {json_path} не найден! Используется пустой список пакетов.")
        return []
    except json.JSONDecodeError:
        print(f"⚠ Ошибка в формате JSON в файле {json_path}! Используется пустой список.")
        return []

def install_packages():
    packages = load_packages_from_json()
    if not packages:
        print("❌ Список пакетов пуст или не загружен. Проверьте install_packages.json.")
        return

    print("🔍 Проверка и установка пакетов...")
    for package in packages:
        if is_package_installed(package):
            print(f"✅ Уже установлен: {package}")
            continue
        
        try:
            print(f"⬇ Устанавливаю {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Успешно: {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка при установке {package}: {e}")

if __name__ == "__main__":
    print("🚀 Начало установки зависимостей...")
    install_packages()
    print("🎉 Готово! Все пакеты проверены.")