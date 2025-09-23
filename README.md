
# EVE_Check_2.0

Проект для мониторинга и уведомлений через Telegram/Discord, с поддержкой звуковых оповещений.

---

## 🔧 Системные требования

- Windows 10 или выше
- Python 3.10+
- ffmpeg (нужен только `bin` каталог)

---

## 📦 Установка

### 1. Установка Python

Скачайте и установите Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
При установке отметьте галочку **"Add Python to PATH"**.

### 2. Установка зависимостей

Откройте терминал (cmd/PowerShell) в папке с проектом и выполните:

```bash
python install_requirements.py
```

Скрипт установит библиотеки из `install_packages.json`.

---

## 📁 Добавление FFmpeg в переменную среды PATH

1. Скопируйте папку `ffmpeg` на диск, например `C:\Tools\ffmpeg`
2. Добавьте `C:\Tools\ffmpeg\bin` в переменную среды PATH:

**Как:**
- Win + R → `sysdm.cpl` → вкладка **Дополнительно** → **Переменные среды**
- Найдите переменную `Path` → **Изменить** → **Добавить** путь
- Нажмите **ОК** везде

Проверьте:

```bash
ffmpeg -version
```

---

## ⚙️ Настройка конфигураций

Редактируйте файлы:

- `Config_Telegram.json` — токен и ID Telegram-чата
- `Config_Discord.json` — токен/вебхук Discord
- `Config_Region.json`, `Config_System.json` — параметры системы

Пример:
```json
{
  "token": "YOUR_TELEGRAM_BOT_TOKEN",
  "chat_id": -100123456789
}
```

---

## 🚀 Запуск

### Вариант 1: Через `.bat`
Просто дважды кликните `BOT.bat`.

### Вариант 2: Через терминал

# Для запуска только Discord бота выполните команду: 

```bash
python EVE_Check.py
```
# Для запуска бота с поддержкой Telegram и Discord выполните команду:

```bash
python EVE_Check_2.0.py
```

---

## 📌 Примечания

- Используются `.wav` файлы из `Sound/` для озвучивания событий
- Бот отправляет уведомления в Telegram/Discord при обнаружении событий

