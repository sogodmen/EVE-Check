import os
import cv2
import json
import discord
import logging
import asyncio
import keyboard
import pyautogui
import numpy as np
from mss import mss
from telegram import Bot
from telegram.ext import Application
from discord.ext import commands

logging.basicConfig(filename='logging.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

print("Добро пожаловать в программу EVE_Check. (c) DED Alliance")

bot_started = False
error_sound_played = False
object_detected = False
last_played_file_nitral = None

######################################################################################################

def load_telegram_config():
    try:
        config_path = os.path.join(os.path.dirname(__file__), "Config_Telegram.json")
        with open(config_path, "r") as file:
            config = json.load(file)
            return config["TELEGRAM_TOKEN"], config["TELEGRAM_CHAT_ID"]
    except Exception as e:
        logging.error(f"Ошибка при загрузке конфигурации Telegram: {e}")
        print(f"Ошибка при загрузке конфигурации Telegram: {e}")
        return None, None

TG, telegram_chat_id = load_telegram_config()
if not TG or not telegram_chat_id:
    logging.error("Не удалось загрузить настройки Telegram. Проверьте файл Config_Telegram.json")
    print("Не удалось загрузить настройки Telegram. Проверьте файл Config_Telegram.json")
    exit(1)

async def send_telegram_notification(message):
    try:
        bot = Bot(token=TG)
        await bot.send_message(chat_id=telegram_chat_id, text=message)
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения в Telegram: {e}")
        print(f"Ошибка при отправке сообщения в Telegram: {e}")

######################################################################################################

def check_required_files(config):
    """Проверяет наличие всех необходимых файлов из конфигурации"""
    missing_files = []
    
    for file_type, path in config["PATHS"].items():
        if not os.path.exists(path):
            missing_files.append(f"{file_type}: {path}")
    
    sound_files = config["THRESHOLDS"]["SOUND_FILES"]
    for i, sound_file in enumerate(sound_files["ENEMY_COUNT"], 1):
        if not os.path.exists(sound_file):
            missing_files.append(f"Enemy sound {i}: {sound_file}")
    
    required_configs = [
        "Config_Telegram.json",
        "Config_Discord.json",
        "Config_System.json"
    ]
    
    for config_file in required_configs:
        if not os.path.exists(config_file):
            missing_files.append(f"Config file: {config_file}")
    
    if missing_files:
        error_msg = "Отсутствуют следующие обязательные файлы:\n" + "\n".join(missing_files)
        logging.error(error_msg)
        print(error_msg)
        raise FileNotFoundError(error_msg)
    
def load_system_config():
    try:
        with open("Config_System.json", "r") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Ошибка при загрузке системной конфигурации: {e}")
        print(f"Ошибка при загрузке системной конфигурации: {e}")
        return None

system_config = load_system_config()

if not system_config:
    logging.error("Не удалось загрузить системную конфигурацию. Проверьте файл Config_System.json")
    print("Не удалось загрузить системную конфигурацию. Проверьте файл Config_System.json")
    exit(1)

def validate_system_config(config):
    required_sections = ["COLOR_DETECTION", "THRESHOLDS", "PATHS", "SCREEN"]
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Отсутствует обязательная секция конфигурации: {section}")
    
    for color in ["RED", "ORANGE", "YELLOW"]:
        if color not in config["COLOR_DETECTION"]:
            raise ValueError(f"Отсутствует конфигурация для цвета: {color}")
    
    if "ENEMY_COUNT" not in config["THRESHOLDS"]["SOUND_FILES"]:
        raise ValueError("Отсутствует конфигурация звуковых файлов для количества врагов")

try:
    check_required_files(system_config)
except FileNotFoundError:
    exit(1)

try:
    validate_system_config(system_config)
except ValueError as e:
    logging.error(f"Ошибка в конфигурации: {e}")
    print(f"Ошибка в конфигурации: {e}")
    exit(1)

DETECTION_THRESHOLD = system_config["THRESHOLDS"]["DETECTION_THRESHOLD"]
template_path = system_config["PATHS"]["TEMPLATE_IMAGE"]

intents = discord.Intents.default().all()
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

def load_config():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "Config_Discord.json")
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Файл конфигурации Discord не найден: {config_path}")
            
        with open(config_path, "r", encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Ошибка при чтении файла Config_Discord.json: {e}")
        print(f"Ошибка при чтении файла Config_Discord.json: {e}")
        return None

def validate_config(config):
    required_keys = ["TOKEN", "GUILD_ID", "CHANNEL_ID"]
    for key in required_keys:
        if key not in config:
            logging.error(f"Отсутствует обязательный параметр конфигурации: {key}")
            print(f"Отсутствует обязательный параметр конфигурации: {key}")
            return False
    return True

config = load_config()

if config is None:
    logging.error("Не удалось загрузить конфигурацию Discord. Проверьте файл Config_Discord.json")
    print("Не удалось загрузить конфигурацию Discord. Проверьте файл Config_Discord.json")
    exit(1)

if config and validate_config(config):
    TOKEN = config["TOKEN"]
    GUILD_ID = config["GUILD_ID"]
    CHANNEL_ID = config["CHANNEL_ID"]
else:
    logging.error("Проверьте параметры конфигурации.")
    print("Проверьте параметры конфигурации.")
    exit(1)

def get_and_save_region():
    logging.info("Пожалуйста, наведите мышь в левый верхний угол области и нажмите F12.")
    print("Пожалуйста, наведите мышь в левый верхний угол области и нажмите F12.")
    logging.info("Затем наведите мышь в правый нижний угол области и нажмите F12 снова.")
    print("Затем наведите мышь в правый нижний угол области и нажмите F12 снова.")
    keyboard.wait('F12')
    left, top = pyautogui.position()
    keyboard.wait('F12')    
    right, bottom = pyautogui.position()
    width = right - left
    height = bottom - top
    region = (left, top, width, height)
    with open("Config_Region.json", "w") as file:
        json.dump(region, file)
    logging.info("Координаты области сохранены.")
    return region

def load_or_ask_region():
    if os.path.exists("Config_Region.json"):
        try:
            with open("Config_Region.json", "r") as file:
                region = json.load(file)
        except json.JSONDecodeError:
            logging.error("Ошибка при загрузке файла с регионом. Будет использован новый регион.")
            print("Ошибка при загрузке файла с регионом. Будет использован новый регион.")
            region = get_and_save_region()
    else:
        region = get_and_save_region()

    if 'region' in locals() and region:
        choice = input("Хотите загрузить настройки из файла? (y/n): ")
        if choice.lower() != 'y':
            region = get_and_save_region()
    return region

region = load_or_ask_region()

async def compare_counter(counter):
    global last_played_file_nitral

    thresholds = [int(t) for t in system_config["THRESHOLDS"]["DETECTION_THRESHOLD"].split(",")]
    sound_files = system_config["THRESHOLDS"]["SOUND_FILES"]
    
    try:
        if counter > thresholds[-1]:
            max_sound = sound_files["MAX_ENEMIES"]
            if last_played_file_nitral != max_sound:
                await play_sound_file(max_sound, GUILD_ID, CHANNEL_ID)
                last_played_file_nitral = max_sound
                logging.info(f"Воспроизведен звук: {max_sound}")
                await send_telegram_notification("🙆‍♂️ Внимание! В системе множественные цели!")
        elif counter in thresholds:
            index = thresholds.index(counter)
            if index == 0:
                zero_sound = sound_files["ONE_ENEMY_LEFT"]
                if last_played_file_nitral != zero_sound:
                    await play_sound_file(zero_sound, GUILD_ID, CHANNEL_ID)
                    last_played_file_nitral = zero_sound
                    logging.info(f"Воспроизведен звук: {zero_sound}")
                    await send_telegram_notification("🤷‍♂️ Нейтрал покинул систему!")
            else:
                sound_file = sound_files["ENEMY_COUNT"][index - 1]
                if last_played_file_nitral != sound_file:
                    await play_sound_file(sound_file, GUILD_ID, CHANNEL_ID)
                    last_played_file_nitral = sound_file
                    logging.info(f"Воспроизведен звук: {sound_file}")
                    await send_telegram_notification(f"🙅‍♂️ Обнаружено врагов: {counter}")
    
    except IndexError:
        logging.error("Ошибка: Недостаточно звуковых файлов в конфигурации для данного количества врагов")
    except KeyError as e:
        logging.error(f"Ошибка в конфигурации: отсутствует ключ {e}")
    except Exception as e:
        logging.error(f"Неизвестная ошибка в compare_counter: {e}")

def find_error_client(template_path, threshold=0.7):
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]
    eve_exit = pyautogui.screenshot()
    eve_exit = np.array(eve_exit)
    eve_exit_gray = cv2.cvtColor(eve_exit, cv2.COLOR_RGB2GRAY)
    res = cv2.matchTemplate(eve_exit_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    if loc[0].size > 0:
        return True
    else:
        return False

async def object_detection(region):
    global object_detected

    while True:
        screenshot = pyautogui.screenshot(region=region)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        red_lower = np.array(system_config["COLOR_DETECTION"]["RED"]["LOWER"], np.uint8)
        red_upper = np.array(system_config["COLOR_DETECTION"]["RED"]["UPPER"], np.uint8)
        orange_lower = np.array(system_config["COLOR_DETECTION"]["ORANGE"]["LOWER"], np.uint8)
        orange_upper = np.array(system_config["COLOR_DETECTION"]["ORANGE"]["UPPER"], np.uint8)
        yellow_lower = np.array(system_config["COLOR_DETECTION"]["YELLOW"]["LOWER"], np.uint8)
        yellow_upper = np.array(system_config["COLOR_DETECTION"]["YELLOW"]["UPPER"], np.uint8)

        red_mask = cv2.inRange(hsv_frame, red_lower, red_upper)
        orange_mask = cv2.inRange(hsv_frame, orange_lower, orange_upper)
        yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)

        red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)                
        yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        red_count = len(red_contours)
        orange_count = len(orange_contours)
        yellow_count = len(yellow_contours)
        
        counter = red_count + orange_count + yellow_count

        if not object_detected and counter > 0:
            object_detected = True

        if object_detected:
            await compare_counter(counter)
            
        cv2.drawContours(frame, red_contours, -1, (0, 255, 255), 2)
        cv2.drawContours(frame, orange_contours, -1, (0, 255, 255), 2)
        cv2.drawContours(frame, yellow_contours, -1, (0, 255, 255), 2)

        if find_error_client(template_path):
            logging.error("Отключение клиента - Потеряна связь с сервером!!!")
            print("Отключение клиента - Потеряна связь с сервером!!!")
            await send_telegram_notification("🔴 Критическая ситуация: Клиент игры отключён!")
            await handle_error_client()
            break

        await asyncio.sleep(system_config["SCREEN"]["SCAN_INTERVAL"])

