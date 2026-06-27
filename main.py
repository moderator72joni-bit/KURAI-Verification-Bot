# -*- coding: utf-8 -*-
import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    print("=" * 60)
    print("❌ ОШИБКА: BOT_TOKEN не найден в файле .env!")
    print("   Создайте файл .env с содержимым:")
    print("   BOT_TOKEN=ваш_токен_бота")
    print("=" * 60)
    exit(1)

print("✅ Токен загружен!")

# ============================================
# КОНФИГУРАЦИЯ
# ============================================
GUILD_ID = 1518355089377464421
UNVERIFY_ROLE_ID = 1519052285685141554
VERIFIED_ROLE_ID = 1518355089419403281
STAFF_ROLE_ID = 1519426143701434640
BANNED_ROLE_ID = 1520043070484123719
VERIFY_CATEGORY_ID = 1519619103101550632
RECEPTION_CATEGORY_ID = 1519051921904763104
LOG_CHANNEL_ID = 1519627825869754440
NOTIFICATION_CHANNEL_ID = 1520042053881303190
STAFF_COMMAND_CHANNEL_ID = 1520099157476638730
ACTION_CHANNEL_ID = 1520110791234158654

GENDER_ROLE_IDS = {
    'male': 1518355089419403282,
    'female': 1518355089419403283,
}

VOICE_CHANNELS_IDS = [
    1519059821557579878,
    1519071615059628164,
    1519071801563418634,
    1519071864423714888,
    1519071932480225422,
    1519469742652391534,
    1519469828816109590,
]

# Все роли Staff
STAFF_ROLES = [
    1519426143701434640,  # Support
    1519426426636603462,  # Creative
    1519426936873554193,  # Control
    1518355089406955520,  # Moderator
    1520097774857879782,  # Curator
    1519713881017155644,  # Master
    1518355089377464430,  # Administrator
    1518355089377464423,  # Owner
    1519427308274975004,  # Closemod
    1519730114127200267,  # Broadcaster
    1519727771922727012,  # Content Maker
    1519427150917275669,  # Global Event
]

GENDER_GIVER_ROLES = [
    1519426143701434640,  # Support
    1519426426636603462,  # Creative
    1519426936873554193,  # Control
    1518355089406955520,  # Moderator
    1520097774857879782,  # Curator
    1519713881017155644,  # Master
    1518355089377464430,  # Administrator
    1518355089377464423,  # Owner
]

STAFF_MANAGEMENT_ROLES = [
    1520097774857879782,  # Curator
    1519713881017155644,  # Master
    1518355089377464430,  # Administrator
    1518355089377464423,  # Owner
]

CHANGE_GENDER_ROLES = [
    1519426143701434640,  # Support
    1519426426636603462,  # Creative
    1519426936873554193,  # Control
    1518355089406955520,  # Moderator
    1520097774857879782,  # Curator
    1519713881017155644,  # Master
    1518355089377464430,  # Administrator
    1518355089377464423,  # Owner
]

# ============================================
# СТИЛЬ KURAI - ЦВЕТА
# ============================================
COLORS = {
    'primary': 0x6C5CE7,
    'secondary': 0x4A2B8F,
    'accent': 0x8B5CF6,
    'dark': 0x2D1B4E,
    'success': 0x00D4FF,
    'danger': 0xFF4757,
    'warning': 0xFFA502,
    'gold': 0xF1C40F,
    'purple': 0x6C5CE7,
    'cyan': 0x00D4FF,
}

# ============================================
# БАЗА ДАННЫХ
# ============================================
DATA_FILE = "staff_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

staff_data = load_data()

PUNISHMENT_FILE = "punishments.json"

