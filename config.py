"""
Конфигурационный файл для бота KURAI
Замените все ID на свои значения!
"""

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

class Config:
    """
    Главный класс конфигурации
    Все настройки бота хранятся здесь
    """
    
    # ============================================
    # 1. ТОКЕН БОТА (из .env файла)
    # ============================================
    BOT_TOKEN = os.getenv('')
    
    # ============================================
    # 2. ID СЕРВЕРА (GUILD)
    # ============================================
    # Как получить: ПКМ на сервере → Копировать ID
    GUILD_ID = 1518355089377464421  # ЗАМЕНИТЕ НА СВОЙ ID
    
    # ============================================
    # 3. ID РОЛЕЙ
    # ============================================
    # Как получить: Настройки сервера → Роли → ПКМ на роли → Копировать ID
    
    # Роль, которая выдается при входе на сервер
    UNVERIFY_ROLE_ID = 1519052285685141554  # ЗАМЕНИТЕ
    
    # Роль, которая выдается после успешной верификации
    VERIFIED_ROLE_ID = 1518355089419403281  # ЗАМЕНИТЕ
    
    # Роль сотрудников (Support/Staff), у которых есть доступ к командам
    STAFF_ROLE_ID = 1519426143701434640  # ЗАМЕНИТЕ
    
    # Роль для отстраненных пользователей
    BANNED_ROLE_ID = 1520043070484123719  # ЗАМЕНИТЕ
    
    # ID ролей для гендерной системы (можно добавить свои)
    GENDER_ROLES = {
        'male': 1518355089419403282,     # ID роли "Мужской"
        'female': 1518355089419403283,   # ID роли "Женский"
        'non_binary': 1520045604989046897, # ID роли "Небинарный"
        'other': 123456789012345678,    # ID роли "Другой"
    }
    
    # ============================================
    # 4. ID КАТЕГОРИЙ
    # ============================================
    # Как получить: ПКМ на категории → Копировать ID
    
    # Категория "Верификация" - видят только неверифицированные
    VERIFY_CATEGORY_ID = 1519618750603595887  # ЗАМЕНИТЕ
    
    # Категория "Приемная" - где сидят Support и голосовые каналы
    RECEPTION_CATEGORY_ID = 1519051921904763104  # ЗАМЕНИТЕ
    
    # Категория для основных каналов (скрыта от Unverify)
    MAIN_CATEGORY_ID = 1518355090787012617  # ЗАМЕНИТЕ
    
    # ============================================
    # 5. ID КАНАЛОВ
    # ============================================
    # Как получить: ПКМ на канале → Копировать ID
    
    # Канал для логов (все действия Support)
    LOG_CHANNEL_ID = 1519627825869754440  # ЗАМЕНИТЕ
    
    # Канал для уведомлений (оповещения о входе в голосовой канал)
    NOTIFICATION_CHANNEL_ID = 1520042053881303190  # ЗАМЕНИТЕ
    
    # Канал для приветствий (новые участники)
    WELCOME_CHANNEL_ID = 1519619103101550632  # ЗАМЕНИТЕ
    
    # Канал для правил
    RULES_CHANNEL_ID = 1518355090044620910  # ЗАМЕНИТЕ
    
    # ============================================
    # 6. ID ГОЛОСОВЫХ КАНАЛОВ ДЛЯ ВЕРИФИКАЦИИ (7 штук)
    # ============================================
    # Как получить: ПКМ на голосовом канале → Копировать ID
    
    VOICE_CHANNELS_IDS = [
        1519059821557579878,  # Прихожая 1
        1519071615059628164,  # Прихожая 2
        1519071801563418634,  # Прихожая 3
        1519071864423714888,  # Прихожая 4
        1519071932480225422,  # Прихожая 5
        1519469742652391534,  # Прихожая 6
        1519469828816109590,  # Прихожая 7
    ]
    
    # ============================================
    # 7. НАСТРОЙКИ БАЗЫ ДАННЫХ
    # ============================================
    
    # Тип базы данных: 'json', 'sqlite', 'postgresql'
    DATABASE_TYPE = 'json'
    
    # Путь к файлу JSON (если используется JSON)
    JSON_DB_PATH = 'bot/database/punishments.json'
    
    # Настройки для SQLite (если используется)
    SQLITE_DB_PATH = 'bot/database/kurai_bot.db'
    
    # Настройки для PostgreSQL (если используется)
    # POSTGRES_HOST = 'localhost'
    # POSTGRES_PORT = 5432
    # POSTGRES_DB = 'kurai_bot'
    # POSTGRES_USER = 'kurai_user'
    # POSTGRES_PASSWORD = 'secure_password'
    
    # ============================================
    # 8. НАСТРОЙКИ ЛОГИРОВАНИЯ
    # ============================================
    
    # Уровень логирования: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    LOG_LEVEL = 'INFO'
    
    # Путь к файлу логов
    LOG_FILE_PATH = 'bot/logs/bot.log'
    
    # Логировать ли в консоль
    LOG_TO_CONSOLE = True
    
    # Логировать ли в файл
    LOG_TO_FILE = True
    
    # ============================================
    # 9. НАСТРОЙКИ ВЕРИФИКАЦИИ
    # ============================================
    
    # Автоматически выдавать роль Unverify при входе
    AUTO_UNVERIFY = True
    
    # Удалять ли роль Unverify после верификации
    REMOVE_UNVERIFY_ON_VERIFY = True
    
    # Сообщение в ЛС при входе
    WELCOME_DM_MESSAGE = """
👋 Приветствую, {user}!

Ты попал на сервер **KURAI**!

📢 **Важно:** Ты проходишь голосовую верификацию.
🎙 Зайди в любой голосовой канал из категории **"Прихожие"** (всего их 7).
Там тебе зададут несколько вопросов.

📋 После успешной верификации ты получишь доступ ко всем каналам.

⚠️ **Не забудь ознакомиться с правилами сервера!**

Удачи! 🍀
"""
    
    # Сообщение в канал при входе участника
    WELCOME_CHANNEL_MESSAGE = """
🎉 Добро пожаловать, {user}!

📌 Ты получил роль **Unverify**.
🎙 Для верификации зайди в любой голосовой канал из категории **"Прихожие"**.
👥 Там тебя встретят наши Support и проведут верификацию.

Удачи! 🌟
"""
    
    # ============================================
    # 10. НАСТРОЙКИ НАКАЗАНИЙ
    # ============================================
    
    # Список доступных дней для отстранения
    PUNISHMENT_DAYS = [7, 14, 28]
    
    # Автоматически снимать наказание по истечению срока
    AUTO_REMOVE_PUNISHMENT = True
    
    # Интервал проверки наказаний (в секундах)
    PUNISHMENT_CHECK_INTERVAL = 3600  # 1 час
    
    # ============================================
    # 11. НАСТРОЙКИ ИНТЕРФЕЙСА
    # ============================================
    
    # Цвета Embed (в HEX)
    COLORS = {
        'success': 0x00FF00,      # Зеленый
        'error': 0xFF0000,        # Красный
        'warning': 0xFFA500,      # Оранжевый
        'info': 0x0099FF,         # Синий
        'gold': 0xFFD700,         # Золотой
        'purple': 0x9B59B6,       # Фиолетовый
        'unverify': 0x95A5A6,     # Серый (для Unverify)
    }
    
    # Эмодзи для кнопок и сообщений
    EMOJIS = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'verify': '🔊',
        'unverify': '🔇',
        'gender': '🎭',
        'ban': '⛔',
        'change': '🔄',
        'staff': '👤',
        'avatar': '🖼',
        'punishment': '⛓️',
        'welcome': '👋',
        'rules': '📋',
        'voice': '🎙️',
        'support': '🛠️',
        'log': '📝',
        'timer': '⏰',
        'calendar': '📅',
        'user': '👤',
    }
    
    # ============================================
    # 12. НАСТРОЙКИ ВРЕМЕНИ
    # ============================================
    
    # Часовой пояс (для отображения времени)
    TIMEZONE = 'Europe/Moscow'  # Или 'UTC'
    
    # Формат даты и времени
    DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'
    DATE_FORMAT = '%d.%m.%Y'
    
    # ============================================
    # 13. ПРАВА ДОСТУПА
    # ============================================
    
    # Уровни доступа для ролей
    PERMISSIONS = {
        'owner': 10,       # Владелец сервера
        'admin': 8,        # Администратор
        'head_staff': 5,   # Главный Support
        'staff': 3,        # Support
        'trial_staff': 1,  # Стажер
        'member': 0,       # Обычный участник
    }
    
    # Минимальный уровень для использования команд
    COMMAND_PERMISSIONS = {
        'action': 3,              # /action
        'staff_profile': 3,       # /staff_profile
        'view_avatar': 3,         # /view_avatar
        'punishment': 3,          # /punishment
        'verify': 3,              # /verify
        'unverify': 3,            # /unverify
        'staff_list': 3,          # /staff_list
        'staff_stats': 5,         # /staff_stats
        'add_note': 3,            # /add_note
        'clear_punishments': 8,   # /clear_punishments
        'sync_commands': 8,       # /sync_commands
        'reload_config': 8,       # /reload_config
    }
    
    # ============================================
    # 14. ВСПОМОГАТЕЛЬНЫЕ НАСТРОЙКИ
    # ============================================
    
    # Максимальное количество наказаний для одного пользователя
    MAX_PUNISHMENTS = 10
    
    # Время жизни кнопок (в секундах)
    BUTTON_TIMEOUT = 300  # 5 минут
    
    # Задержка перед автоматической выдачей роли (в секундах)
    AUTO_ROLE_DELAY = 5
    
    # ============================================
    # 15. МЕТОДЫ ДЛЯ ПРОВЕРКИ КОНФИГУРАЦИИ
    # ============================================
    
    @classmethod
    def validate_config(cls):
        """
        Проверяет, все ли обязательные параметры заполнены
        """
        errors = []
        
        if not cls.BOT_TOKEN:
            errors.append("❌ BOT_TOKEN не установлен!")
        
        if cls.GUILD_ID == 123456789012345678:
            errors.append("❌ GUILD_ID не изменен! Замените на ID своего сервера.")
        
        if cls.UNVERIFY_ROLE_ID == 123456789012345678:
            errors.append("❌ UNVERIFY_ROLE_ID не изменен! Замените на ID роли.")
        
        if cls.STAFF_ROLE_ID == 123456789012345678:
            errors.append("❌ STAFF_ROLE_ID не изменен! Замените на ID роли.")
        
        if cls.LOG_CHANNEL_ID == 123456789012345678:
            errors.append("❌ LOG_CHANNEL_ID не изменен! Замените на ID канала.")
        
        if any(id == 123456789012345678 for id in cls.VOICE_CHANNELS_IDS):
            errors.append("❌ VOICE_CHANNELS_IDS не изменены! Замените на ID голосовых каналов.")
        
        return errors
    
    @classmethod
    def get_config_summary(cls):
        """
        Возвращает краткую информацию о конфигурации
        """
        return f"""
        📊 **Конфигурация бота KURAI**
        
        🤖 Бот: {cls.BOT_TOKEN[:20]}... (скрыто)
        🏠 Сервер ID: {cls.GUILD_ID}
        🎭 Роль Unverify: {cls.UNVERIFY_ROLE_ID}
        🎭 Роль Staff: {cls.STAFF_ROLE_ID}
        📝 Канал логов: {cls.LOG_CHANNEL_ID}
        🎙️ Голосовых каналов: {len(cls.VOICE_CHANNELS_IDS)}
        📁 Тип БД: {cls.DATABASE_TYPE}
        """