async def handle_error_client():
    global error_sound_played
    
    if not error_sound_played:
        await play_sound_file(system_config["PATHS"]["ERROR_SOUND"], GUILD_ID, CHANNEL_ID)
        await asyncio.sleep(system_config["SCREEN"]["ERROR_CHECK_INTERVAL"])
        await object_detection(region)

async def play_sound_file(file_path, guild_id, channel_id):
    guild = bot.get_guild(int(guild_id))
    if guild:
        try:
            voice_client = await connect_to_voice_channel(guild, channel_id)
            if voice_client:
                await play_sound(voice_client, file_path)
        except Exception as e:
            logging.error(f"Ошибка при воспроизведении звука: {e}")
            print(f"Ошибка при воспроизведении звука: {e}")
    else:
        logging.error("Сервер не найден.")
        print("Сервер не найден.")

async def connect_to_voice_channel(guild, channel_id):
    voice_channel = guild.get_channel(int(channel_id))
    if voice_channel:
        if not voice_channel.guild.voice_client:
            try:
                return await voice_channel.connect()
            except Exception as e:
                logging.error("Ошибка при подключении к голосовому каналу:", e)
                print("Ошибка при подключении к голосовому каналу:", e)
        else:
            return voice_channel.guild.voice_client
    else:
        logging.error("Канал голоса не найден.")
        print("Канал голоса не найден.")
        return None

async def play_sound(voice_client, file_path):
    if os.path.isfile(file_path):
        try:
            voice_client.play(discord.FFmpegPCMAudio(file_path))
            while voice_client.is_playing():
                await asyncio.sleep(1)
            await voice_client.disconnect()
        except Exception as e:
            logging.error("Файл не найден:", file_path)
            print("Файл не найден:", file_path)

async def object_detection_forever():
    while True:
        try:
            await object_detection(region)
        except Exception as e:
            logging.error(f"Произошла ошибка при обнаружении объекта: {e}")
            print(f"Произошла ошибка при обнаружении объекта: {e}")
            await asyncio.sleep(5)

async def play_start_bot_sound():
    global bot_started
    if not bot_started:
        await play_sound_file(system_config["PATHS"]["START_SOUND"], GUILD_ID, CHANNEL_ID)
        bot_started = True
        
@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user}')
    print(f'Logged in as {bot.user}')
    await send_telegram_notification(f'🟢 Подключение клиента: {bot.user}')
    await play_start_bot_sound()
    bot.loop.create_task(object_detection_forever())

if __name__ == "__main__":
    bot.run(TOKEN)
    