def load_punishments():
    if os.path.exists(PUNISHMENT_FILE):
        with open(PUNISHMENT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_punishments(data):
    with open(PUNISHMENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

punishments = load_punishments()

# ============================================
# ИНИЦИАЛИЗАЦИЯ БОТА
# ============================================
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ============================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================

def get_staff_data(user_id):
    user_id = str(user_id)
    if user_id not in staff_data:
        staff_data[user_id] = {
            "points": 0,
            "verifications": 0,
            "bans": 0,
            "warnings": [],
            "strikes": 0,
            "is_dismissed": False
        }
        save_data(staff_data)
    return staff_data[user_id]

def clear_staff_profile(user_id):
    """Полностью очищает профиль сотрудника"""
    user_id = str(user_id)
    staff_data[user_id] = {
        "points": 0,
        "verifications": 0,
        "bans": 0,
        "warnings": [],
        "strikes": 0,
        "is_dismissed": False
    }
    save_data(staff_data)
    return staff_data[user_id]

def add_verification(user_id):
    data = get_staff_data(user_id)
    data["verifications"] += 1
    data["points"] += 1
    save_data(staff_data)

def add_ban(user_id):
    data = get_staff_data(user_id)
    data["bans"] += 1
    data["points"] += 2
    save_data(staff_data)

def has_any_role(user, role_ids):
    for role_id in role_ids:
        role = user.guild.get_role(role_id)
        if role and role in user.roles:
            return True
    return False

def is_staff(user):
    return has_any_role(user, STAFF_ROLES)

# ============================================
# СОБЫТИЯ
# ============================================

@bot.event
async def on_ready():
    print(f"✦ Бот {bot.user} запущен!")
    print(f"📊 ID бота: {bot.user.id}")
    
    try:
        await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print("✦ Команды синхронизированы!")
    except Exception as e:
        print(f"❌ Ошибка синхронизации: {e}")

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.id != GUILD_ID:
        return
    
    unverify_role = guild.get_role(UNVERIFY_ROLE_ID)
    if unverify_role:
        await member.add_roles(unverify_role, reason="Автоматическая выдача Unverify")
    
    try:
        embed = discord.Embed(
            title="✦ KURAI • ВЕРИФИКАЦИЯ",
            description=(
                "**ПОДТВЕРДИ СВОЙ АККАУНТ И ПОЛУЧИ ДОСТУП**\n"
                "к полному функционалу сервера **KURAI**\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🎙️ **КАК ПРОЙТИ ВЕРИФИКАЦИЮ:**\n"
                "• Зайди в любой голосовой канал в категории **«Приемная»**\n"
                "• Наши саппорты верифицируют тебя там\n\n"
                "📋 **ВАЖНО:** Ознакомься с правилами сервера!\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"✦ Добро пожаловать в KURAI, {member.mention}! ✦"
            ),
            color=COLORS['primary']
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        await member.send(embed=embed)
    except:
        pass
    
    notification_channel = guild.get_channel(NOTIFICATION_CHANNEL_ID)
    if notification_channel:
        embed = discord.Embed(
            title="✦ НОВЫЙ УЧАСТНИК",
            description=f"{member.mention} присоединился к серверу!",
            color=COLORS['primary']
        )
        embed.add_field(name="📅 Дата", value=datetime.now().strftime("%d.%m.%Y %H:%M"), inline=True)
        embed.add_field(name="🆔 ID", value=f"`{member.id}`", inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"✦ KURAI • Всего участников: {guild.member_count}")
        await notification_channel.send(embed=embed)

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.id in VOICE_CHANNELS_IDS:
        guild = member.guild
        unverify_role = guild.get_role(UNVERIFY_ROLE_ID)
        
        if unverify_role in member.roles:
            reception_category = guild.get_channel(RECEPTION_CATEGORY_ID)
            if reception_category:
                for channel in reception_category.channels:
                    if isinstance(channel, discord.TextChannel):
                        embed = discord.Embed(
                            title="✦ УЧАСТНИК В ГОЛОСОВОМ КАНАЛЕ",
                            description=(
                                f"{member.mention} зашел в **{after.channel.name}**\n"
                                "и готов к верификации!"
                            ),
                            color=COLORS['cyan']
                        )
                        embed.set_footer(text="✦ KURAI • Пригласите саппорта")
                        await channel.send(embed=embed)
                        break

# ============================================
# КОМАНДА: /action
# ============================================

@bot.tree.command(name="action", description="✦ Панель управления верификацией")
@app_commands.default_permissions(administrator=True)
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def action(interaction: discord.Interaction):
    if not is_staff(interaction.user):
        embed = discord.Embed(
            title="✦ ОШИБКА",
            description="У вас нет прав на использование этой команды!",
            color=COLORS['danger']
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(
        title="✦ ПАНЕЛЬ УПРАВЛЕНИЯ",
        description=(
            "**ВЕРИФИКАЦИЯ И УПРАВЛЕНИЕ**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📌 **ДОСТУПНЫЕ ДЕЙСТВИЯ:**\n"
            "• 🎭 Выдать гендерную роль\n"
            "• ⛔ Отстранение от верификации\n"
            "• 🔄 Сменить гендерную роль\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "✦ Выберите действие с помощью кнопок ниже"
        ),
        color=COLORS['primary']
    )
    embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
    embed.set_footer(text=f"✦ KURAI • Вызвал: {interaction.user.display_name}")
    
    view = ActionView()
    await interaction.response.send_message(embed=embed, view=view)

class ActionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label="🎭 Выдать гендер", style=discord.ButtonStyle.blurple, custom_id="gender", emoji="🎭")
    async def gender_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not has_any_role(interaction.user, GENDER_GIVER_ROLES):
            embed = discord.Embed(
                title="✦ ОШИБКА",
                description="У вас нет прав на выдачу гендерных ролей!",
                color=COLORS['danger']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        await interaction.response.send_modal(GenderSelectModal())
    
    @discord.ui.button(label="⛔ Отстранение", style=discord.ButtonStyle.danger, custom_id="ban", emoji="⛔")
    async def ban_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not has_any_role(interaction.user, GENDER_GIVER_ROLES):
            embed = discord.Embed(
                title="✦ ОШИБКА",
                description="У вас нет прав на отстранение!",
                color=COLORS['danger']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        await interaction.response.send_modal(PunishmentModal())
    
    @discord.ui.button(label="🔄 Сменить роль", style=discord.ButtonStyle.secondary, custom_id="change_role", emoji="🔄")
    async def change_role_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not has_any_role(interaction.user, CHANGE_GENDER_ROLES):
            embed = discord.Embed(
                title="✦ ОШИБКА",
                description="У вас нет прав на смену гендерных ролей!",
                color=COLORS['danger']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        await interaction.response.send_modal(ChangeGenderModal())

class GenderSelectModal(discord.ui.Modal, title="✦ Выбор гендерной роли"):
    user_id = discord.ui.TextInput(
        label="🆔 ID пользователя",
        placeholder="Введите ID участника",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user = await interaction.guild.fetch_member(int(self.user_id.value))
        except:
            embed = discord.Embed(
                title="✦ ОШИБКА",
                description="Пользователь не найден! Проверьте ID.",
                color=COLORS['danger']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title="✦ ВЫБОР ГЕНДЕРНОЙ РОЛИ",
            description=f"Выберите гендерную роль для {user.mention}:",
            color=COLORS['primary']
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text="✦ KURAI • Выберите роль")
        
        view = GenderChoiceView(user=user, modal_interaction=interaction)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class GenderChoiceView(discord.ui.View):
    def __init__(self, user, modal_interaction):
        super().__init__(timeout=120)
        self.user = user
        self.modal_interaction = modal_interaction
    
    @discord.ui.button(label="👨 Male", style=discord.ButtonStyle.blurple, custom_id="male", emoji="👨")
    async def male_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.give_gender_role(interaction, 'male')
    
    @discord.ui.button(label="👩 Female", style=discord.ButtonStyle.danger, custom_id="female", emoji="👩")
    async def female_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.give_gender_role(interaction, 'female')
    
    async def give_gender_role(self, interaction: discord.Interaction, gender_key: str):
        role_id = GENDER_ROLE_IDS.get(gender_key)
        if not role_id:
            embed = discord.Embed(
                title="✦ ОШИБКА",
                description=f"Роль '{gender_key}' не найдена в конфигурации!",
                color=COLORS['danger']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        role = interaction.guild.get_role(role_id)
        if not role:
            embed = discord.Embed(
                title="✦ ОШИБКА",
                description=f"Роль '{gender_key}' не найдена на сервере!",
                color=COLORS['danger']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await self.user.add_roles(role, reason="Выдача гендерной роли саппортом")
        
        unverify_role = interaction.guild.get_role(UNVERIFY_ROLE_ID)
        if unverify_role and unverify_role in self.user.roles:
            await self.user.remove_roles(unverify_role, reason="Пользователь верифицирован")
        
        add_verification(interaction.user.id)

        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)

        embed = discord.Embed(
            title="✦ ГЕНДЕРНАЯ РОЛЬ ВЫДАНА",
            description=f"Пользователю {self.user.mention} выдана роль **{role.name}**",
            color=COLORS['success']
        )
        embed.add_field(name="✦ Поинты", value="+1 поинт саппорту!", inline=False)
        embed.set_thumbnail(url=self.user.display_avatar.url)
        embed.set_footer(text=f"✦ KURAI • Выдал: {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

        notification_channel = interaction.guild.get_channel(NOTIFICATION_CHANNEL_ID)
        if notification_channel:
            embed_notify = discord.Embed(
                title="✦ ПОЛЬЗОВАТЕЛЬ ВЕРИФИЦИРОВАН",
                description=f"{self.user.mention} успешно верифицирован!",
                color=COLORS['success']
            )
            embed_notify.add_field(name="✦ Саппорт", value=interaction.user.mention, inline=True)
            embed_notify.add_field(name="✦ Роль", value=role.mention, inline=True)
            embed_notify.set_thumbnail(url=self.user.display_avatar.url)
            embed_notify.set_footer(text="✦ KURAI • Верификация завершена")
            await notification_channel.send(embed=embed_notify)

        try:
            feedback_embed = discord.Embed(
                title="✦ ОСТАВЬТЕ ОТЗЫВ О САППОРТЕ!",
                description=(
                    f"Вас верифицировал саппорт **{interaction.user.display_name}**!\n\n"
                    "Если вы хотите оставить отзыв о его работе, напишите ему в личные сообщения.\n"
                    "Ваше мнение очень важно для нас! 💜"
                ),
                color=COLORS['purple']
            )
            feedback_embed.set_footer(text="✦ KURAI • Спасибо за обратную связь!")
            await self.user.send(embed=feedback_embed)
        except:
            pass

class ChangeGenderModal(discord.ui.Modal, title="✦ Смена гендерной роли"):
    user_id = discord.ui.TextInput(
        label="🆔 ID пользователя",
        placeholder="Введите ID участника",
        required=True
    )
    new_role = discord.ui.TextInput(
        label="🎭 Новая гендерная роль",
        placeholder="Male или Female",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user = await interaction.guild.fetch_member(int(self.user_id.value))
        except:
            embed = discord.Embed(
                title="✦ ОШИБКА",
                description="Пользователь не найден!",
                color=COLORS['danger']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        for role_id in GENDER_ROLE_IDS.values():
            role = interaction.guild.get_role(role_id)
            if role and role in user.roles:
                await user.remove_roles(role)

        new_role = discord.utils.get(interaction.guild.roles, name=self.new_role.value)
        if not new_role:
            embed = discord.Embed(
                title="✦ ОШИБКА",
                description=f"Роль '{self.new_role.value}' не найдена!",
                color=COLORS['danger']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await user.add_roles(new_role, reason="Смена гендерной роли")

        embed = discord.Embed(
            title="✦ ГЕНДЕРНАЯ РОЛЬ ИЗМЕНЕНА",
            description=f"Пользователю {user.mention} выдана роль **{new_role.name}**",
            color=COLORS['gold']
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"✦ KURAI • Выдал: {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

        notification_channel = interaction.guild.get_channel(NOTIFICATION_CHANNEL_ID)
        if notification_channel:
            embed_notify = discord.Embed(
                title="✦ СМЕНА ГЕНДЕРНОЙ РОЛИ",
                description=f"У {user.mention} изменена гендерная роль!",
                color=COLORS['gold']
            )
            embed_notify.add_field(name="✦ Саппорт", value=interaction.user.mention, inline=True)
            embed_notify.add_field(name="🎭 Новая роль", value=new_role.mention, inline=True)
            embed_notify.set_footer(text="✦ KURAI • Роль изменена")
            await notification_channel.send(embed=embed_notify)

class PunishmentModal(discord.ui.Modal, title="✦ Отстранение от верификации"):
    user_id = discord.ui.TextInput(
        label="🆔 ID пользователя",
        placeholder="Введите ID участника",
        required=True
    )
    days = discord.ui.TextInput(
        label="📅 Количество дней",
        placeholder="Введите число (7, 14, 28)",
        required=True
    )
    reason = discord.ui.TextInput(
        label="📝 Причина отстранения",
        placeholder="Укажите причину",
        required=True,
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user = await interaction.guild.fetch_member(int(self.user_id.value))
            days = int(self.days.value)
        except:
            embed = discord.Embed(
                title="✦ ОШИБКА",
                description="Пользователь не найден или неверное количество дней!",
                color=COLORS['danger']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        end_date = datetime.now() + timedelta(days=days)
        
        punishments[str(user.id)] = {
            "reason": self.reason.value,
            "end_date": end_date.isoformat(),
            "days": days,
            "moderator": interaction.user.id
        }
        save_punishments(punishments)

        ban_role = interaction.guild.get_role(BANNED_ROLE_ID)
        if ban_role:
            await user.add_roles(ban_role, reason=f"Отстранение на {days} дней")
        
        unverify_role = interaction.guild.get_role(UNVERIFY_ROLE_ID)
        if unverify_role and unverify_role in user.roles:
            await user.remove_roles(unverify_role, reason="Пользователь отстранен")

        add_ban(interaction.user.id)

        embed = discord.Embed(
            title="✦ ОТСТРАНЕНИЕ ПРИМЕНЕНО",
            description=f"Пользователь {user.mention} отстранен на **{days} дней**.",
            color=COLORS['danger']
        )
        embed.add_field(name="📝 Причина", value=self.reason.value, inline=False)
        embed.add_field(name="✦ Поинты", value="+2 поинта саппорту!", inline=False)
        embed.add_field(name="📅 Дата окончания", value=end_date.strftime("%d.%m.%Y %H:%M"), inline=False)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"✦ KURAI • Выдал: {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

        notification_channel = interaction.guild.get_channel(NOTIFICATION_CHANNEL_ID)
        if notification_channel:
            embed_notify = discord.Embed(
                title="✦ ПОЛЬЗОВАТЕЛЬ ОТСТРАНЕН",
                description=f"{user.mention} отстранен от верификации!",
                color=COLORS['danger']
            )
            embed_notify.add_field(name="✦ Саппорт", value=interaction.user.mention, inline=True)
            embed_notify.add_field(name="📅 Дней", value=f"{days} дней", inline=True)
            embed_notify.add_field(name="📝 Причина", value=self.reason.value, inline=False)
            embed_notify.set_footer(text="✦ KURAI • Отстранение применено")
            await notification_channel.send(embed=embed_notify)

        try:
            await user.send(f"⛔ Вы были отстранены от верификации на **{days} дней**.\nПричина: {self.reason.value}")
        except:
            pass

# ============================================
# КОМАНДА: /staff_profile
# ============================================

@bot.tree.command(name="staff_profile", description="✦ Просмотр профиля сотрудника")
@app_commands.default_permissions(administrator=True)
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def staff_profile(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        member = interaction.user

    staff_role = interaction.guild.get_role(STAFF_ROLE_ID)
    if staff_role not in member.roles:
        embed = discord.Embed(
            title="✦ ОШИБКА",
            description="Этот пользователь не является сотрудником!",
            color=COLORS['danger']
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    data = get_staff_data(member.id)
    
    embed = discord.Embed(
        title=f"✦ ПРОФИЛЬ СОТРУДНИКА",
        description=f"**{member.display_name}**",
        color=COLORS['primary']
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    
    embed.add_field(
        name="✦ СТАТИСТИКА",
        value=(
            f"├ 🆔 ID: `{member.id}`\n"
            f"├ 📅 Вход: {member.joined_at.strftime('%d.%m.%Y')}\n"
            f"└ ⭐ Поинты: **{data['points']}**"
        ),
        inline=False
    )
    
    embed.add_field(
        name="✦ ДОСТИЖЕНИЯ",
        value=(
            f"├ Верификаций: **{data['verifications']}**\n"
            f"└ Отстранений: **{data['bans']}**"
        ),
        inline=True
    )
    
    status = "✦ Активен" if not data.get("is_dismissed") else "✦ Снят"
    embed.add_field(
        name="✦ СТАТУС",
        value=status,
        inline=True
    )
    
    embed.set_footer(text="✦ 1 верификация = 1 поинт • 1 отстранение = 2 поинта")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ============================================
# КОМАНДА: /staff (С ПОЛНОЙ ОЧИСТКОЙ ПРОФИЛЯ)
# ============================================

@bot.tree.command(name="staff", description="✦ Управление персоналом")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def staff(interaction: discord.Interaction):
    if not is_staff(interaction.user):
        embed = discord.Embed(
            title="✦ ОШИБКА",
            description="У вас нет прав на использование этой команды!",
            color=COLORS['danger']
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if not has_any_role(interaction.user, STAFF_MANAGEMENT_ROLES):
        embed = discord.Embed(
            title="✦ ОШИБКА",
            description="У вас нет прав на использование этой команды!",
            color=COLORS['danger']
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    embed = discord.Embed(
        title="✦ УПРАВЛЕНИЕ ПЕРСОНАЛОМ",
        description=(
            "**ПАНЕЛЬ УПРАВЛЕНИЯ СОТРУДНИКАМИ**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📌 **ДОСТУПНЫЕ ДЕЙСТВИЯ:**\n"
            "• ⚠️ Выдать предупреждение\n"
            "• ⛔ Снять с должности\n\n"
            "⚠️ **3 предупреждения** = автоматическое снятие\n"
            "🔄 При снятии **ВЕСЬ ПРОФИЛЬ** очищается:\n"
            "   • Поинты → 0\n"
            "   • Верификации → 0\n"
            "   • Отстранения → 0\n"
            "   • Предупреждения → 0\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "✦ Выберите действие с помощью кнопок ниже"
        ),
        color=COLORS['secondary']
    )
    embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
    embed.set_footer(text=f"✦ KURAI • Вызвал: {interaction.user.display_name}")
    
    view = StaffManagementView()
    await interaction.response.send_message(embed=embed, view=view)

class StaffManagementView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label="⚠️ Предупреждение", style=discord.ButtonStyle.danger, custom_id="warn", emoji="⚠️")
    async def warn_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(WarningModal())
    
    @discord.ui.button(label="⛔ Снять с должности", style=discord.ButtonStyle.danger, custom_id="dismiss", emoji="⛔")
    async def dismiss_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DismissModal())

class WarningModal(discord.ui.Modal, title="✦ Выдача предупреждения"):
    user_id = discord.ui.TextInput(
        label="🆔 ID сотрудника",
        placeholder="Введите ID участника",
        required=True
    )
    reason = discord.ui.TextInput(
        label="📝 Причина предупреждения",
        placeholder="Нарушение правил",
        required=True,
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user = await interaction.guild.fetch_member(int(self.user_id.value))
        except:
            embed = discord.Embed(
                title="✦ ОШИБКА",
                description="Пользователь не найден!",
                color=COLORS['danger']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        staff_role = interaction.guild.get_role(STAFF_ROLE_ID)
        if staff_role not in user.roles:
            embed = discord.Embed(
                title="✦ ОШИБКА",
                description="Этот пользователь не является сотрудником!",
                color=COLORS['danger']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        data = get_staff_data(user.id)
        data["warnings"].append(f"{self.reason.value} (выдал: {interaction.user.display_name})")
        data["strikes"] += 1
        
        if data["strikes"] >= 3:
            await user.remove_roles(staff_role, reason=f"{data['strikes']} предупреждений - снятие с должности")
            # ПОЛНОСТЬЮ ОЧИЩАЕМ ПРОФИЛЬ
            clear_staff_profile(user.id)
            dismiss_msg = f"\n\n🔄 **Весь профиль сотрудника ОЧИЩЕН!**"
            data = get_staff_data(user.id)  # Обновляем данные
        else:
            dismiss_msg = ""

        save_data(staff_data)

        embed = discord.Embed(
            title="✦ ПРЕДУПРЕЖДЕНИЕ ВЫДАНО",
            description=f"Сотруднику {user.mention} выдано предупреждение.",
            color=COLORS['warning']
        )
        embed.add_field(name="📝 Причина", value=self.reason.value, inline=False)
        
        if data.get("is_dismissed"):
            embed.add_field(
                name="🔄 ПРОФИЛЬ ОЧИЩЕН",
                value="✅ Все поинты, верификации, отстранения и предупреждения сброшены!",
                inline=False
            )
        else:
            embed.add_field(name="📊 Всего предупреждений", value=f"{data['strikes']}/3", inline=True)
        
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"✦ KURAI • Выдал: {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

        try:
            warn_msg = f"⚠️ Вы получили предупреждение!\nПричина: {self.reason.value}"
            if data.get("is_dismissed"):
                warn_msg += f"\n\n🔄 Вы сняты с должности!\nВесь ваш профиль ОЧИЩЕН:\n• Поинты → 0\n• Верификации → 0\n• Отстранения → 0\n• Предупреждения → 0"
            else:
                warn_msg += f"\nВсего: {data['strikes']}/3"
            await user.send(warn_msg)
        except:
            pass

class DismissModal(discord.ui.Modal, title="✦ Снятие с должности"):
    user_id = discord.ui.TextInput(
        label="🆔 ID сотрудника",
        placeholder="Введите ID участника",
        required=True
    )
    reason = discord.ui.TextInput(
        label="📝 Причина снятия",
        placeholder="Нарушение правил",
        required=True,
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user = await interaction.guild.fetch_member(int(self.user_id.value))
        except:
            embed = discord.Embed(
                title="✦ ОШИБКА",
                description="Пользователь не найден!",
                color=COLORS['danger']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        staff_role = interaction.guild.get_role(STAFF_ROLE_ID)
        if staff_role not in user.roles:
            embed = discord.Embed(
                title="✦ ОШИБКА",
                description="Этот пользователь не является сотрудником!",
                color=COLORS['danger']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await user.remove_roles(staff_role, reason=f"Снятие с должности: {self.reason.value}")
        
        # ПОЛНОСТЬЮ ОЧИЩАЕМ ПРОФИЛЬ
        clear_staff_profile(user.id)
        data = get_staff_data(user.id)  # Получаем очищенные данные

        embed = discord.Embed(
            title="✦ СОТРУДНИК СНЯТ С ДОЛЖНОСТИ",
            description=f"{user.mention} снят с должности.",
            color=COLORS['danger']
        )
        embed.add_field(name="📝 Причина", value=self.reason.value, inline=False)
        embed.add_field(
            name="🔄 ПРОФИЛЬ ОЧИЩЕН",
            value="✅ Все поинты, верификации, отстранения и предупреждения сброшены!",
            inline=False
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"✦ KURAI • Выдал: {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

        try:
            await user.send(
                f"⛔ Вы сняты с должности!\n"
                f"Причина: {self.reason.value}\n\n"
                f"🔄 Весь ваш профиль ОЧИЩЕН:\n"
                f"• Поинты → 0\n"
                f"• Верификации → 0\n"
                f"• Отстранения → 0\n"
                f"• Предупреждения → 0\n\n"
                f"При повторном назначении вы начинаете с чистого листа."
            )
        except:
            pass

# ============================================
# КОМАНДА: /view_avatar
# ============================================

@bot.tree.command(name="view_avatar", description="✦ Просмотр аватара пользователя")
@app_commands.default_permissions(administrator=True)
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def view_avatar(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        member = interaction.user

    embed = discord.Embed(
        title=f"✦ АВАТАР {member.display_name}",
        color=COLORS['primary']
    )
    embed.set_image(url=member.display_avatar.url)
    embed.set_footer(text=f"✦ KURAI • ID: {member.id} • Запросил: {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ============================================
# КОМАНДА: /punishment
# ============================================

@bot.tree.command(name="punishment", description="✦ Просмотр наказаний пользователя")
@app_commands.default_permissions(administrator=True)
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def punishment(interaction: discord.Interaction, member: discord.Member):
    if not is_staff(interaction.user):
        embed = discord.Embed(
            title="✦ ОШИБКА",
            description="У вас нет прав на использование этой команды!",
            color=COLORS['danger']
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    user_id = str(member.id)
    
    if user_id not in punishments:
        embed = discord.Embed(
            title="✦ ИНФОРМАЦИЯ",
            description=f"У пользователя {member.mention} нет активных наказаний.",
            color=COLORS['primary']
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    data = punishments[user_id]
    end_date = datetime.fromisoformat(data["end_date"])
    remaining = end_date - datetime.now()
    days_left = remaining.days

    embed = discord.Embed(
        title=f"✦ НАКАЗАНИЕ ДЛЯ {member.display_name}",
        color=COLORS['danger']
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="📝 Причина", value=data["reason"], inline=False)
    embed.add_field(name="📅 Дней", value=data["days"], inline=True)
    embed.add_field(name="⏳ Осталось", value=days_left if days_left > 0 else "Истекло", inline=True)
    embed.add_field(name="👤 Выдал", value=f"<@{data['moderator']}>", inline=False)
    embed.add_field(name="📅 Дата окончания", value=end_date.strftime("%d.%m.%Y %H:%M"), inline=False)
    embed.set_footer(text=f"✦ KURAI • ID: {member.id}")

    await interaction.response.send_message(embed=embed, ephemeral=True)

# ============================================
# КОМАНДА: /ping
# ============================================

@bot.tree.command(name="ping", description="✦ Проверка работы бота")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    
    embed = discord.Embed(
        title="✦ ПОНГ!",
        description=f"Задержка: **{latency} мс**",
        color=COLORS['primary']
    )
    embed.add_field(name="✦ Статус", value="✅ Бот работает", inline=True)
    embed.add_field(name="✦ Время", value=datetime.now().strftime("%H:%M:%S"), inline=True)
    embed.set_footer(text=f"✦ KURAI • Вызвал: {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)

# ============================================
# ЗАПУСК БОТА
# ============================================

if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ ОШИБКА: Неправильный токен!")
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")