# ============================================
# 16. ДОПОЛНИТЕЛЬНЫЕ КЛАССЫ ДЛЯ РАЗНЫХ ОКРУЖЕНИЙ
# ============================================

class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    LOG_LEVEL = 'DEBUG'
    DATABASE_TYPE = 'json'
    LOG_TO_CONSOLE = True
    AUTO_UNVERIFY = True

class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    LOG_LEVEL = 'WARNING'
    DATABASE_TYPE = 'postgresql'
    LOG_TO_CONSOLE = False
    LOG_TO_FILE = True
    AUTO_UNVERIFY = True

class TestingConfig(Config):
    """Конфигурация для тестирования"""
    LOG_LEVEL = 'ERROR'
    DATABASE_TYPE = 'sqlite'
    LOG_TO_CONSOLE = False
    LOG_TO_FILE = False
    AUTO_UNVERIFY = False

# ============================================
# 17. ВЫБОР КОНФИГУРАЦИИ
# ============================================

# По умолчанию используем основную конфигурацию
# Для переключения раскомментируйте нужную строку:
# CONFIG = DevelopmentConfig()
# CONFIG = ProductionConfig()
# CONFIG = TestingConfig()

CONFIG = Config()  # Основная конфигурация

# Экспортируем основные переменные для удобства
BOT_TOKEN = CONFIG.BOT_TOKEN
GUILD_ID = CONFIG.GUILD_ID
UNVERIFY_ROLE_ID = CONFIG.UNVERIFY_ROLE_ID
VERIFIED_ROLE_ID = CONFIG.VERIFIED_ROLE_ID
STAFF_ROLE_ID = CONFIG.STAFF_ROLE_ID
BANNED_ROLE_ID = CONFIG.BANNED_ROLE_ID
VERIFY_CATEGORY_ID = CONFIG.VERIFY_CATEGORY_ID
RECEPTION_CATEGORY_ID = CONFIG.RECEPTION_CATEGORY_ID
LOG_CHANNEL_ID = CONFIG.LOG_CHANNEL_ID
NOTIFICATION_CHANNEL_ID = CONFIG.NOTIFICATION_CHANNEL_ID
WELCOME_CHANNEL_ID = CONFIG.WELCOME_CHANNEL_ID
VOICE_CHANNELS_IDS = CONFIG.VOICE_CHANNELS_IDS
COLORS = CONFIG.COLORS
EMOJIS = CONFIG.EMOJIS
DATABASE_TYPE = CONFIG.DATABASE_TYPE
JSON_DB_PATH = CONFIG.JSON_DB_PATH

# ============================================
# 18. ФУНКЦИЯ ДЛЯ ЗАГРУЗКИ КОНФИГА
# ============================================

def load_config():
    """
    Загружает конфигурацию и проверяет ее
    """
    errors = Config.validate_config()
    
    if errors:
        print("⚠️ Обнаружены ошибки в конфигурации:")
        for error in errors:
            print(f"  {error}")
        return False
    
    print("✅ Конфигурация загружена успешно!")
    print(Config.get_config_summary())
    return True

# Если запускаем файл напрямую - проверяем конфиг
if __name__ == "__main__":
    load_config()