import pygame
import random
import sys
import math
import os

# ============================================================
# INITIALISE
# ============================================================

pygame.init()

# Optional audio and character art live next to this script.  PNG is preferred
# for Soggy Cat because it can preserve transparency, but JPG also works.
ASSET_DIR = os.path.dirname(os.path.abspath(__file__))
MENU_MUSIC_FILES = ("menu_music.ogg", "menu_music.mp3", "menu_music.wav",
                    "menu.ogg", "menu.mp3", "menu.wav")
INGAME_MUSIC_FILES = ("ingame_music.ogg", "ingame_music.mp3", "ingame_music.wav",
                      "game_music.ogg", "game_music.mp3", "game_music.wav")
SOGGY_CAT_FILES = ("soggycat.png", "soggycat.jpg", "soggycat.jpeg")
DEVELOPER_IMAGE_FILES = ("developer.jpg", "developer.jpeg", "developer.png")

# ------------------------------------------------------------
# VERSION    Short version string shown across the UI.
# ------------------------------------------------------------
GAME_VERSION = "V1.8"

current_music = None
music_volume = 0.45

try:
    if not pygame.mixer.get_init():
        pygame.mixer.init()
except pygame.error:
    pass


def distance(x1, y1, x2, y2):
    """Return the straight-line distance between two points."""
    return math.hypot(x2 - x1, y2 - y1)


def asset_roots():
    """Return candidate folders for optional assets (source run and packaged exe)."""
    roots = [ASSET_DIR]
    if hasattr(sys, "_MEIPASS"):
        roots.append(sys._MEIPASS)
    roots.append(os.path.dirname(os.path.abspath(sys.executable)))
    seen = set()
    unique = []
    for root in roots:
        root = os.path.normcase(os.path.abspath(root))
        if root not in seen:
            seen.add(root)
            unique.append(root)
    return unique


def find_asset(filenames):
    """Return the first supplied asset found beside the game, if any."""
    for root in asset_roots():
        for filename in filenames:
            path = os.path.join(root, filename)
            if os.path.isfile(path):
                return path
    return None


def ensure_mixer():
    """Make sure the mixer is running, retrying if the audio device was busy."""
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        return pygame.mixer.get_init() is not None
    except pygame.error:
        return False


def play_music(kind):
    """Loop the appropriate optional menu or in-game track without crashing."""
    global current_music
    if not ensure_mixer():
        return
    filenames = MENU_MUSIC_FILES if kind == "menu" else INGAME_MUSIC_FILES
    music_path = find_asset(filenames)
    if music_path == current_music:
        return
    try:
        if music_path:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()
        current_music = music_path
    except pygame.error:
        # Sound hardware/codecs are optional; gameplay should still start.
        current_music = None


def set_music_volume(value):
    """Set music volume from 0.0 to 1.0 and apply it immediately."""
    global music_volume
    music_volume = max(0.0, min(1.0, float(value)))
    if not ensure_mixer():
        return
    try:
        pygame.mixer.music.set_volume(music_volume)
    except pygame.error:
        pass


def stop_music():
    """Silence the menu track during active combat."""
    global current_music
    try:
        pygame.mixer.music.stop()
    except pygame.error:
        pass
    current_music = None


def load_soggy_cat_image():
    """Load and scale Soggy Cat art, returning None when it has not been added yet."""
    image_path = find_asset(SOGGY_CAT_FILES)
    if not image_path:
        return None
    try:
        image = pygame.image.load(image_path).convert_alpha()
        return pygame.transform.smoothscale(image, (40, 40))
    except pygame.error:
        return None

WINDOWED_SIZE = (800, 600)
WIDTH, HEIGHT = WINDOWED_SIZE
screen = pygame.display.set_mode(WINDOWED_SIZE)


pygame.mouse.set_visible(False)


# ============================================================
# DEVELOPER CREDIT
# ============================================================

developer_image = None


def load_developer_image():
    """Load the developer JPG/PNG and scale it for the top-right credit."""
    global developer_image
    if developer_image is not None:
        return developer_image

    image_path = find_asset(DEVELOPER_IMAGE_FILES)
    if not image_path:
        return None
    try:
        image = pygame.image.load(image_path).convert()
        developer_image = pygame.transform.smoothscale(image, (70, 70))
        return developer_image
    except pygame.error:
        return None


def draw_developer_credit():
    """Draw 'Developer' with the developer image directly underneath."""
    label = font_enemy.render("Developer", True, ACCENT)
    x = 12
    y = 10
    screen.blit(label, (x, y))

    image = load_developer_image()
    if image is not None:
        image_x = 12
        image_y = y + label.get_height() + 5
        screen.blit(image, (image_x, image_y))


# ============================================================
# CUSTOM CURSOR
# ============================================================

def draw_custom_cursor():
    """Draw a clean circular cursor on top of everything."""
    mx, my = pygame.mouse.get_pos()
    glow_circle((mx, my), 9, ACCENT, 18)
    pygame.draw.circle(screen, ACCENT, (mx, my), 7, 2)
    pygame.draw.circle(screen, WHITE, (mx, my), 2)

pygame.display.set_caption("Cardijn Battlegrounds")

clock = pygame.time.Clock()
FPS = 120


# ============================================================
# COLOURS
# ============================================================

WHITE = (245, 248, 255)
GREEN = (70, 235, 145)
RED = (255, 75, 95)
TEAR_BLUE = (125, 220, 255)
BLACK = (7, 9, 15)
YELLOW = (255, 215, 80)
GRAY = (42, 48, 62)
LIGHT_GRAY = (160, 170, 190)

PURPLE = (180, 0, 180)
ORANGE = (255, 128, 0)
DARK_ORANGE = (220, 80, 0)
CYAN = (0, 220, 220)
PINK = (255, 80, 180)
DARK_BLUE = (40, 80, 220)
LIME = (100, 255, 50)
BROWN = (140, 80, 30)

GOLD = (255, 190, 0)
DARK_RED = (130, 0, 0)
SPEED_GREEN = (50, 255, 100)
FIRE_RED = (255, 80, 50)

SHOP_BLUE = (60, 130, 255)


# ============================================================
# THEMES
# ============================================================

THEMES = {
    "Midnight": {
        "BG_TOP": (8, 12, 24), "BG_BOTTOM": (17, 22, 38),
        "PANEL": (20, 26, 43), "PANEL_2": (25, 32, 52),
        "BORDER": (62, 75, 105), "MUTED": (105, 118, 145),
        "ACCENT": (75, 170, 255), "ACCENT_2": (125, 90, 255),
        "GLOW": (100, 200, 255), "GRID": (24, 31, 50),
    },
    "Neon Green": {
        "BG_TOP": (4, 16, 10), "BG_BOTTOM": (10, 31, 20),
        "PANEL": (10, 25, 18), "PANEL_2": (15, 38, 26),
        "BORDER": (35, 100, 62), "MUTED": (90, 145, 110),
        "ACCENT": (55, 255, 125), "ACCENT_2": (20, 190, 100),
        "GLOW": (70, 255, 150), "GRID": (18, 55, 35),
    },
    "Crimson": {
        "BG_TOP": (22, 5, 9), "BG_BOTTOM": (42, 10, 18),
        "PANEL": (35, 12, 19), "PANEL_2": (50, 16, 25),
        "BORDER": (115, 38, 52), "MUTED": (160, 95, 105),
        "ACCENT": (255, 65, 90), "ACCENT_2": (210, 35, 70),
        "GLOW": (255, 80, 105), "GRID": (62, 20, 30),
    },
    "Purple Void": {
        "BG_TOP": (13, 7, 24), "BG_BOTTOM": (29, 12, 48),
        "PANEL": (25, 15, 42), "PANEL_2": (36, 20, 58),
        "BORDER": (91, 57, 130), "MUTED": (135, 110, 160),
        "ACCENT": (190, 100, 255), "ACCENT_2": (115, 70, 235),
        "GLOW": (205, 125, 255), "GRID": (45, 27, 70),
    },
    "Cyberpunk": {
        "BG_TOP": (4, 10, 20), "BG_BOTTOM": (12, 19, 31),
        "PANEL": (9, 20, 29), "PANEL_2": (14, 30, 40),
        "BORDER": (35, 92, 105), "MUTED": (95, 145, 155),
        "ACCENT": (0, 240, 220), "ACCENT_2": (255, 55, 190),
        "GLOW": (30, 255, 235), "GRID": (15, 55, 62),
    },
    "Amber": {
        "BG_TOP": (20, 12, 4), "BG_BOTTOM": (39, 23, 7),
        "PANEL": (34, 22, 10), "PANEL_2": (48, 31, 13),
        "BORDER": (112, 76, 31), "MUTED": (160, 125, 78),
        "ACCENT": (255, 175, 45), "ACCENT_2": (235, 105, 20),
        "GLOW": (255, 195, 65), "GRID": (60, 40, 16),
    },
}

CURRENT_THEME = "Midnight"

# Active theme colours
BG_TOP = THEMES[CURRENT_THEME]["BG_TOP"]
BG_BOTTOM = THEMES[CURRENT_THEME]["BG_BOTTOM"]
PANEL = THEMES[CURRENT_THEME]["PANEL"]
PANEL_2 = THEMES[CURRENT_THEME]["PANEL_2"]
BORDER = THEMES[CURRENT_THEME]["BORDER"]
MUTED = THEMES[CURRENT_THEME]["MUTED"]
ACCENT = THEMES[CURRENT_THEME]["ACCENT"]
ACCENT_2 = THEMES[CURRENT_THEME]["ACCENT_2"]
GLOW = THEMES[CURRENT_THEME]["GLOW"]

def apply_theme(name):
    """Apply a theme's colours and rebuild the cached background."""
    global CURRENT_THEME, BG_TOP, BG_BOTTOM, PANEL, PANEL_2, BORDER, MUTED
    global ACCENT, ACCENT_2, GLOW, BACKGROUND_SURFACE, VIGNETTE_SURFACE
    CURRENT_THEME = name
    theme = THEMES[name]
    BG_TOP = theme["BG_TOP"]
    BG_BOTTOM = theme["BG_BOTTOM"]
    PANEL = theme["PANEL"]
    PANEL_2 = theme["PANEL_2"]
    BORDER = theme["BORDER"]
    MUTED = theme["MUTED"]
    ACCENT = theme["ACCENT"]
    ACCENT_2 = theme["ACCENT_2"]
    GLOW = theme["GLOW"]

    BACKGROUND_SURFACE = pygame.Surface((WIDTH, HEIGHT)).convert()
    for y in range(HEIGHT):
        t = y / max(1, HEIGHT - 1)
        colour = tuple(int(BG_TOP[i] * (1 - t) + BG_BOTTOM[i] * t) for i in range(3))
        pygame.draw.line(BACKGROUND_SURFACE, colour, (0, y), (WIDTH, y))

    grid = theme["GRID"]
    for x in range(0, WIDTH, 40):
        pygame.draw.line(BACKGROUND_SURFACE, grid, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(BACKGROUND_SURFACE, grid, (0, y), (WIDTH, y), 1)

    VIGNETTE_SURFACE = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(VIGNETTE_SURFACE, (*GLOW, 18), (WIDTH // 2, HEIGHT // 2), 330)

# ============================================================
# FONTS
# ============================================================

font_title = pygame.font.SysFont("segoe ui", 52, bold=True)
font_big = pygame.font.SysFont("segoe ui", 38, bold=True)
font_ui = pygame.font.SysFont("segoe ui", 24, bold=True)
font_enemy = pygame.font.SysFont("segoe ui", 16, bold=True)
font_small = pygame.font.SysFont("segoe ui", 14)
font_tiny = pygame.font.SysFont("segoe ui", 11)


# Cached static background
apply_theme(CURRENT_THEME)


# ============================================================
# POLISHED UI HELPERS
# ============================================================

def draw_gradient_background():
    """Blit the pre-rendered background instead of rebuilding it every frame."""
    screen.blit(BACKGROUND_SURFACE, (0, 0))
    screen.blit(VIGNETTE_SURFACE, (0, 0))


def panel(rect, fill=PANEL, border=BORDER, radius=14, width=1, shadow=True):
    """Draw a soft, layered card so menus and HUD elements feel more modern."""
    if shadow:
        shadow_surf = pygame.Surface((rect.w + 18, rect.h + 18), pygame.SRCALPHA)
        shadow_rect = pygame.Rect(9, 10, rect.w, rect.h)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 75), shadow_rect, border_radius=radius + 2)
        screen.blit(shadow_surf, (rect.x - 9, rect.y - 7))
    pygame.draw.rect(screen, fill, rect, border_radius=radius)
    if width:
        pygame.draw.rect(screen, border, rect, width, border_radius=radius)


def draw_ui_shadow(rect, radius=10, offset=(0, 5), alpha=85, spread=6):
    """Draw a soft drop shadow behind a UI element without tinting its text."""
    shadow = pygame.Surface((rect.w + spread * 2, rect.h + spread * 2), pygame.SRCALPHA)
    shadow_rect = pygame.Rect(spread, spread, rect.w, rect.h)
    pygame.draw.rect(shadow, (0, 0, 0, alpha), shadow_rect, border_radius=radius)
    screen.blit(shadow, (rect.x - spread + offset[0], rect.y - spread + offset[1]))


def draw_text_shadow(text, font, colour, x, y, offset=(2, 2), alpha=140):
    """Draw a clean offset shadow first, then the actual text."""
    shadow = font.render(text, True, (0, 0, 0))
    shadow.set_alpha(alpha)
    screen.blit(shadow, (x + offset[0], y + offset[1]))
    surf = font.render(text, True, colour)
    screen.blit(surf, (x, y))
    return surf


def button(rect, label, active=False, accent=None, subtitle=None):
    """Consistent modern button with hover/selection treatment."""
    accent = accent or ACCENT
    burst_on_hover(rect, accent)
    if active:
        draw_rect_glow(rect, accent, radius=10, alpha=50, spread=10)
    draw_ui_shadow(rect, radius=10, offset=(0, 4), alpha=65, spread=5)
    if active:
        pygame.draw.rect(screen, accent, rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, rect, 1, border_radius=10)
        text_colour = BLACK
    else:
        pygame.draw.rect(screen, PANEL_2, rect, border_radius=10)
        pygame.draw.rect(screen, BORDER, rect, 1, border_radius=10)
        text_colour = WHITE
    surf = font_ui.render(label, True, text_colour)
    screen.blit(surf, (rect.centerx - surf.get_width() // 2, rect.centery - surf.get_height() // 2))
    if subtitle:
        sub = font_tiny.render(subtitle, True, MUTED if not active else BLACK)
        screen.blit(sub, (rect.centerx - sub.get_width() // 2, rect.bottom - 16))


def section_label(text, x, y, colour=None):
    colour = colour or ACCENT
    draw_text_shadow(text.upper(), font_tiny, colour, x, y, offset=(1, 1), alpha=120)
    surf = font_tiny.render(text.upper(), True, colour)
    pygame.draw.line(screen, colour, (x, y + surf.get_height() + 4), (x + 42, y + surf.get_height() + 4), 2)


def text_center(text, font, colour, y, x=None):
    surf = font.render(text, True, colour)
    if x is None:
        x = WIDTH // 2
    shadow = font.render(text, True, (0, 0, 0))
    shadow.set_alpha(125)
    screen.blit(shadow, (x - shadow.get_width() // 2 + 2, y + 2))
    screen.blit(surf, (x - surf.get_width() // 2, y))
    return surf


def glow_circle(pos, radius, colour, alpha=45):
    glow = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
    centre = (radius * 2, radius * 2)
    for r, a in [(radius * 2, alpha // 4),
                 (int(radius * 1.6), alpha // 3),
                 (radius, alpha)]:
        pygame.draw.circle(glow, (*colour, a), centre, r)
    screen.blit(
        glow,
        (int(pos[0] - radius * 2), int(pos[1] - radius * 2))
    )


def bar(rect, value, maximum, fill, back=(35, 40, 55), height=None):
    x, y, w, h = rect
    pygame.draw.rect(screen, back, (x, y, w, h), border_radius=h // 2)
    ratio = 0 if maximum <= 0 else max(0, min(1, value / maximum))
    fw = int(w * ratio)
    if fw > 0:
        pygame.draw.rect(screen, fill, (x, y, fw, h), border_radius=h // 2)
    pygame.draw.rect(screen, BORDER, (x, y, w, h), 1, border_radius=h // 2)


def badge(text, x, y, colour=ACCENT):
    surf = font_tiny.render(text.upper(), True, WHITE)
    rect = pygame.Rect(x, y, surf.get_width() + 18, surf.get_height() + 8)
    pygame.draw.rect(screen, (*colour,), rect, border_radius=8)
    screen.blit(surf, (rect.x + 9, rect.y + 4))
    return rect


# ============================================================
# ANIMATION HELPERS
# ============================================================

def lerp(a, b, t):
    """Smoothly interpolate between two values."""
    return a + (b - a) * t


def pulse_val(base=0.5, amplitude=0.35, period=0.5, offset=0):
    """Return an oscillating 0..1 value driven by the global clock."""
    t = pygame.time.get_ticks() / 1000.0
    return base + amplitude * math.sin(t * 2 * math.pi / period + offset)


def ease_out(t):
    """Smooth deceleration — useful for entrance motion."""
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def draw_rect_glow(rect, colour, radius=10, alpha=40, spread=12):
    """Draw a soft layered glow behind a rounded rectangle."""
    glow = pygame.Surface((rect.w + spread * 2, rect.h + spread * 2), pygame.SRCALPHA)
    for i in range(4):
        inner = pygame.Rect(spread, spread, rect.w, rect.h)
        inflate = int(spread * (1 - i / 4))
        inner.inflate_ip(-inflate * 2, -inflate * 2)
        pygame.draw.rect(glow, (*colour, alpha // (i + 1)), inner, border_radius=max(6, radius - i))
    screen.blit(glow, (rect.x - spread, rect.y - spread))


def draw_alpha_rect(rect, colour, radius=10, alpha=55):
    """Draw a rounded rectangle that fades into whatever is behind it."""
    surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    pygame.draw.rect(surf, (*colour, alpha), (0, 0, rect.w, rect.h), border_radius=radius)
    screen.blit(surf, rect.topleft)


def draw_fade_enter(age_frames, target_rect, drift=18):
    """Return a copy of *target_rect* eased upward while a menu fades in."""
    t = ease_out(age_frames / 16.0)
    moved = target_rect.copy()
    moved.y += int(drift * (1 - t))
    return moved


# ============================================================
# PARTICLE EFFECTS
# ============================================================
#
# A small, shared particle pool powers the menu hover bursts and
# the combat shooting/impact VFX.  Particles are plain dicts so
# they are cheap to spawn and cull even at 120 FPS.

MAX_PARTICLES = 500
g_particles = []   # {x, y, vx, vy, life, max_life, size, colour}
g_flashes = []     # short-lived muzzle glow {x, y, radius, life, max_life, colour, alpha}
_particle_surf_cache = {}   # (size, colour) -> pre-rendered soft dot


def spawn_burst(x, y, colour, count=14, speed=3.0, angle=0, spread=360,
                size=3, life=28, gravity=0.0):
    """Spawn a fan of particles anywhere from a full circle to a tight cone."""
    global g_particles
    if len(g_particles) >= MAX_PARTICLES:
        return
    for _ in range(count):
        if len(g_particles) >= MAX_PARTICLES:
            return
        a = math.radians(angle) + random.uniform(-math.radians(spread) * 0.5,
                                                 math.radians(spread) * 0.5)
        v = random.uniform(speed * 0.45, speed)
        g_particles.append({
            "x": x + random.uniform(-2, 2),
            "y": y + random.uniform(-2, 2),
            "vx": math.cos(a) * v,
            "vy": math.sin(a) * v,
            "life": random.randint(max(2, life // 2), life),
            "max_life": life,
            "size": random.uniform(size * 0.5, size),
            "colour": colour,
            "gravity": gravity,
        })


def update_fx():
    """Advance every live particle and muzzle flash by one frame."""
    for p in g_particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vx"] *= 0.90
        p["vy"] *= 0.90
        p["vy"] += p["gravity"]
        p["life"] -= 1
        if p["life"] <= 0:
            g_particles.remove(p)

    for f in g_flashes[:]:
        f["life"] -= 1
        if f["life"] <= 0:
            g_flashes.remove(f)


def draw_fx():
    """Draw the active particles and muzzle flashes above the scene."""
    for p in g_particles:
        alpha = int(255 * (p["life"] / p["max_life"]))
        size = max(1, int(p["size"]))
        key = (size, p["colour"])
        surf = _particle_surf_cache.get(key)
        if surf is None:
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*p["colour"], 255), (size, size), size)
            _particle_surf_cache[key] = surf
        surf.set_alpha(alpha)
        screen.blit(surf, (int(p["x"]) - size, int(p["y"]) - size))

    for f in g_flashes:
        p = min(1.0, f["life"] / f["max_life"])
        grow = f["radius"] * (1 + 0.8 * (1 - p))
        glow_circle((f["x"], f["y"]), grow, f["colour"], int(f["alpha"] * p))


# Tracks which buttons are hovered so a burst only fires on the
# transition from "not hovered" to "hovered", not every single frame.
_hover_state = {}


def burst_on_hover(rect, colour, spread=360):
    """Emit a small particle burst the moment the mouse enters a control."""
    key = (rect.x, rect.y, rect.w, rect.h)
    hovering = rect.collidepoint(pygame.mouse.get_pos())
    if hovering and not _hover_state.get(key, False):
        spawn_burst(rect.centerx, rect.centery, colour,
                    count=12, speed=2.4, spread=spread, size=2.5, life=22)
    _hover_state[key] = hovering


# ============================================================
# SCREEN TRANSITIONS
# ============================================================

FADE_STEP = 30           # overlay alpha change per frame
FADE_HOLD_FRAMES = 4     # frames held fully black before switching screens
fade_alpha = 0           # current overlay alpha 0..255
fade_mode = "idle"       # "idle" | "in" | "out"
fade_hold = 0            # frames held at full black
exit_ok = False          # True once a returning menu's fade-out has finished
_pending_action = None   # function to run after the fade-out completes


def tick_fade():
    """Advance the shared screen-fade animation once per frame."""
    global fade_alpha, fade_mode, fade_hold, exit_ok, _pending_action
    if fade_mode == "in":
        fade_alpha = max(0, fade_alpha - FADE_STEP)
        if fade_alpha <= 0:
            fade_mode = "idle"
            fade_hold = 0
    elif fade_mode == "out":
        fade_alpha = min(255, fade_alpha + FADE_STEP)
        if fade_alpha >= 255:
            fade_hold += 1
            if fade_hold >= FADE_HOLD_FRAMES:
                fade_hold = 0
                if _pending_action is not None:
                    action, _pending_action = _pending_action, None
                    fade_mode = "in"
                    fade_alpha = 255
                    action()
                else:
                    # Fade-out finished for a menu that is returning to its caller.
                    fade_mode = "in"
                    fade_alpha = 255
                    exit_ok = True


def draw_fade_overlay():
    """Draw the dark transition overlay at the current alpha."""
    if fade_alpha > 0:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(fade_alpha)))
        screen.blit(overlay, (0, 0))


def fade_out_blocking():
    """Synchronously fade the current screen to black before switching."""
    global fade_alpha, fade_mode, fade_hold, exit_ok
    if fade_mode != "idle":
        return 1
    fade_mode = "out"
    fade_alpha = 0
    fade_hold = 0
    exit_ok = False
    guard = 0
    while fade_mode == "out" and guard < FPS * 2:
        tick_fade()
        draw_fade_overlay()
        pygame.display.flip()
        clock.tick(FPS)
        guard += 1
    # Hand the new screen a fully black canvas to fade in from.
    fade_mode = "in"
    fade_alpha = 255
    exit_ok = False
    return 0


def run_transition(action):
    """Fade out the current screen, run *action* on black, then fade its frames in."""
    if fade_mode == "idle":
        fade_out_blocking()
    action()


def request_menu_exit():
    """Begin a fade-out so the active menu can return cleanly after it finishes."""
    global fade_alpha, fade_mode, fade_hold, exit_ok
    if fade_mode != "idle":
        return
    fade_mode = "out"
    fade_alpha = 0
    fade_hold = 0
    exit_ok = False


def reset_exit_ok():
    """Consume the exit signal raised by tick_fade after a menu fade-out."""
    global exit_ok
    exit_ok = False


# ============================================================
# CHARACTERS
# ============================================================
#
# ability:
#   name       = ability name
#   cooldown   = cooldown in seconds
#
# Monika is deliberately VERY OP.
# ============================================================

CHARACTERS = {

    "Ethan": {
        "hp": 60,
        "speed": 4.0,
        "t_speed": 18,
        "rate": 11,
        "range": 120,
        "damage": 5,
        "bullet_size": 5,
        "color": (0, 200, 255),
        "desc": "ouuh its ethan panini",
        "ability": "Panini Barrage",
        "ability_cd": 8,
        "ability_desc": "Fires sixteen panini shots in a ring around you."
    },

    "Mr Byrne": {
        "hp": 200,
        "speed": 3.5,
        "t_speed": 5,
        "rate": 22,
        "range": 50,
        "damage": 10,
        "bullet_size": 10,
        "color": (200, 0, 200),
        "desc": "big boy",
        "ability": "Big Slam",
        "ability_cd": 10,
        "ability_desc": "Slams the ground and damages every enemy around you."
    },

    "Pashmeet": {
        "hp": 20,
        "speed": 1.0,
        "t_speed": 3,
        "rate": 30,
        "range": 10,
        "damage": 1,
        "bullet_size": 1,
        "color": (255, 128, 0),
        "desc": "PASHMEET YOU SUCK",
        "ability": "PASHMEET RAGE",
        "ability_cd": 12,
        "ability_desc": "Enters a rage that boosts damage, speed and fire rate."
    },

    "Lucas": {
        "hp": 105,
        "speed": 5,
        "t_speed": 11,
        "rate": 17,
        "range": 55,
        "damage": 6,
        "bullet_size": 6,
        "color": (255, 50, 50),
        "desc": "hot damn",
        "ability": "Burning Dash",
        "ability_cd": 8,
        "ability_desc": "Gain a burst of speed and set fire to nearby enemies."
    },

    "Darcy": {
        "hp": 100,
        "speed": 4.3,
        "t_speed": 10,
        "rate": 16,
        "range": 50,
        "damage": 7,
        "bullet_size": 7,
        "color": CYAN,
        "desc": "darcy howard",
        "ability": "Ice Shield",
        "ability_cd": 12,
        "ability_desc": "Encases yourself in an ice shield that blocks damage."
    },

    "Mr Deng": {
        "hp": 130,
        "speed": 3.4,
        "t_speed": 15,
        "rate": 18,
        "range": 55,
        "damage": 4,
        "bullet_size": 4,
        "color": PURPLE,
        "desc": "daddy denguh~",
        "ability": "Deng Storm",
        "ability_cd": 10,
        "ability_desc": "Summons a storm of twelve shots around you."
    },

    "chudson mcchud": {
        "hp": 140,
        "speed": 5,
        "t_speed": 10,
        "rate": 16,
        "range": 50,
        "damage": 10,
        "bullet_size": 10,
        "color": DARK_ORANGE,
        "desc": "woah he a chuddy boi",
        "ability": "Chud Explosion",
        "ability_cd": 9,
        "ability_desc": "Detonates a huge explosion that damages everything."
    },

    "Jethro": {
        "hp": 120,
        "speed": 3,
        "t_speed": 7,
        "rate": 15,
        "range": 55,
        "damage": 6,
        "bullet_size": 6,
        "color": YELLOW,
        "desc": "tranjethro",
        "ability": "Jethro Beam",
        "ability_cd": 9,
        "ability_desc": "Fires a piercing beam at every nearby enemy."
    },

    "Lincoln": {
        "hp": 140,
        "speed": 2.5,
        "t_speed": 15,
        "rate": 10,
        "range": 60,
        "damage": 7,
        "bullet_size": 7,
        "color": DARK_BLUE,
        "desc": "lincolnstein",
        "ability": "Teleport",
        "ability_cd": 7,
        "ability_desc": "Blink away to safety and turn briefly invincible."
    },

    "Jack": {
        "hp": 200,
        "speed": 2.8,
        "t_speed": 30,
        "rate": 30,
        "range": 140,
        "damage": 10,
        "bullet_size": 10,
        "color": BROWN,
        "desc": "one legged strong dude",
        "ability": "Jack Nuke",
        "ability_cd": 14,
        "ability_desc": "Drops a massive nuke that wipes nearby enemies."
    },

    "Lenny": {
        "hp": 130,
        "speed": 4.2,
        "t_speed": 10,
        "rate": 19,
        "range": 50,
        "damage": 11,
        "bullet_size": 11,
        "color": LIME,
        "desc": "sick as",
        "ability": "Lenny Rush",
        "ability_cd": 8,
        "ability_desc": "Rush at high speed and fire a ring of shots."
    },

    "straight teeth": {
        "hp": 70,
        "speed": 3.0,
        "t_speed": 8,
        "rate": 16,
        "range": 50,
        "damage": 9,
        "bullet_size": 9,
        "color": PINK,
        "desc": "AUGH STOP IT HURTS",
        "ability": "Pain Field",
        "ability_cd": 10,
        "ability_desc": "Summons a pain field that damages enemies inside."
    },

    "Toby": {
        "hp": 200,
        "speed": 2.8,
        "t_speed": 9,
        "rate": 15,
        "range": 55,
        "damage": 9,
        "bullet_size": 9,
        "color": ORANGE,
        "desc": "big toby",
        "ability": "Toby Charge",
        "ability_cd": 9,
        "ability_desc": "Charge forward with momentum and slam nearby enemies."
    },

    "Kirat": {
        "hp": 100,
        "speed": 5.1,
        "t_speed": 9,
        "rate": 15,
        "range": 55,
        "damage": 7,
        "bullet_size": 7,
        "color": CYAN,
        "desc": "jaskirat singhle",
        "ability": "Kirat Multishot",
        "ability_cd": 8,
        "ability_desc": "Fires a massive ring of multishot bullets."
    },

    "Mr Ginn": {
        "hp": 155,
        "speed": 3.4,
        "t_speed": 7,
        "rate": 19,
        "range": 65,
        "damage": 8,
        "bullet_size": 8,
        "color": PURPLE,
        "desc": "this guy sucks",
        "ability": "Ginn Zone",
        "ability_cd": 10,
        "ability_desc": "Creates a zone that constantly damages enemies."
    },

    "Bentley": {
        "hp": 50,
        "speed": 3.4,
        "t_speed": 10,
        "rate": 13,
        "range": 55,
        "damage": 6,
        "bullet_size": 6,
        "color": GOLD,
        "desc": "he small n weak but fast kinda maybe",
        "ability": "Tiny Speed",
        "ability_cd": 7,
        "ability_desc": "Massively boosts speed and fire rate with shields."
    },

    "Beau": {
        "hp": 150,
        "speed": 4.2,
        "t_speed": 7,
        "rate": 20,
        "range": 65,
        "damage": 6,
        "bullet_size": 6,
        "color": (100, 150, 255),
        "desc": "im too lazy for this",
        "ability": "Beau Blast",
        "ability_cd": 10,
        "ability_desc": "Fires a 360-degree blast of heavy shots."
    },

    "Billy": {
        "hp": 120,
        "speed": 5.4,
        "t_speed": 14,
        "rate": 12,
        "range": 48,
        "damage": 7,
        "bullet_size": 7,
        "color": (255, 100, 100),
        "desc": "bily",
        "ability": "Billy Blitz",
        "ability_cd": 7,
        "ability_desc": "Blitz yourself with speed and a ring of shots."
    },

    "Will": {
        "hp": 125,
        "speed": 4.4,
        "t_speed": 8,
        "rate": 14,
        "range": 70,
        "damage": 6,
        "bullet_size": 6,
        "color": (100, 255, 180),
        "desc": "wilhod studios can you sponsor me",
        "ability": "Will Heal",
        "ability_cd": 12,
        "ability_desc": "Restore half your health and gain brief shields."
    },

    "Wyatt": {
        "hp": 145,
        "speed": 3.9,
        "t_speed": 8,
        "rate": 17,
        "range": 65,
        "damage": 8,
        "bullet_size": 8,
        "color": (180, 100, 255),
        "desc": "ok",
        "ability": "Wyatt Storm",
        "ability_cd": 10,
        "ability_desc": "Conjures a storm of shots all around you."
    },

    # ========================================================
    # NEW CHARACTERS
    # ========================================================

    "Arron": {
        "hp": 160,
        "speed": 4.6,
        "t_speed": 30,
        "rate": 10,
        "range": 75,
        "damage": 10,
        "bullet_size": 20,
        "color": (255, 180, 50),
        "desc": "Arronchini ball",
        "ability": "Arron Barrage",
        "ability_cd": 8,
        "ability_desc": "Fires three rings of heavy Arronchini shots."
    },

    "Jett": {
        "hp": 115,
        "speed": 6.5,
        "t_speed": 17,
        "rate": 10,
        "range": 90,
        "damage": 8,
        "bullet_size": 8,
        "color": (80, 255, 255),
        "desc": "jet engine                                                                                                                                                ",
        "ability": "JETT OVERDRIVE",
        "ability_cd": 15,
        "ability_desc": "Blasts a burst while hugely boosting speed and fire rate."
    },

    "Lachie": {
        "hp": 145,
        "speed": 5.0,
        "t_speed": 14,
        "rate": 14,
        "range": 75,
        "damage": 8,
        "bullet_size": 8,
        "color": (80, 255, 140),
        "desc": "Lachie goes turbo",
        "ability": "Lachie Turbo",
        "ability_cd": 10,
        "ability_desc": "Go turbo: fast movement, fast firing and a quick ring."
    },

    "Jakub": {
        "hp": 175,
        "speed": 3.8,
        "t_speed": 12,
        "rate": 16,
        "range": 85,
        "damage": 9,
        "bullet_size": 9,
        "color": (255, 220, 60),
        "desc": "Jakub calls in the chaos",
        "ability": "Jakub Meteor",
        "ability_cd": 11,
        "ability_desc": "Calls a huge meteor that smashes every enemy."
    },

    "Ben": {
        "hp": 110,
        "speed": 5.6,
        "t_speed": 16,
        "rate": 12,
        "range": 100,
        "damage": 7,
        "bullet_size": 7,
        "color": (255, 100, 210),
        "desc": "Ben disappears and strikes back",
        "ability": "Ben Phantom",
        "ability_cd": 9,
        "ability_desc": "Vanish, become invincible, then strike from everywhere."
    },

    "Brianna": {
        "hp": 125,
        "speed": 4.5,
        "t_speed": 13,
        "rate": 14,
        "range": 80,
        "damage": 8,
        "bullet_size": 8,
        "color": (255, 110, 190),
        "desc": "Brianna brings the pressure",
        "ability": "Brianna Barrage",
        "ability_cd": 9,
        "ability_desc": "Fires a barrage around you while gaining speed."
    },

    "Kody": {
        "hp": 140,
        "speed": 5.2,
        "t_speed": 14,
        "rate": 13,
        "range": 70,
        "damage": 8,
        "bullet_size": 8,
        "color": (255, 150, 100),
        "desc": "kody my goat",
        "ability": "Kody Cyclone",
        "ability_cd": 9,
        "ability_desc": "Whips up a cyclone of shots and briefly shields you."
    },

    "Monika": {
        "hp": 1000,
        "speed": 7.0,
        "t_speed": 25,
        "rate": 4,
        "range": 250,
        "damage": 25,
        "bullet_size": 25,
        "color": (255, 50, 150),
        "desc": "MONIKA IS ABSOLUTELY BROKEN",
        "ability": "MONIKA DELETES EVERYTHING",
        "ability_cd": 5,
        "ability_desc": "Deletes every enemy on screen and turns you invincible."
    },

    "Soggy Cat": {
        "hp": 135,
        "speed": 4.8,
        "t_speed": 12,
        "rate": 14,
        "range": 150,
        "damage": 6,
        "bullet_size": 12,
        "color": (120, 190, 255),
        "desc": "soggy but surprisingly dangerous",
        "ability": "Soggy Spray",
        "ability_cd": 8,
        "ability_desc": "Sprays a soggy barrage of shots everywhere."
    },

    # Hidden characters.
    "Kempson": {
        "hp": 180, "speed": 3.9, "t_speed": 14, "rate": 12,
        "range": 90, "damage": 10, "bullet_size": 10,
        "color": (255, 205, 80), "desc": "the secret shopkeeper has entered the arena",
        "ability": "Kempson Deal", "ability_cd": 10,
        "ability_desc": "The shopkeeper deals heavy damage to everyone nearby."
    },}


# Monika is intentionally hidden behind the character-select puzzle.
monika_unlocked = False
soggy_cat_unlocked = True
kempson_unlocked = True


# ============================================================
# ENEMIES
# ============================================================

ENEMY_NAMES = [
    "Lucas",
    "Darcy",
    "Mr Deng",
    "chudson mcchud",
    "Jethro",
    "Lincoln",
    "Jack",
    "Lenny",
    "straight teeth",
    "Toby",
    "Kirat",
    "Mr Ginn",
    "Bentley",
    "Beau",
    "Billy",
    "Will",
    "Wyatt"
]


CHARACTER_PASSIVES = {
    "Ethan": ("MOMENTUM", "Moving makes your shots faster."),
    "Mr Byrne": ("TANK", "Take 25% less damage, but move slower."),
    "Pashmeet": ("BERSERKER", "Damage rises as your HP gets lower."),
    "Lucas": ("BURNOUT", "Moving gives you a small damage boost."),
    "Darcy": ("GUARDIAN", "Periodically blocks one hit completely."),
    "Mr Deng": ("STORM", "Every few shots fire an extra projectile."),
    "chudson mcchud": ("BOOM", "Kills create a small damaging explosion."),
    "Jethro": ("SNIPER", "Standing still charges your shots for bonus damage."),
    "Lincoln": ("PHASE", "Chance to dodge incoming enemy bullets."),
    "Jack": ("HEAVY HITTER", "Close enemies take extra damage from your shots."),
    "Lenny": ("RUSHER", "Deal more damage while moving."),
    "straight teeth": ("GLASS CANNON", "Deal 35% more damage, but have less HP."),
    "Toby": ("CHARGE", "Moving builds momentum for stronger shots."),
    "Kirat": ("MULTISHOT", "Every fourth shot fires two side projectiles."),
    "Mr Ginn": ("CONTROL", "Nearby enemies are slowed."),
    "Bentley": ("TINY", "Smaller hitbox and very fast firing."),
    "Beau": ("BALANCED", "Reliable all-rounder with no major weakness."),
    "Billy": ("BLITZ", "Moving increases your fire rate."),
    "Will": ("VITALITY", "Kills restore a small amount of HP."),
    "Wyatt": ("CHAIN", "Shots have a chance to split toward another enemy."),
    "Arron": ("CANNON", "Large projectiles hit harder."),
    "Jett": ("OVERDRIVE", "Moving greatly improves fire rate."),
    "Lachie": ("TURBO", "Constant movement increases speed further."),
    "Jakub": ("METEOR", "Every eighth shot calls down a heavy blast."),
    "Ben": ("PHANTOM", "Chance to ignore incoming damage."),
    "Brianna": ("BARRAGE", "Continuous firing builds bonus damage."),
    "Monika": ("DELETE", "Shots pierce enemies and never stop on hit."),
    "Soggy Cat": ("AUTO AIM", "Automatically fires piercing shots at enemies."),
    "Kempson": ("DEALER", "Every kill has a chance to refund your ability cooldown."),
    "Kody": ("CYCLONE", "Moving while firing boosts your fire rate."),
}

# ============================================================
# PLAYER
# ============================================================

class PlayerEntity:

    def __init__(self, name, stats):

        self.name = name
        self.sprite = load_soggy_cat_image() if name == "Soggy Cat" else None

        self.x = WIDTH // 2
        self.y = HEIGHT // 2

        self.size = 30 if name == "Bentley" else 40

        self.base_speed = stats["speed"]
        self.speed = stats["speed"]

        self.color = stats["color"]

        self.max_hp = stats["hp"]
        self.hp = stats["hp"]

        self.base_damage = stats["damage"]
        self.damage = stats["damage"]

        self.vel_x = 0
        self.vel_y = 0

        self.invuln = 0

        self.speed_boost_timer = 0
        self.fire_rate_timer = 0

        self.speed_upgrades = 0
        self.damage_upgrades = 0
        self.fire_upgrades = 0
        self.hp_upgrades = 0

        self.score_multiplier = 1
        # Each shop item tracks its own purchases, allowing its price to double.
        self.shop_purchases = [0] * 6

        # Ability
        self.ability_cooldown = 0
        self.ability_max_cooldown = (
            stats["ability_cd"] * FPS
        )

        self.ability_flash = 0

        # Special temporary damage multiplier
        self.damage_boost_timer = 0

        # Smooth motion trail. A short history keeps this cheap even at 120 FPS.
        self.trail = []
        self.trail_max = 18
        self.passive_shot_timer = 0

        self.passive_name, self.passive_desc = CHARACTER_PASSIVES.get(
            name, ("STANDARD", "A dependable fighter.")
        )
        self.passive_shot_count = 0
        self.passive_guard_cooldown = 0
        self.passive_chain_cooldown = 0
        self.passive_charge = 0
        self.passive_fire_streak = 0
        self.wave_banner_timer = 0
        self.wave_banner_wave = 1

        self.kill_feed = []

    def update_trail(self):
        """Store the player's centre after movement for a smooth fading trail."""
        cx = self.x + self.size * 0.5
        cy = self.y + self.size * 0.5

        if not self.trail:
            self.trail.append([cx, cy])
            return

        last_x, last_y = self.trail[-1]
        # Avoid filling the list with practically identical points when stationary.
        if (cx - last_x) ** 2 + (cy - last_y) ** 2 > 0.25:
            self.trail.append([cx, cy])

        if len(self.trail) > self.trail_max:
            del self.trail[:-self.trail_max]

    def draw_trail(self):
        """Draw a soft, fading chain of circles behind the player."""
        if len(self.trail) < 2:
            return

        trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        total = len(self.trail)

        for i, (x, y) in enumerate(self.trail[:-1]):
            progress = i / max(1, total - 1)
            alpha = int(10 + 75 * progress)
            radius = max(3, int(self.size * (0.16 + 0.22 * progress)))

            pygame.draw.circle(
                trail_surface,
                (*self.color, alpha),
                (int(x), int(y)),
                radius
            )

        screen.blit(trail_surface, (0, 0))


    def update_effects(self):

        if self.speed_boost_timer > 0:

            self.speed_boost_timer -= 1

            self.speed = (
                self.base_speed * 1.65
                + self.speed_upgrades * 0.35
            )

        else:

            self.speed = (
                self.base_speed
                + self.speed_upgrades * 0.35
            )

        if self.fire_rate_timer > 0:
            self.fire_rate_timer -= 1

        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1

        if self.ability_flash > 0:
            self.ability_flash -= 1

        if self.damage_boost_timer > 0:
            self.damage_boost_timer -= 1

        if self.passive_guard_cooldown > 0:
            self.passive_guard_cooldown -= 1

        if self.passive_chain_cooldown > 0:
            self.passive_chain_cooldown -= 1

        # Character passives that modify movement.
        if self.name == "Lachie" and (abs(self.vel_x) + abs(self.vel_y)) > 0.1:
            self.speed = max(self.speed, self.base_speed + 0.8 + self.speed_upgrades * 0.35)

        if self.name == "Bentley":
            self.speed = max(self.speed, self.base_speed + self.speed_upgrades * 0.4)

        if self.name == "Jett" and (abs(self.vel_x) + abs(self.vel_y)) > 0.1:
            self.speed = max(self.speed, self.base_speed + self.speed_upgrades * 0.35)


# ============================================================
# TEAR
# ============================================================

class TearEntity:

    def __init__(
        self,
        x,
        y,
        vx,
        vy,
        dist,
        radius,
        damage,
        passive=False
    ):

        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.life = dist

        self.radius = radius

        self.damage = damage
        # Passive Soggy Cat bullets travel through enemies, damaging each once.
        self.passive = passive
        self.hit_enemies = set()


# ============================================================
# ENEMY
# ============================================================

class EnemyEntity:

    def __init__(
        self,
        x,
        y,
        name,
        small=False,
        wave=1
    ):

        self.x = x
        self.y = y

        self.name = name
        self.small = small

        # ----------------------------------------------------
        # REAL ENEMY HP
        # ----------------------------------------------------

        if small:

            self.size = 15

            self.speed = (
                2.8 +
                min(wave * 0.025, 1.6)
            )

            self.max_hp = (
                3 +
                wave // 3
            )

        else:

            self.size = 30

            self.speed = (
                1.8 +
                min(wave * 0.035, 1.8)
            )

            base_hp = {
                "Lucas": 8,
                "Darcy": 12,
                "Mr Deng": 15,
                "chudson mcchud": 20,
                "Jethro": 10,
                "Lincoln": 13,
                "Jack": 25,
                "Lenny": 16,
                "straight teeth": 9,
                "Toby": 24,
                "Kirat": 12,
                "Mr Ginn": 18,
                "Bentley": 6,
                "Beau": 17,
                "Billy": 10,
                "Will": 13,
                "Wyatt": 15
            }.get(name, 10)

            # HP increases every wave
            self.max_hp = (
                base_hp +
                wave * 3
            )

        self.hp = self.max_hp

        self.ability_timer = random.randint(
            120,
            240
        )

        self.special_timer = random.randint(
            100,
            180
        )

        self.shield_timer = 0

        self.enraged = False

        self.dash_timer = random.randint(
            150,
            250
        )

        self.dash_active = 0

        self.dash_vx = 0
        self.dash_vy = 0

        self.is_boss = False
        self.is_mini_boss = False
        self.is_elite = False
        self.elite_flash = 0


# ============================================================
# BOSS
# ============================================================

class ChampionBoss(EnemyEntity):

    def __init__(self, wave):

        super().__init__(
            WIDTH // 2 - 35,
            -100,
            "Mr Champion",
            False,
            wave
        )

        self.size = 70

        # Much larger scaling than normal enemies
        self.max_hp = (
            500 +
            wave * 150
        )

        self.hp = self.max_hp

        self.speed = (
            1.6 +
            wave * 0.03
        )

        self.is_boss = True

        self.ability_timer = 120
        self.shoot_timer = 80
        self.spawn_timer = 300

        self.phase = 1
        self.phase_flash = 0


class MattMiniBoss(EnemyEntity):
    """An even-wave mini-boss that prioritises eating nearby bricks."""

    def __init__(self, wave):
        super().__init__(
            random.choice([45, WIDTH - 90]),
            random.randint(80, HEIGHT - 120),
            "Matt",
            False,
            wave
        )
        self.size = 42
        # Nerfed so Matt stays threatening without becoming an enormous
        # HP sponge on later waves.
        self.max_hp = 50 + wave * 12
        self.hp = self.max_hp
        self.speed = 1.8 + min(wave * 0.025, 0.8)
        self.heal_per_brick = max(8, int(self.max_hp * 0.12))
        self.is_mini_boss = True
        self.eating_flash = 0


class Brick:
    """A breakable arena object that Matt consumes for health."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 28
        self.max_hp = 25
        self.hp = self.max_hp


def spawn_matt_bricks():
    return [
        Brick(
            random.randint(55, WIDTH - 85),
            random.randint(100, HEIGHT - 85)
        )
        for _ in range(8)
    ]


# ============================================================
# ENEMY BULLET
# ============================================================

def award_kill(player, enemy):
    """Award reduced score so point progression takes longer."""
    base = 50 if enemy.is_boss else (15 if enemy.is_mini_boss else (3 if enemy.is_elite else 1))
    points = base * player.score_multiplier
    if enemy.is_boss:
        message = f"BOSS DEFEATED  +{points}"
    elif enemy.is_mini_boss:
        message = f"MATT DOWN  +{points}"
    elif enemy.is_elite:
        message = f"ELITE DOWN  +{points}"
    else:
        message = f"{enemy.name}  +{points}"
    add_kill_feed(player, message)
    return points


def add_kill_feed(player, message, ttl=150):
    """Add a temporary message to the player's kill feed."""
    if hasattr(player, "kill_feed"):
        player.kill_feed.append([message, ttl])
        player.kill_feed = player.kill_feed[-4:]


class EnemyBullet:

    def __init__(
        self,
        x,
        y,
        vx,
        vy,
        radius=7
    ):

        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.radius = radius

        self.life = 300


# ============================================================
# AREA EFFECT
# ============================================================

class AreaEffect:

    def __init__(
        self,
        x,
        y,
        radius,
        duration,
        color,
        damage=5
    ):

        self.x = x
        self.y = y

        self.radius = radius

        self.duration = duration

        self.color = color

        self.damage = damage


# ============================================================
# PICKUP
# ============================================================

class Pickup:

    def __init__(
        self,
        x,
        y,
        pickup_type
    ):

        self.x = x
        self.y = y

        self.type = pickup_type

        self.radius = 14

        self.life = FPS * 15

        self.bob = random.uniform(
            0,
            math.pi * 2
        )

    def update(self):

        self.life -= 1
        self.bob += 0.08

    def draw(self):

        offset = math.sin(
            self.bob
        ) * 3

        colour = (
            SPEED_GREEN
            if self.type == "speed"
            else FIRE_RED
        )

        pygame.draw.circle(
            screen,
            colour,
            (
                int(self.x),
                int(self.y + offset)
            ),
            self.radius
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (
                int(self.x),
                int(self.y + offset)
            ),
            self.radius,
            2
        )

        text = (
            "S"
            if self.type == "speed"
            else "F"
        )

        surf = font_small.render(
            text,
            True,
            BLACK
        )

        screen.blit(
            surf,
            (
                self.x -
                surf.get_width() // 2,
                self.y +
                offset -
                surf.get_height() // 2
            )
        )


# ============================================================
# ENEMY BULLET
# ============================================================

def create_enemy_bullet(
    bullets,
    x,
    y,
    target_x,
    target_y,
    speed=4,
    radius=7
):

    dx = target_x - x
    dy = target_y - y

    length = math.sqrt(
        dx * dx +
        dy * dy
    )

    if length == 0:
        return

    dx /= length
    dy /= length

    bullets.append(
        EnemyBullet(
            x,
            y,
            dx * speed,
            dy * speed,
            radius
        )
    )


# ============================================================
# DAMAGE ALL ENEMIES
# ============================================================

def damage_all_enemies(
    enemies,
    damage,
    player,
    pickups,
    wave
):

    kills = 0

    for e in enemies[:]:

        e.hp -= damage

        if e.hp <= 0:

            if e.is_boss:

                score_gain = award_kill(player, e)

                for _ in range(5):

                    pickups.append(
                        Pickup(
                            e.x + random.randint(-50, 50),
                            e.y + random.randint(-50, 50),
                            random.choice(
                                ["speed", "fire"]
                            )
                        )
                    )

            else:

                score_gain = award_kill(player, e)

                if random.random() < 0.08:

                    pickups.append(
                        Pickup(
                            e.x + e.size // 2,
                            e.y + e.size // 2,
                            random.choice(
                                ["speed", "fire"]
                            )
                        )
                    )

            spawn_burst(e.x + e.size // 2, e.y + e.size // 2,
                        (255, 120, 80), count=14, speed=3.0,
                        spread=360, size=3, life=22)

            enemies.remove(e)
            kills += score_gain

    return kills


# ============================================================
# PLAYER ABILITIES
# ============================================================

def use_ability(
    player,
    enemies,
    tears,
    enemy_bullets,
    area_effects,
    pickups,
    wave
):

    if player.ability_cooldown > 0:
        return 0

    player.ability_cooldown = (
        player.ability_max_cooldown
    )

    player.ability_flash = 20

    score_gain = 0

    cx = player.x + player.size // 2
    cy = player.y + player.size // 2


    # ========================================================
    # ETHAN - PANINI BARRAGE
    # ========================================================

    if player.name == "Ethan":

        for i in range(16):

            angle = (
                i *
                math.pi * 2 /
                16
            )

            tears.append(
                TearEntity(
                    cx,
                    cy,
                    math.cos(angle) * 14,
                    math.sin(angle) * 14,
                    80,
                    9,
                    player.damage * 3
                )
            )


    # ========================================================
    # MR BYRNE - BIG SLAM
    # ========================================================

    elif player.name == "Mr Byrne":

        area_effects.append(
            AreaEffect(
                cx,
                cy,
                180,
                25,
                PURPLE,
                20
            )
        )

        score_gain += damage_all_enemies(
            enemies,
            25,
            player,
            pickups,
            wave
        )


    # ========================================================
    # PASHMEET - RAGE
    # ========================================================

    elif player.name == "Pashmeet":

        player.damage_boost_timer = FPS * 8
        player.speed_boost_timer = FPS * 8
        player.fire_rate_timer = FPS * 8

        player.damage += 3


    # ========================================================
    # LUCAS - BURNING DASH
    # ========================================================

    elif player.name == "Lucas":

        player.speed_boost_timer = FPS * 5

        area_effects.append(
            AreaEffect(
                cx,
                cy,
                100,
                120,
                FIRE_RED,
                12
            )
        )


    # ========================================================
    # DARCY - ICE SHIELD
    # ========================================================

    elif player.name == "Darcy":

        player.invuln = FPS * 5

        area_effects.append(
            AreaEffect(
                cx,
                cy,
                90,
                FPS * 5,
                CYAN,
                0
            )
        )


    # ========================================================
    # MR DENG - DENG STORM
    # ========================================================

    elif player.name == "Mr Deng":

        for i in range(12):

            angle = (
                i *
                math.pi * 2 /
                12
            )

            tears.append(
                TearEntity(
                    cx,
                    cy,
                    math.cos(angle) * 10,
                    math.sin(angle) * 10,
                    100,
                    8,
                    player.damage * 2
                )
            )


    # ========================================================
    # CHUDSON - EXPLOSION
    # ========================================================

    elif player.name == "chudson mcchud":

        area_effects.append(
            AreaEffect(
                cx,
                cy,
                220,
                20,
                DARK_ORANGE,
                25
            )
        )

        score_gain += damage_all_enemies(
            enemies,
            20,
            player,
            pickups,
            wave
        )


    # ========================================================
    # JETHRO - BEAM
    # ========================================================

    elif player.name == "Jethro":

        for e in enemies[:]:

            if distance(
                cx,
                cy,
                e.x + e.size // 2,
                e.y + e.size // 2
            ) < 300:

                e.hp -= 60

                if e.hp <= 0:

                    enemies.remove(e)

                    score_gain += (
                        2 *
                        player.score_multiplier
                    )


    # ========================================================
    # LINCOLN - TELEPORT
    # ========================================================

    elif player.name == "Lincoln":

        angle = random.uniform(
            0,
            math.pi * 2
        )

        player.x = (
            cx +
            math.cos(angle) * 220
        )

        player.y = (
            cy +
            math.sin(angle) * 220
        )

        player.x = max(
            0,
            min(
                WIDTH - player.size,
                player.x
            )
        )

        player.y = max(
            0,
            min(
                HEIGHT - player.size,
                player.y
            )
        )

        player.invuln = FPS * 2


    # ========================================================
    # JACK - NUKE
    # ========================================================

    elif player.name == "Jack":

        area_effects.append(
            AreaEffect(
                cx,
                cy,
                300,
                30,
                GOLD,
                50
            )
        )

        score_gain += damage_all_enemies(
            enemies,
            50,
            player,
            pickups,
            wave
        )


    # ========================================================
    # LENNY - RUSH
    # ========================================================

    elif player.name == "Lenny":

        player.speed_boost_timer = FPS * 6

        for i in range(20):

            angle = (
                i *
                math.pi * 2 /
                20
            )

            tears.append(
                TearEntity(
                    cx,
                    cy,
                    math.cos(angle) * 12,
                    math.sin(angle) * 12,
                    100,
                    7,
                    player.damage * 2
                )
            )


    # ========================================================
    # STRAIGHT TEETH - PAIN FIELD
    # ========================================================

    elif player.name == "straight teeth":

        area_effects.append(
            AreaEffect(
                cx,
                cy,
                200,
                FPS * 5,
                PINK,
                12
            )
        )


    # ========================================================
    # TOBY - CHARGE
    # ========================================================

    elif player.name == "Toby":

        player.speed_boost_timer = FPS * 5

        area_effects.append(
            AreaEffect(
                cx,
                cy,
                120,
                30,
                ORANGE,
                30
            )
        )


    # ========================================================
    # KIRAT - MULTISHOT
    # ========================================================

    elif player.name == "Kirat":

        for i in range(32):

            angle = (
                i *
                math.pi * 2 /
                32
            )

            tears.append(
                TearEntity(
                    cx,
                    cy,
                    math.cos(angle) * 13,
                    math.sin(angle) * 13,
                    100,
                    6,
                    player.damage * 2
                )
            )


    # ========================================================
    # MR GINN - GINN ZONE
    # ========================================================

    elif player.name == "Mr Ginn":

        area_effects.append(
            AreaEffect(
                cx,
                cy,
                250,
                FPS * 5,
                DARK_BLUE,
                15
            )
        )


    # ========================================================
    # BENTLEY - TINY SPEED
    # ========================================================

    elif player.name == "Bentley":

        player.speed_boost_timer = FPS * 10
        player.fire_rate_timer = FPS * 10
        player.invuln = FPS * 3


    # ========================================================
    # BEAU - BLAST
    # ========================================================

    elif player.name == "Beau":

        for i in range(24):

            angle = (
                i *
                math.pi * 2 /
                24
            )

            tears.append(
                TearEntity(
                    cx,
                    cy,
                    math.cos(angle) * 11,
                    math.sin(angle) * 11,
                    120,
                    8,
                    player.damage * 3
                )
            )


    # ========================================================
    # BILLY - BLITZ
    # ========================================================

    elif player.name == "Billy":

        player.speed_boost_timer = FPS * 4
        player.fire_rate_timer = FPS * 4

        for i in range(12):

            angle = (
                i *
                math.pi * 2 /
                12
            )

            tears.append(
                TearEntity(
                    cx,
                    cy,
                    math.cos(angle) * 16,
                    math.sin(angle) * 16,
                    90,
                    6,
                    player.damage * 2
                )
            )


    # ========================================================
    # WILL - HEAL
    # ========================================================

    elif player.name == "Will":

        player.hp = min(
            player.max_hp,
            player.hp + player.max_hp // 2
        )

        player.invuln = FPS * 2


    # ========================================================
    # WYATT - STORM
    # ========================================================

    elif player.name == "Wyatt":

        for i in range(18):

            angle = (
                i *
                math.pi * 2 /
                18
            )

            tears.append(
                TearEntity(
                    cx,
                    cy,
                    math.cos(angle) * 12,
                    math.sin(angle) * 12,
                    110,
                    8,
                    player.damage * 2
                )
            )


    # ========================================================
    # AARON - BARRAGE
    # ========================================================

    elif player.name == "Aaron":

        # 3 rings of bullets
        for ring in range(3):

            for i in range(18):

                angle = (
                    i *
                    math.pi * 2 /
                    18
                ) + ring * 0.15

                tears.append(
                    TearEntity(
                        cx,
                        cy,
                        math.cos(angle) * (11 + ring * 2),
                        math.sin(angle) * (11 + ring * 2),
                        120,
                        8,
                        player.damage * 3
                    )
                )


    # ========================================================
    # JETT - OVERDRIVE
    # ========================================================

    elif player.name == "Jett":

        player.speed_boost_timer = FPS * 8
        player.fire_rate_timer = FPS * 8
        player.invuln = FPS * 2

        for i in range(24):

            angle = (
                i *
                math.pi * 2 /
                24
            )

            tears.append(
                TearEntity(
                    cx,
                    cy,
                    math.cos(angle) * 18,
                    math.sin(angle) * 18,
                    100,
                    7,
                    player.damage * 3
                )
            )


    # ========================================================
    # LACHIE - TURBO
    # ========================================================

    elif player.name == "Lachie":
        # Lachie becomes extremely fast and fires a rapid ring of shots.
        player.speed_boost_timer = FPS * 7
        player.fire_rate_timer = FPS * 7

        for i in range(20):
            angle = i * math.pi * 2 / 20
            tears.append(
                TearEntity(
                    cx, cy,
                    math.cos(angle) * 16,
                    math.sin(angle) * 16,
                    110, 7,
                    player.damage * 2
                )
            )

    # ========================================================
    # JAKUB - METEOR
    # ========================================================

    elif player.name == "Jakub":
        # Jakub drops a huge damaging zone around himself.
        area_effects.append(
            AreaEffect(
                cx,
                cy,
                260,
                35,
                YELLOW,
                35
            )
        )
        score_gain += damage_all_enemies(
            enemies,
            35,
            player,
            pickups,
            wave
        )

    # ========================================================
    # BEN - PHANTOM
    # ========================================================

    elif player.name == "Ben":
        # Ben vanishes briefly, becomes invulnerable, then unleashes a burst.
        player.invuln = FPS * 5
        player.speed_boost_timer = FPS * 5

        for i in range(16):
            angle = i * math.pi * 2 / 16
            tears.append(
                TearEntity(
                    cx, cy,
                    math.cos(angle) * 20,
                    math.sin(angle) * 20,
                    100, 8,
                    player.damage * 3
                )
            )

    # ========================================================
    # MONIKA - DELETE EVERYTHING
    # ========================================================

    elif player.name == "Monika":

        # Monika gets an absurd screen-wide attack.
        for e in enemies[:]:

            if e.is_boss:

                e.hp -= 1000

                if e.hp <= 0:

                    enemies.remove(e)

                    score_gain += (
                        250 *
                        player.score_multiplier
                    )

                    for _ in range(8):

                        pickups.append(
                            Pickup(
                                e.x + random.randint(-60, 60),
                                e.y + random.randint(-60, 60),
                                random.choice(
                                    ["speed", "fire"]
                                )
                            )
                        )

            else:

                e.hp -= 999999

                if e.hp <= 0:

                    enemies.remove(e)

                    score_gain += (
                        5 *
                        player.score_multiplier
                    )

        # Also become temporarily invincible.
        player.invuln = FPS * 5

        player.speed_boost_timer = FPS * 10
        player.fire_rate_timer = FPS * 10

    # ========================================================
    # BRIANNA - BARRAGE
    # ========================================================

    elif player.name == "Brianna":
        player.speed_boost_timer = FPS * 5

        for i in range(18):
            angle = i * math.pi * 2 / 18
            tears.append(
                TearEntity(
                    cx,
                    cy,
                    math.cos(angle) * 15,
                    math.sin(angle) * 15,
                    105,
                    8,
                    player.damage * 2
                )
            )

    # ========================================================
    # KODY - CYCLONE
    # ========================================================

    elif player.name == "Kody":
        # Kody whips up a cyclone of shots and briefly shields up.
        player.invuln = FPS * 2
        player.speed_boost_timer = FPS * 4

        for i in range(24):
            angle = i * math.pi * 2 / 24
            tears.append(
                TearEntity(
                    cx, cy,
                    math.cos(angle) * 15,
                    math.sin(angle) * 15,
                    110, 7,
                    player.damage * 2
                )
            )

    # Soggy Cat sprays a watery barrage in every direction.
    elif player.name == "Soggy Cat":
        for i in range(18):
            angle = i * math.pi * 2 / 18 + random.uniform(-0.12, 0.12)
            tears.append(
                TearEntity(
                    cx, cy,
                    math.cos(angle) * 15,
                    math.sin(angle) * 15,
                    95, 8,
                    player.damage * 2,
                    passive=True
                )
            )

    # Custom fighters get a balanced radial burst instead of having no ability.
    elif player.name.startswith("Custom Fighter"):
        for i in range(12):
            angle = i * math.pi * 2 / 12
            tears.append(
                TearEntity(
                    cx, cy,
                    math.cos(angle) * 13,
                    math.sin(angle) * 13,
                    90, 7,
                    player.damage * 2
                )
            )
        player.invuln = FPS * 1

    return score_gain


# ============================================================
# THEME MENU
# ============================================================

def theme_menu():
    names = list(THEMES.keys())
    selected = names.index(CURRENT_THEME)
    age = 0

    while True:
        tick_fade()
        draw_gradient_background()
        text_center("THEME SELECT", font_title, WHITE, 70)
        text_center("Choose the look of Cardijn Battlegrounds", font_small, MUTED, 132)

        panel_rect = draw_fade_enter(age, pygame.Rect(WIDTH // 2 - 210, 175, 420, 330))
        panel(panel_rect, PANEL, BORDER, 16, 1)

        for i, name in enumerate(names):
            rect = pygame.Rect(WIDTH // 2 - 175, panel_rect.y + 20 + i * 46, 350, 38)
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            active = i == selected or hovered
            burst_on_hover(rect, THEMES[name]["ACCENT"])
            colour = BLACK if active else WHITE
            fill = THEMES[name]["ACCENT"] if active else PANEL_2
            if active:
                draw_rect_glow(rect, THEMES[name]["ACCENT"], radius=9, alpha=34, spread=9)
            pygame.draw.rect(screen, fill, rect, border_radius=9)
            if not active:
                pygame.draw.rect(screen, BORDER, rect, 1, border_radius=9)
            label = font_ui.render(name, True, colour)
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

        text_center("ENTER / CLICK  •  ESC TO GO BACK", font_tiny, MUTED, 525)
        update_fx()
        draw_fx()

        if exit_ok:
            reset_exit_ok()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and fade_mode == "idle":
                for i, name in enumerate(names):
                    rect = pygame.Rect(WIDTH // 2 - 175, panel_rect.y + 20 + i * 46, 350, 38)
                    if rect.collidepoint(event.pos):
                        selected = i
                        apply_theme(name)
            if fade_mode == "idle" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(names)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(names)
                elif event.key == pygame.K_RETURN:
                    apply_theme(names[selected])
                elif event.key == pygame.K_ESCAPE:
                    request_menu_exit()
            elif fade_mode != "idle" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    request_menu_exit()

        draw_fade_overlay()
        draw_custom_cursor()
        pygame.display.flip()
        clock.tick(FPS)
        age += 1


# ============================================================
# CREDITS
# ============================================================

def credits_menu():
    """Show the people responsible for this totally serious game."""
    age = 0
    while True:
        tick_fade()
        draw_gradient_background()

        text_center("CREDITS", font_title, WHITE, 70)
        text_center("because im not a bad person", font_small, MUTED, 125)

        credit_rect = draw_fade_enter(age, pygame.Rect(WIDTH // 2 - 260, 145, 520, 405))
        panel(credit_rect, PANEL, BORDER, 16, 1)

        text_center("CARDIJN BATTLEGROUNDS", font_big, ACCENT, 190)
        text_center("Created by @snakepoledancing on discord", font_ui, WHITE, 260)
        text_center("Fur:Trash for the amazing music.", font_small, LIGHT_GRAY, 325)
        text_center("The fizcord discord server for promoting and ideas.", font_small, LIGHT_GRAY, 349)
        text_center("@troll_the_world on discord for making the wiki", font_small, LIGHT_GRAY, 373)
        text_center("And my friends for making this possible! <3", font_small, LIGHT_GRAY, 397)
        text_center("Thanks for playing!", font_ui, ACCENT, 445)
        text_center("ESC: back", font_tiny, MUTED, 505)
        update_fx()
        draw_fx()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if fade_mode == "idle":
                    request_menu_exit()

        if exit_ok:
            reset_exit_ok()
            return

        draw_fade_overlay()
        draw_custom_cursor()
        pygame.display.flip()
        clock.tick(FPS)
        age += 1


# ============================================================
# CHANGELOG
# ============================================================

CHANGELOG_ENTRIES = [
    ("Fixed music"),
    ("Added particles"),
    ("Updated UI again"),
]

def changelog_menu():
    selected = 0
    scroll = 0
    visible_count = 10
    age = 0

    while True:
        tick_fade()
        draw_gradient_background()
        text_center("CHANGELOG", font_title, WHITE, 28)
        text_center(f"CARDIJN BATTLEGROUNDS {GAME_VERSION}", font_small, MUTED, 82)

        card = draw_fade_enter(age, pygame.Rect(55, 110, 690, 428))
        panel(card, PANEL, BORDER, 18, 1)

        start = max(0, min(scroll, max(0, len(CHANGELOG_ENTRIES) - visible_count)))
        visible = CHANGELOG_ENTRIES[start:start + visible_count]

        y = 140
        for i, item in enumerate(visible):
            active = (start + i) == selected
            row = pygame.Rect(75, y, 650, 34)
            hovered = row.collidepoint(pygame.mouse.get_pos())
            if hovered and not active:
                burst_on_hover(row, ACCENT)
                active = True

            if active:
                draw_rect_glow(row, ACCENT, radius=8, alpha=30, spread=8)
                pygame.draw.rect(screen, PANEL_2, row, border_radius=8)
                pygame.draw.rect(screen, ACCENT, row, 1, border_radius=8)

            # Support both the newer one-item changelog format
            # and the older (version, entry) format.
            if isinstance(item, (tuple, list)):
                if len(item) >= 2:
                    version, entry = item[0], item[1]
                else:
                    version, entry = GAME_VERSION, item[0]
            else:
                version, entry = GAME_VERSION, item

            badge(version, row.x + 8, row.y + 5, ACCENT if active else BORDER)
            draw_text_shadow(
                entry,
                font_small,
                WHITE if active else LIGHT_GRAY,
                row.x + 88,
                row.y + 8,
                offset=(1, 1),
                alpha=100
            )
            y += 37

        if start > 0:
            text_center("▲ MORE", font_tiny, MUTED, 120)
        if start + visible_count < len(CHANGELOG_ENTRIES):
            text_center("▼ MORE", font_tiny, MUTED, 524)

        text_center("UP/DOWN: SCROLL   •   ENTER/ESC: BACK", font_tiny, MUTED, 565)
        update_fx()
        draw_fx()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if fade_mode == "idle":
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                        request_menu_exit()
                    elif event.key == pygame.K_UP:
                        selected = max(0, selected - 1)
                        if selected < scroll:
                            scroll = selected
                    elif event.key == pygame.K_DOWN:
                        selected = min(len(CHANGELOG_ENTRIES) - 1, selected + 1)
                        if selected >= scroll + visible_count:
                            scroll = selected - visible_count + 1

                elif event.key == pygame.K_ESCAPE:
                    request_menu_exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if card.collidepoint(event.pos):
                    y_check = 140
                    for i in range(len(visible)):
                        row = pygame.Rect(75, y_check, 650, 34)
                        if row.collidepoint(event.pos):
                            selected = start + i
                            break
                        y_check += 37

        if exit_ok:
            reset_exit_ok()
            return
        draw_fade_overlay()
        draw_custom_cursor()
        pygame.display.flip()
        clock.tick(FPS)
        age += 1


# ============================================================
# MAIN MENU
# ============================================================

def main_menu():
    play_music("menu")
    selected = 0
    options = ["PLAY", "CREATE CHARACTER", "THEMES", "CHANGELOG", "CREDITS", "MUSIC VOLUME", "QUIT"]
    age = 0
    selected_y = 322.0

    while True:
        tick_fade()
        draw_gradient_background()

        # Brand / title with a gentle breathing glow
        title_pulse = int(16 + 9 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.004)))
        glow_circle((WIDTH // 2, 72), 44, ACCENT, title_pulse)
        pygame.draw.circle(screen, PANEL_2, (WIDTH // 2, 72), 36)
        pygame.draw.circle(screen, ACCENT, (WIDTH // 2, 72), 36, 2)
        text_center("CB", font_big, WHITE, 50)
        text_center(GAME_VERSION, font_tiny, MUTED, 112)

        text_center("CARDIJN", font_title, WHITE, 132)
        text_center("BATTLEGROUNDS", font_title, ACCENT, 206)

        # Music credits
        music_x = WIDTH - 100
        music_y = 30

        text_center("MUSIC", font_enemy, ACCENT, music_y, music_x)

        menu_music_text = font_tiny.render(
            "Menu Music: parasite - Fur:Trash",
            True,
            LIGHT_GRAY
        )
        game_music_text = font_tiny.render(
            "Game Music: DOGPIT - Fur:Trash",
            True,
            LIGHT_GRAY
        )

        screen.blit(
            menu_music_text,
            (music_x - menu_music_text.get_width() // 2, music_y + 28)
        )

        screen.blit(
            game_music_text,
            (music_x - game_music_text.get_width() // 2, music_y + 48)
        )

        # Main menu — sized so the card never runs off the bottom of the
        # 800x600 window, with even margins around its options.
        menu_rect = draw_fade_enter(age, pygame.Rect(WIDTH // 2 - 185, 268, 370, 300))
        panel(menu_rect, PANEL, BORDER, 18, 1)
        section_label("MAIN MENU", menu_rect.x + 24, menu_rect.y + 15)

        # Smoothly glide the selection highlight between options.
        target_y = menu_rect.y + 40 + selected * 36
        selected_y = lerp(selected_y, target_y, 0.38)
        if abs(selected_y - target_y) < 0.4:
            selected_y = target_y
        highlight = pygame.Rect(menu_rect.x + 14, int(selected_y) - 2, menu_rect.w - 28, 34)
        draw_rect_glow(highlight, ACCENT, radius=10, alpha=30, spread=8)
        draw_alpha_rect(highlight, ACCENT, radius=10, alpha=40)

        for i, option in enumerate(options):
            rect = pygame.Rect(menu_rect.x + 24, menu_rect.y + 40 + i * 36, menu_rect.w - 48, 30)
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            active = i == selected or hovered
            label = f"MUSIC VOLUME   {round(music_volume * 100)}%" if option == "MUSIC VOLUME" else option
            button(rect, label, active)

        if selected == 5:
            bar_rect = pygame.Rect(menu_rect.x + 65, menu_rect.bottom - 14, menu_rect.w - 130, 5)
            bar(bar_rect, music_volume, 1.0, ACCENT, back=GRAY)

        controls = "WASD MOVE   •   ARROWS SHOOT   •   E ABILITY   •   P PAUSE"
        text_center(controls, font_tiny, MUTED, 579)
        update_fx()
        draw_fx()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if fade_mode == "idle" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_LEFT and selected == 5:
                    set_music_volume(music_volume - 0.05)
                elif event.key == pygame.K_RIGHT and selected == 5:
                    set_music_volume(music_volume + 0.05)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        fade_out_blocking()
                        return
                    elif selected == 1:
                        run_transition(create_character_menu)
                    elif selected == 2:
                        run_transition(theme_menu)
                    elif selected == 3:
                        run_transition(changelog_menu)
                    elif selected == 4:
                        run_transition(credits_menu)
                    elif selected == 5:
                        # Volume is controlled directly with LEFT/RIGHT.
                        pass
                    else:
                        fade_out_blocking()
                        pygame.quit()
                        sys.exit()

            if fade_mode == "idle" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in range(len(options)):
                    rect = pygame.Rect(menu_rect.x + 24, menu_rect.y + 40 + i * 36, menu_rect.w - 48, 30)
                    if rect.collidepoint(event.pos):
                        selected = i
                        if i == 0:
                            fade_out_blocking()
                            return
                        elif i == 1:
                            run_transition(create_character_menu)
                        elif i == 2:
                            run_transition(theme_menu)
                        elif i == 3:
                            run_transition(changelog_menu)
                        elif i == 4:
                            run_transition(credits_menu)
                        elif i == 5:
                            # Clicking the volume option selects it;
                            # LEFT/RIGHT changes the volume.
                            pass
                        else:
                            fade_out_blocking()
                            pygame.quit()
                            sys.exit()

        draw_developer_credit()
        draw_fade_overlay()
        draw_custom_cursor()
        pygame.display.flip()
        clock.tick(FPS)
        age += 1


# ============================================================
# CUSTOM CHARACTER CREATOR
# ============================================================

CUSTOM_COLORS = [
    (0, 220, 255), (255, 70, 90), (180, 0, 220), (255, 180, 40),
    (100, 255, 80), (255, 80, 190), (80, 140, 255), (255, 255, 255)
]

def create_character_menu():
    """Create a character without needing to edit the source code."""
    name = ""
    color_index = 0
    hp = 100
    speed = 4.0
    tear_speed = 12
    fire_rate = 16
    attack_range = 70
    damage = 7
    bullet_size = 7

    fields = ["NAME", "HP", "SPEED", "TEAR SPEED", "FIRE RATE", "RANGE", "DAMAGE", "BULLET SIZE", "COLOR", "CREATE"]
    selected = 0
    age = 0

    while True:
        tick_fade()
        draw_gradient_background()

        text_center("CHARACTER CREATOR", font_title, WHITE, 22)
        text_center(
            "Build your own fighter. LEFT/RIGHT changes the selected stat.",
            font_small, MUTED, 80
        )

        # Preview
        preview = draw_fade_enter(age, pygame.Rect(25, 125, 280, 390))
        panel(preview, PANEL, BORDER, 16, 1)
        preview_color = CUSTOM_COLORS[color_index]

        glow_circle((165, 220), 52, preview_color, 38)
        pygame.draw.circle(screen, PANEL_2, (165, 220), 45)
        pygame.draw.rect(
            screen, preview_color, (140, 195, 50, 50), border_radius=12
        )
        pygame.draw.rect(
            screen, WHITE, (140, 195, 50, 50), 2, border_radius=12
        )
        text_center(name, font_ui, preview_color, 285, 165)
        text_center("CUSTOM", font_small, MUTED, 320, 165)

        # Editor
        editor = draw_fade_enter(age, pygame.Rect(320, 125, 460, 390))
        panel(editor, PANEL, BORDER, 16, 1)

        values = [
            name if name else "Unnamed Fighter",
            f"{hp}",
            f"{speed:.1f}",
            f"{tear_speed}",
            f"{fire_rate}",
            f"{attack_range}",
            f"{damage}",
            f"{bullet_size}",
            f"{color_index + 1}/{len(CUSTOM_COLORS)}"
        ]

        # Stat limits are enforced directly below when values change.

        y = 145
        for i, field in enumerate(fields[:-1]):
            active = i == selected
            rect = pygame.Rect(335, y, 430, 38)
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            burst_on_hover(rect, preview_color if not active else ACCENT)

            if active:
                pygame.draw.rect(screen, ACCENT, rect, border_radius=9)
                label_color = BLACK
                value_color = BLACK
            else:
                pygame.draw.rect(screen, PANEL_2, rect, border_radius=9)
                pygame.draw.rect(screen, BORDER, rect, 1, border_radius=9)
                label_color = WHITE
                value_color = LIGHT_GRAY

            label = font_small.render(field, True, label_color)
            value = font_ui.render(values[i], True, value_color)
            screen.blit(label, (rect.x + 12, rect.centery - label.get_height() // 2))
            screen.blit(value, (rect.right - value.get_width() - 12,
                                 rect.centery - value.get_height() // 2))
            y += 34

        # Create button
        create_rect = pygame.Rect(335, 455, 430, 38)
        active = selected == len(fields) - 1
        burst_on_hover(create_rect, GREEN)
        pygame.draw.rect(
            screen, GREEN if active else PANEL_2,
            create_rect, border_radius=9
        )
        if not active:
            pygame.draw.rect(screen, BORDER, create_rect, 1, border_radius=9)
        create_text = font_ui.render("CREATE CHARACTER", True, BLACK if active else WHITE)
        screen.blit(create_text, (
            create_rect.centerx - create_text.get_width() // 2,
            create_rect.centery - create_text.get_height() // 2
        ))

        text_center(
            "NAME: TYPE • UP/DOWN SELECT • LEFT/RIGHT CHANGE • ENTER CREATE • ESC BACK",
            font_tiny, MUTED, 555
        )
        update_fx()
        draw_fx()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    request_menu_exit()
                    continue

                if fade_mode != "idle":
                    continue

                if selected == 0:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_SPACE and len(name) < 24:
                        name += " "
                    elif event.unicode and event.unicode.isprintable() and len(name) < 24:
                        name += event.unicode
                    # Name editing consumes the key so it doesn't also change fields.
                    if event.key not in (pygame.K_UP, pygame.K_DOWN):
                        continue

                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(fields)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(fields)

                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    direction = 1 if event.key == pygame.K_RIGHT else -1

                    if selected == 1:
                        hp = max(25, min(500, hp + direction * 25))
                    elif selected == 2:
                        speed = max(1.0, min(8.0, round(speed + direction * 0.5, 1)))
                    elif selected == 3:
                        tear_speed = max(4, min(30, tear_speed + direction))
                    elif selected == 4:
                        fire_rate = max(4, min(30, fire_rate + direction))
                    elif selected == 5:
                        attack_range = max(20, min(250, attack_range + direction * 10))
                    elif selected == 6:
                        damage = max(1, min(30, damage + direction))
                    elif selected == 7:
                        bullet_size = max(2, min(30, bullet_size + direction))
                    elif selected == 8:
                        color_index = (color_index + direction) % len(CUSTOM_COLORS)

                elif event.key == pygame.K_RETURN and selected == 0:
                    # Enter while editing the name simply keeps the current name.
                    name = name.strip() or "Custom Fighter"

                elif event.key == pygame.K_RETURN and selected == len(fields) - 1:
                    # Ensure unique name in case the creator is opened repeatedly.
                    base_name = name.strip() or "Custom Fighter"
                    custom_name = base_name
                    number = 2
                    while custom_name in CHARACTERS:
                        custom_name = f"{base_name} {number}"
                        number += 1

                    CHARACTERS[custom_name] = {
                        "hp": hp,
                        "speed": speed,
                        "t_speed": tear_speed,
                        "rate": fire_rate,
                        "range": attack_range,
                        "damage": damage,
                        "bullet_size": bullet_size,
                        "color": CUSTOM_COLORS[color_index],
                        "desc": "A fighter you built yourself.",
                        "ability": "Custom Burst",
                        "ability_desc": "A balanced burst of shots all around you.",
                        "ability_cd": 8
                    }
                    spawn_burst(create_rect.centerx, create_rect.centery, GREEN,
                                count=26, speed=3.4, spread=360, size=3, life=30)
                    request_menu_exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and fade_mode == "idle":
                # Clicking a field selects it; clicking CREATE confirms it.
                y_check = 145
                for i in range(len(fields) - 1):
                    rect = pygame.Rect(335, y_check, 430, 30)
                    if rect.collidepoint(event.pos):
                        selected = i
                        break
                    y_check += 34

                if create_rect.collidepoint(event.pos):
                    base_name = name.strip() or "Custom Fighter"
                    custom_name = base_name
                    number = 2
                    while custom_name in CHARACTERS:
                        custom_name = f"{base_name} {number}"
                        number += 1

                    CHARACTERS[custom_name] = {
                        "hp": hp,
                        "speed": speed,
                        "t_speed": tear_speed,
                        "rate": fire_rate,
                        "range": attack_range,
                        "damage": damage,
                        "bullet_size": bullet_size,
                        "color": CUSTOM_COLORS[color_index],
                        "desc": "A fighter you built yourself.",
                        "ability": "Custom Burst",
                        "ability_desc": "A balanced burst of shots all around you.",
                        "ability_cd": 8
                    }
                    spawn_burst(create_rect.centerx, create_rect.centery, GREEN,
                                count=26, speed=3.4, spread=360, size=3, life=30)
                    request_menu_exit()

        if exit_ok:
            reset_exit_ok()
            return
        draw_fade_overlay()
        draw_custom_cursor()
        pygame.display.flip()
        clock.tick(FPS)
        age += 1


# ============================================================
# CHARACTER MENU
# ============================================================

def run_monika_unlock_puzzle():
    """Return True when the Monika unlock answer is correct."""
    # Two layers: binary nibbles -> hexadecimal ASCII -> the unlock phrase.
    encoded_message = (
        "0100 0010 0101 0101 0101 0100 0010 0000 "
        "0101 0111 0100 1000 0101 1001"
    )
    answer = "BUT WHY"
    typed_answer = ""
    feedback = ""

    while True:
        tick_fade()
        draw_gradient_background()
        tick = pygame.time.get_ticks()
        pulse = int(120 + 110 * (0.5 + 0.5 * math.sin(tick / 150)))
        glitch = 3 if (tick // 90) % 9 == 0 else 0

        # An unstable, red system overlay makes this feel like a forbidden menu.
        threat = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        threat.fill((75, 0, 10, 42))
        for y in range(0, HEIGHT, 5):
            pygame.draw.line(threat, (255, 20, 45, 16), (0, y), (WIDTH, y), 1)
        screen.blit(threat, (0, 0))
        pygame.draw.rect(screen, (105, 0, 18), (24, 24, WIDTH - 48, HEIGHT - 48), 3)
        pygame.draw.rect(screen, (255, 35, 65), (32, 32, WIDTH - 64, HEIGHT - 64), 1)

        text_center("ACCESS DENIED", font_title, (255, 35, 65), 42)
        text_center("MONIKA'S LOCK", font_big, (255, pulse, pulse), 104)

        puzzle_box = pygame.Rect(WIDTH // 2 - 325, 172, 650, 300)
        panel(puzzle_box, (18, 5, 12), (255, 25, 60), 4, 2)
        for corner_x, corner_y in ((puzzle_box.x, puzzle_box.y),
                                   (puzzle_box.right, puzzle_box.y),
                                   (puzzle_box.x, puzzle_box.bottom),
                                   (puzzle_box.right, puzzle_box.bottom)):
            pygame.draw.circle(screen, (255, pulse, pulse), (corner_x, corner_y), 5)
        text_center("/// ENCRYPTED PAYLOAD ///", font_tiny, (255, 110, 130), 194)
        encoded_font = pygame.font.SysFont("consolas", 16, bold=True)
        encoded_groups = encoded_message.split()
        # A byte is two displayed nibbles.  Keep those pairs together before wrapping.
        binary_bytes = [" ".join(encoded_groups[i:i + 2])
                        for i in range(0, len(encoded_groups), 2)]
        # Keep a long first row while allowing shorter decoded phrases.
        binary_rows = [binary_bytes[:6], binary_bytes[6:]]
        for row_number, groups in enumerate(binary_rows):
            row = encoded_font.render(" ".join(groups), True, (255, 75, 100))
            offset = glitch if row_number % 2 == 0 else -glitch
            screen.blit(row, row.get_rect(center=(WIDTH // 2 + offset, 238 + row_number * 28)))
        text_center("BINARY  >  HEXADECIMAL  >  ASCII", font_tiny, (255, 155, 165), 310)

        input_rect = pygame.Rect(WIDTH // 2 - 215, 337, 430, 52)
        pygame.draw.rect(screen, BLACK, input_rect, border_radius=10)
        pygame.draw.rect(screen, RED if feedback else (255, pulse, pulse), input_rect, 2,
                         border_radius=10)
        entry = font_ui.render(typed_answer or "TYPE THE DECODED MESSAGE", True,
                               WHITE if typed_answer else MUTED)
        screen.blit(entry, entry.get_rect(center=input_rect.center))

        if feedback:
            text_center(feedback, font_small, RED, 407)
        else:
            text_center("this is KINDA hard", font_small,
                        (255, 95, 115), 407)
        text_center("ENTER: submit  •  ESC: retreat", font_tiny, LIGHT_GRAY, 437)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and fade_mode == "idle":
                if event.key == pygame.K_ESCAPE:
                    request_menu_exit()
                if event.key == pygame.K_BACKSPACE:
                    typed_answer = typed_answer[:-1]
                    feedback = ""
                elif event.key == pygame.K_RETURN:
                    if typed_answer.strip().upper() == answer:
                        return True
                    feedback = "That isn't the message. Try decoding it again."
                elif event.unicode and event.unicode.isprintable() and len(typed_answer) < 24:
                    typed_answer += event.unicode.upper()
                    feedback = ""

        if exit_ok:
            reset_exit_ok()
            return False

        draw_fade_overlay()
        draw_custom_cursor()
        pygame.display.flip()
        clock.tick(FPS)

def run_character_menu():
    global monika_unlocked, soggy_cat_unlocked, kempson_unlocked
    names = list(CHARACTERS.keys())
    selected_index = 0

    while True:
        tick_fade()
        draw_gradient_background()

        text_center("CHOOSE YOUR CHARACTER", font_title, WHITE, 22)

        selected = names[selected_index]
        data = CHARACTERS[selected]
        locked = (selected == "Monika" and not monika_unlocked) or (selected == "Kempson" and not kempson_unlocked)

        start_i = max(0, min(selected_index - 4, len(names) - 9))
        end_i = min(len(names), start_i + 9)
        visible = names[start_i:end_i]

        # Character list
        list_rect = pygame.Rect(20, 115, 300, 450)
        panel(list_rect)

        y = 130
        for i, name in enumerate(visible):
            actual_index = start_i + i
            rect = pygame.Rect(32, y, 276, 38)
            active = actual_index == selected_index
            is_locked = ((name == "Monika" and not monika_unlocked) or
                         (name == "Kempson" and not kempson_unlocked))
            colour = MUTED if is_locked else CHARACTERS[name]["color"]
            burst_on_hover(rect, colour)

            if active:
                pygame.draw.rect(screen, colour, rect, border_radius=9)
                text_color = BLACK
                pygame.draw.circle(screen, WHITE, (rect.x + 14, rect.centery), 4)
            else:
                pygame.draw.rect(screen, PANEL_2, rect, border_radius=9)
                pygame.draw.rect(screen, (48, 58, 82), rect, 1, border_radius=9)
                text_color = WHITE

            label = "LOCKED: " + name if is_locked else name
            surf = font_enemy.render(label, True, text_color)
            screen.blit(surf, (rect.x + 26, rect.centery - surf.get_height() // 2))
            y += 44

        # Detail panel
        detail = pygame.Rect(340, 115, 440, 450)
        panel(detail, PANEL, BORDER, 16, 1)

        colour = MUTED if locked else data["color"]
        cx, cy = 560, 165
        glow_circle((cx, cy), 48, colour, 34)
        pygame.draw.circle(screen, PANEL_2, (cx, cy), 42)
        pygame.draw.circle(screen, colour, (cx, cy), 42, 3)
        preview_sprite = load_soggy_cat_image() if selected == "Soggy Cat" else None
        if preview_sprite:
            screen.blit(preview_sprite, preview_sprite.get_rect(center=(cx, cy)))
        else:
            pygame.draw.rect(screen, colour, (cx - 15, cy - 15, 30, 30), border_radius=7)

        text_center("LOCKED" if locked else selected, font_big, colour, 210, 560)
        # Only Monika uses the puzzle prompt. Other characters never show
        if locked and selected == "Monika":
            detail_text = "Solve the tile puzzle to unlock Monika."
        else:
            detail_text = data["desc"].strip() or "No description."
        text_center(detail_text, font_small, LIGHT_GRAY, 274, 560)

        # Stat bars
        stats = [
            ("HP", data["hp"], 1000, RED),
            ("SPEED", data["speed"], 7, ACCENT),
            ("TEAR SPEED", data["t_speed"], 30, TEAR_BLUE),
            ("FIRE RATE", max(1, 30 - data["rate"]), 30, GOLD),
            ("RANGE", data["range"], 250, ACCENT_2),
            ("DAMAGE", data["damage"], 25, FIRE_RED),
        ]

        if locked:
            if selected == "Monika":
                text_center("Press ENTER to attempt the puzzle", font_ui, PINK, 372, 560)
            else:
                text_center("LOCKED", font_ui, MUTED, 372, 560)
        else:
            sy = 296
            for label, value, maximum, stat_colour in stats:
                label_s = font_tiny.render(label, True, MUTED)
                value_s = font_tiny.render(str(value), True, WHITE)
                screen.blit(label_s, (365, sy))
                screen.blit(value_s, (742 - value_s.get_width(), sy))
                bar((365, sy + 16, 365, 7), value, maximum, stat_colour)
                sy += 27

            # Keep the ability and passive sections inside the detail panel.
            # The passive description is wrapped so longer descriptions never
            # run through the panel edge or get clipped.
            badge("ABILITY", 365, 460, colour)
            ability = font_small.render(data["ability"], True, WHITE)
            screen.blit(ability, (445, 464))

            # Show what the ability does on the line below its name.
            ability_desc = data.get("ability_desc", "No description.")
            max_abil_width = detail.right - 365 - 18
            if font_tiny.size(ability_desc)[0] > max_abil_width:
                while ability_desc and font_tiny.size(ability_desc + "...")[0] > max_abil_width:
                    ability_desc = ability_desc[:-1]
                ability_desc += "..."
            abil_s = font_tiny.render(ability_desc, True, MUTED)
            screen.blit(abil_s, (365, 488))

            passive_name, passive_desc = CHARACTER_PASSIVES.get(
                selected, ("STANDARD", "A dependable fighter.")
            )
            badge("PASSIVE", 365, 509, colour)
            passive = font_tiny.render(passive_name, True, WHITE)
            screen.blit(passive, (445, 513))

            # Wrap the description to the available panel width.
            max_passive_width = detail.right - 365 - 18
            words = passive_desc.split()
            lines = []
            line = ""
            for word in words:
                test = word if not line else line + " " + word
                if font_tiny.size(test)[0] <= max_passive_width:
                    line = test
                else:
                    if line:
                        lines.append(line)
                    line = word
            if line:
                lines.append(line)
            for line_index, line_text in enumerate(lines[:2]):
                desc_s = font_tiny.render(line_text, True, MUTED)
                screen.blit(desc_s, (365, 534 + line_index * 15))

        controls = ("↑ ↓ SELECT     ENTER PUZZLE / PLAY     ESC MAIN MENU"
                    if selected == "Monika" and locked else
                    "↑ ↓ SELECT     ENTER PLAY     ESC MAIN MENU")
        text_center(controls, font_tiny, MUTED, 585)
        update_fx()
        draw_fx()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if fade_mode == "idle" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    request_menu_exit()
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(names)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(names)
                elif event.key == pygame.K_RETURN:
                    if locked:
                        if selected != "Monika":
                            continue
                        unlock_result = run_monika_unlock_puzzle()
                        monika_unlocked = bool(unlock_result)
                    else:
                        fade_out_blocking()
                        return selected

            if fade_mode == "idle" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                y_check = 130
                for i, name in enumerate(visible):
                    rect = pygame.Rect(32, y_check, 276, 38)
                    if rect.collidepoint(event.pos):
                        selected_index = start_i + i
                    y_check += 44

        if exit_ok:
            reset_exit_ok()
            return None

        draw_fade_overlay()
        draw_custom_cursor()
        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# SHOP
# ============================================================

SHOP_BASE_COST = 25


def shop_cost(player, item_index):
    """Return the next price for one shop item: 25, 50, 100, 200..."""
    return SHOP_BASE_COST * (2 ** player.shop_purchases[item_index])


def draw_kempson():

    cx = 620
    cy = 105

    pygame.draw.rect(
        screen,
        (80, 80, 90),
        (
            cx - 35,
            cy + 25,
            70,
            65
        )
    )

    pygame.draw.circle(
        screen,
        (230, 190, 150),
        (
            cx,
            cy
        ),
        32
    )

    pygame.draw.arc(
        screen,
        BLACK,
        (
            cx - 32,
            cy - 32,
            64,
            50
        ),
        math.pi,
        math.pi * 2,
        6
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (
            cx - 11,
            cy - 3
        ),
        3
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (
            cx + 11,
            cy - 3
        ),
        3
    )

    pygame.draw.polygon(
        screen,
        RED,
        [
            (cx, cy + 25),
            (cx - 9, cy + 65),
            (cx + 9, cy + 65)
        ]
    )

    name = font_ui.render(
        "MR KEMPSON",
        True,
        GOLD
    )

    screen.blit(
        name,
        (
            cx -
            name.get_width() // 2,
            cy + 98
        )
    )


def shop_menu(player, score):

    selected = 0

    items = [
        "Max HP +25",
        "Speed +0.35",
        "Tear Damage +1",
        "Fire Rate +1",
        "Heal 50% HP",
        "Score Multiplier +1"
    ]

    while True:

        draw_gradient_background()
        panel(pygame.Rect(24, 20, 752, 536), PANEL, BORDER, 18, 1)

        title = font_title.render(
            "MR KEMPSON'S SHOP",
            True,
            WHITE
        )

        screen.blit(
            title,
            (
                WIDTH // 2 -
                title.get_width() // 2,
                20
            )
        )

        points = font_ui.render(
            f"POINTS: {score}",
            True,
            YELLOW
        )

        screen.blit(
            points,
            (
                WIDTH // 2 -
                points.get_width() // 2,
                100
            )
        )

        draw_kempson()

        start_y = 175

        for i, item in enumerate(items):

            rect = pygame.Rect(
                50,
                start_y + i * 52,
                450,
                42
            )

            if i == selected:

                pygame.draw.rect(
                    screen,
                    SHOP_BLUE,
                    rect
                )

                colour = BLACK

            else:

                hovered = rect.collidepoint(pygame.mouse.get_pos())
                if hovered:
                    burst_on_hover(rect, SHOP_BLUE)
                    pygame.draw.rect(
                        screen,
                        SHOP_BLUE,
                        rect,
                        2
                    )
                else:
                    pygame.draw.rect(
                        screen,
                        GRAY,
                        rect,
                        2
                    )

                colour = WHITE

            text = font_ui.render(
                f"{i + 1}. {item}",
                True,
                colour
            )

            screen.blit(
                text,
                (
                    rect.x + 12,
                    rect.y + 6
                )
            )

            cost = font_ui.render(
                str(shop_cost(player, i)),
                True,
                GOLD
            )

            screen.blit(
                cost,
                (
                    rect.right -
                    cost.get_width() -
                    10,
                    rect.y + 6
                )
            )

        stats_x = 530
        stats_y = 260

        stat_title = font_ui.render(
            "UPGRADES",
            True,
            GREEN
        )

        screen.blit(
            stat_title,
            (
                stats_x,
                stats_y
            )
        )

        current_stats = [
            f"Max HP: {player.max_hp}",
            f"Speed: {player.speed:.2f}",
            f"Tear Damage: {player.damage}",
            f"Fire Upgrade: {player.fire_upgrades}",
            f"Score Multiplier: x{player.score_multiplier}"
        ]

        sy = stats_y + 45

        for stat in current_stats:

            surf = font_small.render(
                stat,
                True,
                WHITE
            )

            screen.blit(
                surf,
                (
                    stats_x,
                    sy
                )
            )

            sy += 25

        descriptions = [
            "Increase your maximum health.",
            "Permanently become faster.",
            "Every tear deals more damage.",
            "Shoot tears more frequently.",
            "Restore half of your maximum HP.",
            "Earn more points from kills."
        ]

        desc = font_small.render(
            descriptions[selected],
            True,
            LIGHT_GRAY
        )

        screen.blit(
            desc,
            (
                530,
                470
            )
        )

        controls = font_small.render(
            "UP/DOWN: Select | ENTER: Buy | ESC: Back",
            True,
            LIGHT_GRAY
        )

        screen.blit(
            controls,
            (
                WIDTH // 2 -
                controls.get_width() // 2,
                HEIGHT - 30
            )
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return score

                if event.key == pygame.K_UP:

                    selected -= 1

                    if selected < 0:
                        selected = len(items) - 1

                elif event.key == pygame.K_DOWN:

                    selected += 1

                    if selected >= len(items):
                        selected = 0

                elif event.key == pygame.K_RETURN:

                    current_cost = shop_cost(player, selected)
                    if score >= current_cost:

                        if selected == 0:

                            player.max_hp += 25
                            player.hp += 25
                            player.hp = min(
                                player.hp,
                                player.max_hp
                            )
                            player.hp_upgrades += 1

                        elif selected == 1:

                            player.speed_upgrades += 1

                        elif selected == 2:

                            player.damage += 1
                            player.damage_upgrades += 1

                        elif selected == 3:

                            player.fire_upgrades += 1

                        elif selected == 4:

                            player.hp = min(
                                player.max_hp,
                                player.hp +
                                player.max_hp // 2
                            )

                        elif selected == 5:

                            player.score_multiplier += 1

                        score -= current_cost
                        player.shop_purchases[selected] += 1
                        buy_rect = pygame.Rect(50, start_y + selected * 52, 450, 42)
                        spawn_burst(buy_rect.centerx, buy_rect.centery, GOLD,
                                    count=22, speed=3.2, spread=360, size=3, life=26)

        update_fx()
        draw_fx()
        draw_custom_cursor()
        pygame.display.flip()

        clock.tick(FPS)


# ============================================================
# PAUSE
# ============================================================

def pause_menu(player, score):

    selected = 0

    options = [
        "Resume",
        "Shop",
        "Music Volume",
        "Return to Main Menu"
    ]

    while True:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 190)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        pause_card = pygame.Rect(WIDTH // 2 - 205, 35, 410, 525)
        panel(pause_card, PANEL, BORDER, 20, 1)
        text_center("PAUSED", font_title, YELLOW, 48)
        text_center(f"{score:,} POINTS", font_ui, GOLD, 125)
        section_label("GAME MENU", pause_card.x + 35, 165)

        for i, option in enumerate(options):

            rect = pygame.Rect(
                WIDTH // 2 - 165,
                195 + i * 64,
                330,
                44
            )
            label = f"MUSIC VOLUME   {round(music_volume * 100)}%" if option == "Music Volume" else option.upper()
            button(rect, label, i == selected, SHOP_BLUE)

            if option == "Music Volume":
                bar_rect = pygame.Rect(WIDTH // 2 - 120, rect.bottom + 6, 240, 5)
                bar(bar_rect, music_volume, 1.0, ACCENT, back=GRAY)

        instructions = font_small.render(
            "UP/DOWN: Select | LEFT/RIGHT: Volume | ENTER: Confirm | P: Resume",
            True,
            LIGHT_GRAY
        )

        screen.blit(
            instructions,
            (
                WIDTH // 2 -
                instructions.get_width() // 2,
                HEIGHT - 28
            )
        )

        update_fx()
        draw_fx()
        draw_custom_cursor()
        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key in (
                    pygame.K_p,
                    pygame.K_ESCAPE
                ):
                    return score

                if event.key == pygame.K_UP:
                    selected -= 1
                    if selected < 0:
                        selected = len(options) - 1

                elif event.key == pygame.K_DOWN:
                    selected += 1
                    if selected >= len(options):
                        selected = 0

                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    if selected == 2:
                        direction = 0.05 if event.key == pygame.K_RIGHT else -0.05
                        set_music_volume(music_volume + direction)

                elif event.key == pygame.K_RETURN:

                    if selected == 0:
                        return score

                    elif selected == 1:
                        score = shop_menu(
                            player,
                            score
                        )

                    elif selected == 2:
                        set_music_volume(music_volume)

                    elif selected == 3:
                        return None

        clock.tick(FPS)


# ============================================================
# ENEMY SPAWN LIMIT
# ============================================================

MAX_ACTIVE_ENEMIES = 5

def can_spawn_enemy(enemies):
    """Keep the total number of active enemies capped at five."""
    return len(enemies) < MAX_ACTIVE_ENEMIES



def spawn_enemy(enemies, wave):

    if not can_spawn_enemy(enemies):
        return

    side = random.choice(
        [
            "top",
            "bottom",
            "left",
            "right"
        ]
    )

    if side == "top":

        x = random.randint(
            0,
            WIDTH - 1
        )

        y = -50

    elif side == "bottom":

        x = random.randint(
            0,
            WIDTH - 1
        )

        y = HEIGHT + 50

    elif side == "left":

        x = -50

        y = random.randint(
            0,
            HEIGHT - 1
        )

    else:

        x = WIDTH + 50

        y = random.randint(
            0,
            HEIGHT - 1
        )

    available = ENEMY_NAMES[:]

    if wave < 3:

        available = [
            "Lucas",
            "Darcy",
            "Jethro",
            "Jack",
            "Toby"
        ]

    elif wave < 6:

        available = [
            "Lucas",
            "Darcy",
            "Mr Deng",
            "Jethro",
            "Lincoln",
            "Jack",
            "Lenny",
            "Toby"
        ]

    name = random.choice(
        available
    )

    enemy = EnemyEntity(
        x, y, name, False, wave
    )

    elite_chance = 0.10 if wave >= 3 else 0.0
    if random.random() < elite_chance:
        enemy.is_elite = True
        enemy.size = 38
        enemy.max_hp = int(enemy.max_hp * 2.0)
        enemy.hp = enemy.max_hp
        enemy.speed *= 1.22

    enemies.append(enemy)


# ============================================================
# START GAME
# ============================================================

def start_game():

    while True:

        chosen = run_character_menu()

        if chosen is not None:
            break

        # Escaping the character select returns to the title screen.
        main_menu()

    # Switch away from the menu track only once actual combat begins.
    play_music("ingame")

    cfg = CHARACTERS[
        chosen
    ]

    player = PlayerEntity(
        chosen,
        cfg
    )

    # Bullet size is now a character stat. Existing characters keep their
    # original projectile sizes, while custom characters can choose theirs.
    tear_radius = cfg.get("bullet_size", 7)

    if chosen == "Mr Byrne":
        tear_radius = cfg.get("bullet_size", 12)

    if chosen == "Monika":
        tear_radius = cfg.get("bullet_size", 10)

    tears = []
    enemies = []
    enemy_bullets = []
    area_effects = []
    pickups = []
    bricks = []

    score = 0

    wave = 1

    wave_timer = 0

    wave_duration = FPS * 20

    spawn_timer = 0
    tear_timer = 0

    game_over = False

    boss_spawned_this_wave = False
    matt_spawned_this_wave = False

    return (
        chosen,
        cfg,
        player,
        tear_radius,
        tears,
        enemies,
        enemy_bullets,
        area_effects,
        pickups,
        bricks,
        score,
        wave,
        wave_timer,
        wave_duration,
        spawn_timer,
        tear_timer,
        game_over,
        boss_spawned_this_wave,
        matt_spawned_this_wave
    )



# ============================================================
# BETWEEN-WAVE UPGRADE SYSTEM
# ============================================================

UPGRADE_POOL = [
    ("POWER SHOT", "+20% damage", "damage"),
    ("QUICK FEET", "+0.5 movement speed", "speed"),
    ("RAPID FIRE", "Fire 2 frames faster", "fire"),
    ("REINFORCED", "+20 max HP and heal", "hp"),
    ("SCORE BOOST", "+1 score multiplier", "score"),
    ("FULL REPAIR", "Restore 35% of max HP", "heal"),
]


def apply_wave_upgrade(player, kind):
    if kind == "damage":
        bonus = max(1, int(round(player.base_damage * (0.22 if player.name == "Beau" else 0.20))))
        player.damage += bonus
        player.damage_upgrades += 1
    elif kind == "speed":
        player.speed_upgrades += 1
        if player.name == "Beau":
            player.base_speed += 0.05
    elif kind == "fire":
        player.fire_upgrades += 1
    elif kind == "hp":
        player.max_hp += 20
        player.hp = min(player.max_hp, player.hp + 20)
        player.hp_upgrades += 1
    elif kind == "score":
        player.score_multiplier += 1
    elif kind == "heal":
        player.hp = min(player.max_hp, player.hp + max(1, int(player.max_hp * 0.35)))


def choose_wave_upgrade(player, wave):
    choices = random.sample(UPGRADE_POOL, 3)
    selected = 0

    while True:
        draw_gradient_background()

        # Darkened arena-style overlay.
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((4, 5, 14, 190))
        screen.blit(overlay, (0, 0))

        tick = pygame.time.get_ticks()
        pulse = 0.5 + 0.5 * math.sin(tick / 180)

        title = font_title.render("WAVE COMPLETE", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 68)))
        sub = font_small.render(
            f"WAVE {wave} CLEARED  •  CHOOSE YOUR UPGRADE",
            True, GOLD
        )
        screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 116)))

        card_w, card_h = 225, 265
        gap = 18
        total = card_w * 3 + gap * 2
        start_x = WIDTH // 2 - total // 2

        for i, (name, desc, kind) in enumerate(choices):
            rect = pygame.Rect(start_x + i * (card_w + gap), 160, card_w, card_h)
            active = i == selected
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            if hovered:
                burst_on_hover(rect, GOLD)
                active = True

            border = GOLD if active else BORDER
            fill = PANEL_2 if active else PANEL
            panel(rect, fill, border, 16, 2 if active else 1)

            if active:
                glow_rect = pygame.Rect(rect.x - 3, rect.y - 3, rect.w + 6, rect.h + 6)
                pygame.draw.rect(screen, (*GOLD, int(30 + 35 * pulse)), glow_rect, 3, border_radius=18)

            number = font_ui.render(str(i + 1), True, GOLD if active else MUTED)
            screen.blit(number, (rect.x + 14, rect.y + 12))

            icon_map = {
                "damage": "DMG",
                "speed": "SPD",
                "fire": "FIRE",
                "hp": "HP",
                "score": "x",
                "heal": "+"
            }
            icon = font_big.render(icon_map[kind], True, GOLD)
            screen.blit(icon, icon.get_rect(center=(rect.centerx, rect.y + 75)))

            name_s = font_ui.render(name, True, WHITE)
            screen.blit(name_s, name_s.get_rect(center=(rect.centerx, rect.y + 135)))

            # Wrap the short description.
            words = desc.split()
            lines, line = [], ""
            for word in words:
                test = (line + " " + word).strip()
                if font_tiny.size(test)[0] <= rect.w - 28:
                    line = test
                else:
                    if line:
                        lines.append(line)
                    line = word
            if line:
                lines.append(line)

            yy = rect.y + 180
            for line in lines[:3]:
                s = font_tiny.render(line, True, LIGHT_GRAY)
                screen.blit(s, s.get_rect(center=(rect.centerx, yy)))
                yy += 18

            if active:
                choose = font_tiny.render("ENTER TO SELECT", True, GREEN)
                screen.blit(choose, choose.get_rect(center=(rect.centerx, rect.bottom - 22)))

        controls = font_tiny.render("1 / 2 / 3 SELECT   •   ENTER CONFIRM", True, MUTED)
        screen.blit(controls, controls.get_rect(center=(WIDTH // 2, 455)))

        # Current build summary.
        build = font_tiny.render(
            f"DMG {player.damage}   HP {player.hp}/{player.max_hp}   "
            f"SPD +{player.speed_upgrades}   FIRE +{player.fire_upgrades}",
            True, LIGHT_GRAY
        )
        screen.blit(build, build.get_rect(center=(WIDTH // 2, 490)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_1):
                    selected = 0 if event.key == pygame.K_1 else (selected - 1) % 3
                elif event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_3):
                    selected = 2 if event.key == pygame.K_3 else (selected + 1) % 3
                elif event.key == pygame.K_2:
                    selected = 1
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    apply_wave_upgrade(player, choices[selected][2])
                    player.wave_banner_timer = FPS * 2
                    player.wave_banner_wave = wave
                    return

        update_fx()
        draw_fx()
        draw_custom_cursor()
        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# MAIN GAME
# ============================================================

def game_loop():

    (
        chosen,
        cfg,
        player,
        tear_radius,
        tears,
        enemies,
        enemy_bullets,
        area_effects,
        pickups,
        bricks,
        score,
        wave,
        wave_timer,
        wave_duration,
        spawn_timer,
        tear_timer,
        game_over,
        boss_spawned_this_wave,
        matt_spawned_this_wave
    ) = start_game()

    while True:

        tick_fade()

        # ====================================================
        # EVENTS
        # ====================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # ------------------------------------------------
                # ABILITY
                # ------------------------------------------------

                if (
                    event.key == pygame.K_e
                    and not game_over
                ):

                    score += use_ability(
                        player,
                        enemies,
                        tears,
                        enemy_bullets,
                        area_effects,
                        pickups,
                        wave
                    )

                # ------------------------------------------------
                # PAUSE
                # ------------------------------------------------

                if (
                    event.key == pygame.K_p
                    and not game_over
                ):
                    play_music("menu")
                    pause_result = pause_menu(
                        player,
                        score
                    )

                    if pause_result is None:
                        # Leave the current run and return to the title screen.
                        main_menu()

                        (
                            chosen,
                            cfg,
                            player,
                            tear_radius,
                            tears,
                            enemies,
                            enemy_bullets,
                            area_effects,
                            pickups,
                            bricks,
                                                score,
                            wave,
                            wave_timer,
                            wave_duration,
                            spawn_timer,
                            tear_timer,
                            game_over,
                            boss_spawned_this_wave,
                            matt_spawned_this_wave
                        ) = start_game()
                    else:
                        score = pause_result
                        play_music("ingame")

                # ------------------------------------------------
                # GAME OVER
                # ------------------------------------------------

                if game_over:

                    if event.key == pygame.K_r:

                        (
                            chosen,
                            cfg,
                            player,
                            tear_radius,
                            tears,
                            enemies,
                            enemy_bullets,
                            area_effects,
                            pickups,
                            bricks,
                                                score,
                            wave,
                            wave_timer,
                            wave_duration,
                            spawn_timer,
                            tear_timer,
                            game_over,
                            boss_spawned_this_wave,
                            matt_spawned_this_wave
                        ) = start_game()

        # ========================================================
        # GAME UPDATE
        # ========================================================

        if not game_over:

            keys = pygame.key.get_pressed()

            player.update_effects()


            # ====================================================
            # MOVEMENT
            # ====================================================

            dx = 0
            dy = 0

            if keys[pygame.K_w]:
                dy -= 1

            if keys[pygame.K_s]:
                dy += 1

            if keys[pygame.K_a]:
                dx -= 1

            if keys[pygame.K_d]:
                dx += 1

            if dx != 0 and dy != 0:

                length = math.sqrt(
                    dx * dx +
                    dy * dy
                )

                dx /= length
                dy /= length

            player.vel_x = (
                dx *
                player.speed
            )

            player.vel_y = (
                dy *
                player.speed
            )

            player.x += player.vel_x
            player.y += player.vel_y

            player.x = max(
                0,
                min(
                    player.x,
                    WIDTH - player.size
                )
            )

            player.y = max(
                0,
                min(
                    player.y,
                    HEIGHT - player.size
                )
            )

            player.update_trail()

            # ====================================================
            # WAVE SYSTEM
            # ====================================================

            wave_timer += 1

            # BOSS EVERY 5 WAVES
            if (
                wave % 5 == 0
                and not boss_spawned_this_wave
                and can_spawn_enemy(enemies)
            ):

                enemies.append(
                    ChampionBoss(wave)
                )

                boss_spawned_this_wave = True

            # Matt arrives on even waves, but NEVER alongside Mr Champion.
            # The five-enemy cap also applies to Matt.
            if (
                wave % 2 == 0
                and not matt_spawned_this_wave
                and not boss_spawned_this_wave
                and not any(e.is_boss for e in enemies)
                and can_spawn_enemy(enemies)
            ):
                enemies.append(MattMiniBoss(wave))
                bricks = spawn_matt_bricks()
                matt_spawned_this_wave = True


            if wave_timer >= wave_duration:

                wave += 1

                wave_timer = 0

                spawn_timer = 0

                boss_spawned_this_wave = False
                matt_spawned_this_wave = False
                bricks = []

                if len(enemies) > 35:
                    # Never trim an active boss while cleaning up normal enemies.
                    priority_enemies = [e for e in enemies if e.is_boss or e.is_mini_boss]
                    normal_enemies = [e for e in enemies if not e.is_boss and not e.is_mini_boss]
                    enemies = priority_enemies + normal_enemies[-max(0, 35 - len(priority_enemies)):]

                # Pause between waves and let the player choose one of three upgrades.
                choose_wave_upgrade(player, wave)


            # ====================================================
            # SHOOTING
            # ====================================================

            sdx = 0
            sdy = 0

            if keys[pygame.K_UP]:
                sdy = -1

            elif keys[pygame.K_DOWN]:
                sdy = 1

            elif keys[pygame.K_LEFT]:
                sdx = -1

            elif keys[pygame.K_RIGHT]:
                sdx = 1

            if tear_timer > 0:
                tear_timer -= 1

            if player.name == "Brianna" and not (keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
                player.passive_fire_streak = max(0, player.passive_fire_streak - 1)

            actual_rate = max(
                2 if player.name == "Monika" else 3,
                cfg["rate"] -
                player.fire_upgrades
            )

            if player.name in ("Billy", "Jett") and (abs(player.vel_x) + abs(player.vel_y)) > 0.1:
                actual_rate = max(2, int(actual_rate * 0.75))

            if player.name == "Bentley":
                actual_rate = max(2, int(actual_rate * 0.8))

            if player.fire_rate_timer > 0:

                actual_rate = max(
                    2,
                    int(
                        actual_rate *
                        0.35
                    )
                )

            if (
                (sdx != 0 or sdy != 0)
                and tear_timer <= 0
            ):

                sx = (
                    player.x +
                    player.size // 2
                )

                sy = (
                    player.y +
                    player.size // 2
                )

                vx = (
                    sdx *
                    cfg["t_speed"]
                )

                vy = (
                    sdy *
                    cfg["t_speed"]
                )

                mom = (
                    0.5
                    if player.name == "Ethan"
                    else 0.3
                )

                vx += (
                    player.vel_x *
                    mom
                )

                vy += (
                    player.vel_y *
                    mom
                )

                player.passive_shot_count += 1

                tear_damage = player.damage

                if player.damage_boost_timer > 0:
                    tear_damage *= 3

                if player.name == "Pashmeet":
                    tear_damage *= 1 + max(0, 1 - player.hp / max(1, player.max_hp)) * 1.6
                elif player.name == "Lucas" and (abs(player.vel_x) + abs(player.vel_y)) > 0.1:
                    tear_damage *= 1.15
                elif player.name == "Jethro" and (abs(player.vel_x) + abs(player.vel_y)) < 0.05:
                    tear_damage *= 1.6
                elif player.name == "Lenny" and enemies:
                    nearest = min(
                        enemies,
                        key=lambda e: distance(sx, sy, e.x + e.size // 2, e.y + e.size // 2)
                    )
                    if distance(sx, sy, nearest.x + nearest.size // 2, nearest.y + nearest.size // 2) < 180:
                        tear_damage *= 1.4
                elif player.name == "Jack" and enemies:
                    nearest = min(
                        enemies,
                        key=lambda e: distance(sx, sy, e.x + e.size // 2, e.y + e.size // 2)
                    )
                    if distance(sx, sy, nearest.x + nearest.size // 2, nearest.y + nearest.size // 2) < 130:
                        tear_damage *= 1.35
                elif player.name == "straight teeth":
                    tear_damage *= 1.35
                elif player.name == "Toby" and (abs(player.vel_x) + abs(player.vel_y)) > 0.1:
                    tear_damage *= 1.25
                elif player.name == "Brianna":
                    tear_damage *= 1 + min(player.passive_fire_streak, 10) * 0.04
                    player.passive_fire_streak = min(10, player.passive_fire_streak + 1)

                piercing = player.name == "Monika"

                tears.append(
                    TearEntity(
                        sx,
                        sy,
                        vx,
                        vy,
                        cfg["range"],
                        tear_radius,
                        tear_damage,
                        passive=piercing
                    )
                )

                # Muzzle VFX: a bright flash at the barrel plus a cone of
                # sparks streaming out along the shot direction.
                muzzle_angle = math.degrees(math.atan2(vy, vx))
                spawn_burst(sx, sy, player.color,
                            count=9, speed=2.8, angle=muzzle_angle,
                            spread=50, size=2.5, life=16)
                spawn_burst(sx, sy, WHITE,
                            count=4, speed=3.4, angle=muzzle_angle,
                            spread=14, size=2, life=10)
                g_flashes.append({
                    "x": sx, "y": sy,
                    "radius": tear_radius + 5,
                    "life": 5, "max_life": 5,
                    "colour": player.color,
                    "alpha": 170,
                })

                # Kirat fires side shots every fourth shot.
                if player.name == "Kirat" and player.passive_shot_count % 4 == 0:
                    for side in (-1, 1):
                        tears.append(
                            TearEntity(
                                sx, sy,
                                vx * 0.85 + (-vy * 0.22 * side),
                                vy * 0.85 + (vx * 0.22 * side),
                                cfg["range"] * 0.85,
                                max(4, tear_radius - 1),
                                tear_damage * 0.7
                            )
                        )

                # Mr Deng occasionally doubles a shot.
                if player.name == "Mr Deng" and player.passive_shot_count % 5 == 0:
                    tears.append(
                        TearEntity(sx, sy, vx, vy, cfg["range"], tear_radius, tear_damage * 0.8)
                    )

                if player.name == "Wyatt" and enemies and random.random() < 0.18:
                    target = min(
                        enemies,
                        key=lambda e: distance(sx, sy, e.x + e.size // 2, e.y + e.size // 2)
                    )
                    dx2 = target.x + target.size // 2 - sx
                    dy2 = target.y + target.size // 2 - sy
                    d2 = math.hypot(dx2, dy2)
                    if d2:
                        tears.append(TearEntity(sx, sy, dx2 / d2 * cfg["t_speed"], dy2 / d2 * cfg["t_speed"], cfg["range"] * 0.7, max(4, tear_radius - 1), tear_damage * 0.55))

                if player.name == "Jakub" and player.passive_shot_count % 8 == 0 and enemies:
                    target = min(
                        enemies,
                        key=lambda e: distance(sx, sy, e.x + e.size // 2, e.y + e.size // 2)
                    )
                    area_effects.append(AreaEffect(target.x + target.size // 2, target.y + target.size // 2, 55, 1, GOLD, 28))

                if player.name != "Brianna":
                    player.passive_fire_streak = min(player.passive_fire_streak + 1, 10)

                tear_timer = actual_rate

            # Soggy Cat fires automatically at the nearest enemy.  These
            # watery bullets pierce targets and only damage each target once.
            if player.name == "Soggy Cat":
                if player.passive_shot_timer > 0:
                    player.passive_shot_timer -= 1
                elif enemies:
                    sx = player.x + player.size // 2
                    sy = player.y + player.size // 2
                    target = min(
                        enemies,
                        key=lambda enemy: (enemy.x + enemy.size // 2 - sx) ** 2
                        + (enemy.y + enemy.size // 2 - sy) ** 2
                    )
                    dx = target.x + target.size // 2 - sx
                    dy = target.y + target.size // 2 - sy
                    length = math.hypot(dx, dy)
                    if length:
                        tears.append(
                            TearEntity(
                                sx, sy,
                                dx / length * cfg["t_speed"],
                                dy / length * cfg["t_speed"],
                                cfg["range"], tear_radius,
                                player.damage, passive=True
                            )
                        )
                    player.passive_shot_timer = 30


            # ====================================================
            # UPDATE TEARS
            # ====================================================

            for t in tears[:]:

                t.x += t.vx
                t.y += t.vy

                t.life -= 1

                # Faint sparkle trail behind every tear.
                if random.random() < 0.45:
                    spawn_burst(t.x, t.y, TEAR_BLUE if not t.passive else (105, 185, 255),
                                count=1, speed=0.6, spread=360, size=1.5, life=10)

                if (
                    t.life <= 0
                    or t.x < -30
                    or t.x > WIDTH + 30
                    or t.y < -30
                    or t.y > HEIGHT + 30
                ):

                    if t in tears:
                        tears.remove(t)

            # Bricks are solid targets: a tear breaks one instead of continuing through it.
            for t in tears[:]:
                tear_rect = pygame.Rect(
                    t.x - t.radius, t.y - t.radius,
                    t.radius * 2, t.radius * 2
                )
                for brick in bricks[:]:
                    brick_rect = pygame.Rect(brick.x, brick.y, brick.size, brick.size)
                    if tear_rect.colliderect(brick_rect):
                        if t in tears:
                            spawn_burst(t.x, t.y, ORANGE,
                                        count=8, speed=2.2, spread=360,
                                        size=2, life=14, gravity=0.05)
                        brick.hp -= t.damage
                        if brick.hp <= 0:
                            bricks.remove(brick)
                        if t in tears:
                            tears.remove(t)
                        break


            # ====================================================
            # ENEMY SPAWNING
            # ====================================================

            spawn_timer += 0.5

            spawn_limit = max(
                8,
                45 -
                wave * 1.8
            )

            if wave % 5 == 0:
                spawn_limit += 8
            if spawn_timer >= spawn_limit:

                spawn_timer = 0

                spawn_enemy(
                    enemies,
                    wave
                )


            # ====================================================
            # TARGET
            # ====================================================

            target_x = (
                player.x +
                player.size // 2
            )

            target_y = (
                player.y +
                player.size // 2
            )


            # ====================================================
            # ENEMY AI
            # ====================================================

            for e in enemies[:]:

                if e.is_boss:
                    e.speed = 1.6 + wave * 0.03
                elif e.is_mini_boss:
                    e.speed = 1.8 + min(wave * 0.025, 0.8)
                else:
                    base_speed = 2.8 + min(wave * 0.025, 1.6) if e.small else 1.8 + min(wave * 0.035, 1.8)
                    if e.is_elite:
                        base_speed *= 1.22
                    e.speed = base_speed

                if e.is_mini_boss:
                    # Matt ignores the player whenever a brick is available to eat.
                    if bricks:
                        target_brick = min(
                            bricks,
                            key=lambda brick: distance(
                                e.x + e.size / 2, e.y + e.size / 2,
                                brick.x + brick.size / 2, brick.y + brick.size / 2
                            )
                        )
                        matt_target_x = target_brick.x + target_brick.size / 2
                        matt_target_y = target_brick.y + target_brick.size / 2
                    else:
                        target_brick = None
                        matt_target_x, matt_target_y = target_x, target_y

                    dx_m = matt_target_x - (e.x + e.size / 2)
                    dy_m = matt_target_y - (e.y + e.size / 2)
                    dist_m = math.hypot(dx_m, dy_m)
                    if target_brick is not None and dist_m < e.size / 2 + target_brick.size / 2 + 4:
                        bricks.remove(target_brick)
                        e.hp = min(e.max_hp, e.hp + e.heal_per_brick)
                        e.eating_flash = 20
                    elif dist_m > 0:
                        e.x += dx_m / dist_m * e.speed
                        e.y += dy_m / dist_m * e.speed

                    e.x = max(0, min(WIDTH - e.size, e.x))
                    e.y = max(75, min(HEIGHT - e.size, e.y))
                    if e.eating_flash > 0:
                        e.eating_flash -= 1
                    continue

                if e.is_boss:

                    hp_ratio = e.hp / max(1, e.max_hp)
                    new_phase = 3 if hp_ratio <= 0.33 else (2 if hp_ratio <= 0.66 else 1)
                    if new_phase != e.phase:
                        e.phase = new_phase
                        e.phase_flash = 45
                        add_kill_feed(player, f"MR CHAMPION PHASE {new_phase}!")
                    if e.phase_flash > 0:
                        e.phase_flash -= 1

                    dx_b = (
                        target_x -
                        (
                            e.x +
                            e.size // 2
                        )
                    )

                    dy_b = (
                        target_y -
                        (
                            e.y +
                            e.size // 2
                        )
                    )

                    dist_b = math.sqrt(
                        dx_b * dx_b +
                        dy_b * dy_b
                    )

                    if dist_b > 180:

                        if dist_b != 0:

                            e.x += (
                                dx_b /
                                dist_b
                            ) * e.speed

                            e.y += (
                                dy_b /
                                dist_b
                            ) * e.speed

                    else:

                        angle = math.atan2(
                            dy_b,
                            dx_b
                        )

                        e.x -= (
                            math.sin(angle) *
                            1.2
                        )

                        e.y += (
                            math.cos(angle) *
                            1.2
                        )

                    e.shoot_timer -= 1

                    if e.shoot_timer <= 0:

                        bx = (
                            e.x +
                            e.size // 2
                        )

                        by = (
                            e.y +
                            e.size // 2
                        )

                        base_angle = math.atan2(
                            target_y - by,
                            target_x - bx
                        )

                        spread = 0.7 if e.phase == 1 else (0.85 if e.phase == 2 else 1.0)
                        offsets = [-spread, -spread / 2, 0, spread / 2, spread]
                        if e.phase == 3:
                            offsets += [-0.25, 0.25]
                        for offset in offsets:

                            angle = (
                                base_angle +
                                offset
                            )

                            enemy_bullets.append(
                                EnemyBullet(
                                    bx,
                                    by,
                                    math.cos(angle) * 5,
                                    math.sin(angle) * 5,
                                    9
                                )
                            )

                        e.shoot_timer = 70 if e.phase == 1 else (52 if e.phase == 2 else 38)

                    e.spawn_timer -= 1

                    if e.spawn_timer <= 0:

                        spawn_count = 3 if e.phase < 3 else 4
                        for _ in range(spawn_count):
                            if not can_spawn_enemy(enemies):
                                break

                            angle = random.uniform(
                                0,
                                math.pi * 2
                            )

                            enemies.append(
                                EnemyEntity(
                                    e.x +
                                    math.cos(angle) * 90,
                                    e.y +
                                    math.sin(angle) * 90,
                                    random.choice(
                                        [
                                            "Lucas",
                                            "Darcy",
                                            "Jethro",
                                            "Toby"
                                        ]
                                    ),
                                    False,
                                    wave
                                )
                            )

                        e.spawn_timer = 300

                    continue


                # =================================================
                # JACK
                # =================================================

                if e.name == "Jack":

                    if not e.enraged:

                        e.ability_timer -= 1

                        if e.ability_timer <= 0:

                            e.enraged = True
                            e.speed = 4.0

                    else:

                        e.speed = 4.0


                # =================================================
                # LINCOLN
                # =================================================

                if e.name == "Lincoln":

                    e.special_timer -= 1

                    if e.special_timer <= 0:

                        angle = random.uniform(
                            0,
                            math.pi * 2
                        )

                        d = random.randint(
                            100,
                            220
                        )

                        e.x = (
                            target_x +
                            math.cos(angle) * d
                        )

                        e.y = (
                            target_y +
                            math.sin(angle) * d
                        )

                        e.x = max(
                            -20,
                            min(
                                e.x,
                                WIDTH + 20
                            )
                        )

                        e.y = max(
                            -20,
                            min(
                                e.y,
                                HEIGHT + 20
                            )
                        )

                        e.special_timer = random.randint(
                            150,
                            240
                        )


                # =================================================
                # TOBY
                # =================================================

                if e.name == "Toby":

                    e.dash_timer -= 1

                    if (
                        e.dash_timer <= 0
                        and e.dash_active <= 0
                    ):

                        ddx = (
                            target_x -
                            e.x -
                            e.size // 2
                        )

                        ddy = (
                            target_y -
                            e.y -
                            e.size // 2
                        )

                        dlen = math.sqrt(
                            ddx * ddx +
                            ddy * ddy
                        )

                        if dlen != 0:

                            ddx /= dlen
                            ddy /= dlen

                            e.dash_vx = ddx * 7
                            e.dash_vy = ddy * 7

                            e.dash_active = 35

                        e.dash_timer = random.randint(
                            180,
                            280
                        )

                    if e.dash_active > 0:

                        e.x += e.dash_vx
                        e.y += e.dash_vy

                        e.dash_active -= 1

                    else:

                        if e.x < target_x:
                            e.x += e.speed

                        elif e.x > target_x:
                            e.x -= e.speed

                        if e.y < target_y:
                            e.y += e.speed

                        elif e.y > target_y:
                            e.y -= e.speed

                else:

                    move_speed = e.speed
                    if player.name == "Mr Ginn" and distance(
                        player.x + player.size // 2, player.y + player.size // 2,
                        e.x + e.size // 2, e.y + e.size // 2
                    ) < 170:
                        move_speed *= 0.72

                    if e.x < target_x:
                        e.x += move_speed
                    elif e.x > target_x:
                        e.x -= move_speed

                    if e.y < target_y:
                        e.y += move_speed
                    elif e.y > target_y:
                        e.y -= move_speed

                # =================================================
                # ABILITY TIMER
                # =================================================

                if not e.small:
                    e.ability_timer -= 1


                # =================================================
                # MR DENG
                # =================================================

                if (
                    e.name == "Mr Deng"
                    and e.ability_timer <= 0
                ):

                    for i in range(6):
                        if not can_spawn_enemy(enemies):
                            break

                        angle = (
                            i *
                            math.pi * 2 /
                            6
                        )

                        enemies.append(
                            EnemyEntity(
                                e.x +
                                math.cos(angle) * 40,
                                e.y +
                                math.sin(angle) * 40,
                                "Mr Deng's Dog Dinner",
                                True,
                                wave
                            )
                        )

                    e.ability_timer = random.randint(
                        240,
                        360
                    )


                # =================================================
                # DARCY
                # =================================================

                if (
                    e.name == "Darcy"
                    and e.ability_timer <= 0
                ):

                    e.shield_timer = 240

                    e.ability_timer = random.randint(
                        300,
                        420
                    )

                if e.shield_timer > 0:
                    e.shield_timer -= 1


                # =================================================
                # JETHRO
                # =================================================

                if (
                    e.name == "Jethro"
                    and e.ability_timer <= 0
                ):

                    create_enemy_bullet(
                        enemy_bullets,
                        e.x + e.size // 2,
                        e.y + e.size // 2,
                        target_x,
                        target_y,
                        4.5,
                        7
                    )

                    e.ability_timer = random.randint(
                        90,
                        150
                    )


                # =================================================
                # KIRAT
                # =================================================

                if (
                    e.name == "Kirat"
                    and e.ability_timer <= 0
                ):

                    bx = (
                        e.x +
                        e.size // 2
                    )

                    by = (
                        e.y +
                        e.size // 2
                    )

                    base_angle = math.atan2(
                        target_y - by,
                        target_x - bx
                    )

                    for offset in [
                        -0.45,
                        -0.225,
                        0,
                        0.225,
                        0.45
                    ]:

                        angle = (
                            base_angle +
                            offset
                        )

                        enemy_bullets.append(
                            EnemyBullet(
                                bx,
                                by,
                                math.cos(angle) * 4.5,
                                math.sin(angle) * 4.5,
                                6
                            )
                        )

                    e.ability_timer = random.randint(
                        120,
                        190
                    )


                # =================================================
                # LENNY
                # =================================================

                if (
                    e.name == "Lenny"
                    and e.ability_timer <= 0
                ):

                    for _ in range(2):
                        if not can_spawn_enemy(enemies):
                            break

                        angle = random.uniform(
                            0,
                            math.pi * 2
                        )

                        enemies.append(
                            EnemyEntity(
                                e.x +
                                math.cos(angle) * 45,
                                e.y +
                                math.sin(angle) * 45,
                                random.choice(
                                    [
                                        "Lucas",
                                        "Darcy",
                                        "Jethro",
                                        "Jack",
                                        "Toby",
                                        "Kirat"
                                    ]
                                ),
                                False,
                                wave
                            )
                        )

                    e.ability_timer = random.randint(
                        300,
                        450
                    )


                # =================================================
                # STRAIGHT TEETH
                # =================================================

                if (
                    e.name == "straight teeth"
                    and e.ability_timer <= 0
                ):

                    area_effects.append(
                        AreaEffect(
                            e.x + e.size // 2,
                            e.y + e.size // 2,
                            70,
                            180,
                            PINK,
                            5
                        )
                    )

                    e.ability_timer = random.randint(
                        240,
                        360
                    )


                # =================================================
                # MR GINN
                # =================================================

                if (
                    e.name == "Mr Ginn"
                    and e.ability_timer <= 0
                ):

                    area_effects.append(
                        AreaEffect(
                            target_x,
                            target_y,
                            110,
                            150,
                            DARK_BLUE,
                            8
                        )
                    )

                    e.ability_timer = random.randint(
                        300,
                        420
                    )


            # ====================================================
            # AREA EFFECTS
            # ====================================================

            for area in area_effects[:]:

                area.duration -= 1

                if area.duration <= 0:

                    area_effects.remove(area)

                    continue

                player_cx = (
                    player.x +
                    player.size // 2
                )

                player_cy = (
                    player.y +
                    player.size // 2
                )

                if (
                    area.damage > 0
                    and distance(
                        area.x,
                        area.y,
                        player_cx,
                        player_cy
                    ) < area.radius
                    and player.invuln == 0
                ):

                    blocked = False
                    if player.name == "Darcy" and player.passive_guard_cooldown <= 0:
                        player.passive_guard_cooldown = FPS * 12
                        player.invuln = FPS
                        add_kill_feed(player, "GUARDIAN BLOCK")
                        blocked = True
                    elif player.name == "Ben" and random.random() < 0.18:
                        player.invuln = 20
                        add_kill_feed(player, "PHANTOM DODGE")
                        blocked = True

                    if not blocked:
                        incoming = area.damage
                        if player.name == "Mr Byrne":
                            incoming *= 0.75
                        if player.name == "Lincoln" and random.random() < 0.12:
                            player.invuln = 20
                            add_kill_feed(player, "PHASE DODGE")
                            blocked = True
                        if not blocked:
                            player.hp -= incoming
                            player.invuln = 20

                    if player.hp <= 0:

                        player.hp = 0
                        game_over = True


                # Player abilities can damage enemies.
                if area.damage > 0:

                    for e in enemies[:]:

                        if distance(
                            area.x,
                            area.y,
                            e.x + e.size // 2,
                            e.y + e.size // 2
                        ) < area.radius:

                            e.hp -= area.damage


            # ====================================================
            # REMOVE DEAD ENEMIES FROM AREA DAMAGE
            # ====================================================

            for e in enemies[:]:

                if e.hp <= 0:

                    if e.is_boss:

                        score += award_kill(player, e)
                        for _ in range(5):

                            pickups.append(
                                Pickup(
                                    e.x + random.randint(-50, 50),
                                    e.y + random.randint(-50, 50),
                                    random.choice(
                                        ["speed", "fire"]
                                    )
                                )
                            )

                    else:

                        score += award_kill(player, e)

                    enemies.remove(e)


            # ====================================================
            # ENEMY BULLETS
            # ====================================================

            for bullet in enemy_bullets[:]:

                bullet.x += bullet.vx
                bullet.y += bullet.vy

                bullet.life -= 1

                if (
                    bullet.life <= 0
                    or bullet.x < -30
                    or bullet.x > WIDTH + 30
                    or bullet.y < -30
                    or bullet.y > HEIGHT + 30
                ):

                    if bullet in enemy_bullets:
                        enemy_bullets.remove(
                            bullet
                        )

                    continue

                bullet_rect = pygame.Rect(
                    bullet.x - bullet.radius,
                    bullet.y - bullet.radius,
                    bullet.radius * 2,
                    bullet.radius * 2
                )

                player_rect = pygame.Rect(
                    player.x,
                    player.y,
                    player.size,
                    player.size
                )

                if (
                    bullet_rect.colliderect(
                        player_rect
                    )
                    and player.invuln == 0
                ):

                    blocked = False
                    if player.name == "Darcy" and player.passive_guard_cooldown <= 0:
                        player.passive_guard_cooldown = FPS * 12
                        player.invuln = FPS
                        add_kill_feed(player, "GUARDIAN BLOCK")
                        blocked = True
                    elif player.name == "Ben" and random.random() < 0.18:
                        player.invuln = 20
                        add_kill_feed(player, "PHANTOM DODGE")
                        blocked = True
                    elif player.name == "Lincoln" and random.random() < 0.12:
                        player.invuln = 20
                        add_kill_feed(player, "PHASE DODGE")
                        blocked = True

                    if not blocked:
                        damage = 10 + wave // 3
                        if player.name == "Mr Byrne":
                            damage = int(damage * 0.75)
                        player.hp -= damage
                        player.invuln = 30

                    if bullet in enemy_bullets:
                        enemy_bullets.remove(
                            bullet
                        )

                    if player.hp <= 0:

                        player.hp = 0
                        game_over = True


            # ====================================================
            # PLAYER / ENEMY COLLISION
            # ====================================================

            player_rect = pygame.Rect(
                player.x,
                player.y,
                player.size,
                player.size
            )

            if player.invuln > 0:
                player.invuln -= 1

            for e in enemies[:]:

                enemy_rect = pygame.Rect(
                    e.x,
                    e.y,
                    e.size,
                    e.size
                )

                if (
                    player_rect.colliderect(
                        enemy_rect
                    )
                    and player.invuln == 0
                ):

                    damage = (
                        35 +
                        wave // 2
                        if e.is_boss
                        else 10 +
                        wave // 4
                    )

                    if player.name == "Mr Byrne":
                        damage = int(damage * 0.75)
                    if player.name == "Darcy" and player.passive_guard_cooldown <= 0:
                        player.passive_guard_cooldown = FPS * 12
                        player.invuln = FPS
                        add_kill_feed(player, "GUARDIAN BLOCK")
                        damage = 0
                    elif player.name == "Ben" and random.random() < 0.18:
                        player.invuln = 20
                        add_kill_feed(player, "PHANTOM DODGE")
                        damage = 0
                    elif player.name == "Lincoln" and random.random() < 0.12:
                        player.invuln = 20
                        add_kill_feed(player, "PHASE DODGE")
                        damage = 0

                    player.hp -= damage
                    player.invuln = max(player.invuln, 30)

                    if player.hp <= 0:

                        player.hp = 0
                        game_over = True


            # ====================================================
            # TEAR / ENEMY COLLISION
            # ====================================================

            for t in tears[:]:

                tear_rect = pygame.Rect(
                    t.x - t.radius,
                    t.y - t.radius,
                    t.radius * 2,
                    t.radius * 2
                )

                hit_enemy = False

                for e in enemies[:]:

                    enemy_rect = pygame.Rect(
                        e.x,
                        e.y,
                        e.size,
                        e.size
                    )

                    if not tear_rect.colliderect(
                        enemy_rect
                    ):
                        continue

                    if t.passive and e in t.hit_enemies:
                        continue
                    t.hit_enemies.add(e)

                    # Impact sparks where the tear connects.
                    spawn_burst(t.x, t.y, TEAR_BLUE,
                                count=6, speed=2.0, spread=360,
                                size=2, life=14)


                    # --------------------------------------------
                    # BOSS
                    # --------------------------------------------

                    if e.is_boss:

                        e.hp -= t.damage

                        hit_enemy = True

                        if not t.passive:
                            break
                        continue


                    # --------------------------------------------
                    # DARCY SHIELD
                    # --------------------------------------------

                    if (
                        e.name == "Darcy"
                        and e.shield_timer > 0
                    ):

                        hit_enemy = True

                        if not t.passive:
                            break
                        continue


                    # --------------------------------------------
                    # CHUDSON
                    # --------------------------------------------

                    if (
                        e.name == "chudson mcchud"
                        and e.hp <= t.damage
                    ):

                        for i in range(2):
                            if not can_spawn_enemy(enemies):
                                break

                            enemies.append(
                                EnemyEntity(
                                    e.x +
                                    math.cos(
                                        i * math.pi
                                    ) * 30,
                                    e.y +
                                    math.sin(
                                        i * math.pi
                                    ) * 30,
                                    "Chudson Jr.",
                                    True,
                                    wave
                                )
                            )


                    # --------------------------------------------
                    # DAMAGE NORMAL ENEMY
                    # --------------------------------------------

                    e.hp -= t.damage

                    hit_enemy = True

                    if e.hp <= 0:

                        # Enemy gives a visible pop when they die.
                        spawn_burst(e.x + e.size // 2, e.y + e.size // 2,
                                    (255, 120, 80), count=16, speed=3.0,
                                    spread=360, size=3, life=24)
                        spawn_burst(e.x + e.size // 2, e.y + e.size // 2,
                                    WHITE, count=6, speed=2.2,
                                    spread=360, size=2, life=18)

                        score += award_kill(player, e)

                        if player.name == "Will":
                            player.hp = min(player.max_hp, player.hp + 1)

                        if player.name == "Kempson" and random.random() < 0.12:
                            player.ability_cooldown = max(0, player.ability_cooldown - FPS)
                            add_kill_feed(player, "KEMPSON DEAL  +1s READY")

                        if player.name == "chudson mcchud":
                            area_effects.append(
                                AreaEffect(
                                    e.x + e.size // 2,
                                    e.y + e.size // 2,
                                    45,
                                    1,
                                    DARK_ORANGE,
                                    18
                                )
                            )

                        if random.random() < 0.045:

                            pickups.append(
                                Pickup(
                                    e.x + e.size // 2,
                                    e.y + e.size // 2,
                                    random.choice(
                                        [
                                            "speed",
                                            "fire"
                                        ]
                                    )
                                )
                            )

                    if not t.passive:
                        break

                if hit_enemy and not t.passive:

                    if t in tears:

                        tears.remove(t)


            # ====================================================
            # REMOVE DEAD ENEMIES
            # ====================================================

            for e in enemies[:]:

                if e.hp <= 0:

                    # Bigger death explosion for bosses and mini-bosses.
                    if e.is_boss or e.is_mini_boss or e.is_elite:
                        spawn_burst(e.x + e.size // 2, e.y + e.size // 2,
                                    GOLD, count=40, speed=4.2,
                                    spread=360, size=3.5, life=34)
                        spawn_burst(e.x + e.size // 2, e.y + e.size // 2,
                                    ORANGE, count=20, speed=3.0,
                                    spread=360, size=3, life=28)
                        g_flashes.append({
                            "x": e.x + e.size // 2,
                            "y": e.y + e.size // 2,
                            "radius": max(22, e.size),
                            "life": 8, "max_life": 8,
                            "colour": GOLD,
                            "alpha": 150,
                        })

                    if e.is_boss:

                        score += award_kill(player, e)

                        for _ in range(5):

                            pickups.append(
                                Pickup(
                                    e.x + random.randint(-50, 50),
                                    e.y + random.randint(-50, 50),
                                    random.choice(
                                        ["speed", "fire"]
                                    )
                                )
                            )

                    elif e.is_mini_boss or e.is_elite:

                        score += award_kill(player, e)

                    if e in enemies:
                        enemies.remove(e)


            # ====================================================
            # PICKUPS
            # ====================================================

            for pickup in pickups[:]:

                pickup.update()

                if pickup.life <= 0:

                    pickups.remove(
                        pickup
                    )

                    continue

                player_cx = (
                    player.x +
                    player.size // 2
                )

                player_cy = (
                    player.y +
                    player.size // 2
                )

                if distance(
                    pickup.x,
                    pickup.y,
                    player_cx,
                    player_cy
                ) < 30:

                    if pickup.type == "speed":

                        player.speed_boost_timer = (
                            FPS * 8
                        )

                    else:

                        player.fire_rate_timer = (
                            FPS * 8
                        )

                    pickups.remove(
                        pickup
                    )

        update_fx()

        # ========================================================
        # RENDER
        # ========================================================

        draw_gradient_background()

        if not game_over:

            # ====================================================
            # AREA EFFECTS
            # ====================================================

            for area in area_effects:

                pulse = int(
                    5 *
                    math.sin(
                        pygame.time.get_ticks()
                        / 100
                    )
                )

                pygame.draw.circle(
                    screen,
                    area.color,
                    (
                        int(area.x),
                        int(area.y)
                    ),
                    area.radius + pulse,
                    3
                )


            # ====================================================
            # PICKUPS
            # ====================================================

            for pickup in pickups:
                pickup.draw()


            # ====================================================
            # PLAYER TRAIL
            # ====================================================

            player.draw_trail()

            # ====================================================
            # PLAYER
            # ====================================================

            if player.invuln % 4 < 2:

                cx = int(player.x + player.size // 2)
                cy = int(player.y + player.size // 2)
                glow_circle((cx, cy), player.size // 2, player.color, 28)
                if player.sprite:
                    screen.blit(player.sprite, (int(player.x), int(player.y)))
                else:
                    pygame.draw.rect(
                        screen,
                        player.color,
                        (player.x, player.y, player.size, player.size),
                        border_radius=9
                    )
                    pygame.draw.rect(
                        screen,
                        WHITE,
                        (player.x, player.y, player.size, player.size),
                        2,
                        border_radius=9
                    )

            if player.ability_flash > 0:

                pygame.draw.circle(
                    screen,
                    WHITE,
                    (
                        int(
                            player.x +
                            player.size // 2
                        ),
                        int(
                            player.y +
                            player.size // 2
                        )
                    ),
                    35,
                    3
                )


            # ====================================================
            # TEARS
            # ====================================================

            for t in tears:

                tear_colour = (105, 185, 255) if t.passive else TEAR_BLUE
                glow_circle((t.x, t.y), t.radius, tear_colour, 22)
                pygame.draw.circle(
                    screen,
                    tear_colour,
                    (int(t.x), int(t.y)),
                    t.radius
                )
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (int(t.x), int(t.y)),
                    max(1, t.radius // 3)
                )


            # ====================================================
            # ENEMY BULLETS
            # ====================================================

            for bullet in enemy_bullets:

                glow_circle((bullet.x, bullet.y), bullet.radius, YELLOW, 28)
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (int(bullet.x), int(bullet.y)),
                    bullet.radius
                )
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (int(bullet.x), int(bullet.y)),
                    max(1, bullet.radius // 3)
                )


            # ====================================================
            # BREAKABLE BRICKS
            # ====================================================

            for brick in bricks:
                brick_rect = pygame.Rect(brick.x, brick.y, brick.size, brick.size)
                pygame.draw.rect(screen, (112, 55, 36), brick_rect, border_radius=3)
                pygame.draw.rect(screen, (205, 120, 75), brick_rect, 2, border_radius=3)
                pygame.draw.line(screen, (70, 30, 22),
                                 (brick.x, brick.y + brick.size // 2),
                                 (brick.x + brick.size, brick.y + brick.size // 2), 2)
                pygame.draw.line(screen, (70, 30, 22),
                                 (brick.x + brick.size // 2, brick.y),
                                 (brick.x + brick.size // 2, brick.y + brick.size // 2), 2)
                bar((brick.x, brick.y - 7, brick.size, 4), brick.hp, brick.max_hp, ORANGE)


            # ====================================================
            # ENEMIES
            # ====================================================

            for e in enemies:

                if e.is_mini_boss:
                    if e.eating_flash > 0:
                        glow_circle((e.x + e.size // 2, e.y + e.size // 2),
                                    e.size, GREEN, 32)
                    pygame.draw.rect(screen, (68, 155, 65),
                                     (e.x, e.y, e.size, e.size), border_radius=8)
                    pygame.draw.rect(screen, WHITE,
                                     (e.x, e.y, e.size, e.size), 2, border_radius=8)
                    pygame.draw.rect(screen, BROWN,
                                     (e.x + 9, e.y + 20, e.size - 18, 12), border_radius=4)
                    pygame.draw.circle(screen, WHITE, (int(e.x + 15), int(e.y + 14)), 4)
                    pygame.draw.circle(screen, WHITE, (int(e.x + 31), int(e.y + 14)), 4)
                    bar((e.x, e.y - 10, e.size, 5), e.hp, e.max_hp, GREEN)
                    matt_label = font_enemy.render("MATT", True, GREEN)
                    screen.blit(matt_label, (e.x + e.size // 2 - matt_label.get_width() // 2,
                                             e.y - 29))
                    continue

                if e.is_boss:

                    pygame.draw.rect(
                        screen,
                        DARK_RED,
                        (
                            e.x,
                            e.y,
                            e.size,
                            e.size
                        )
                    )

                    pygame.draw.rect(
                        screen,
                        GOLD,
                        (
                            e.x - 4,
                            e.y - 4,
                            e.size + 8,
                            e.size + 8
                        ),
                        4
                    )

                    name_surf = font_ui.render(
                        "MR CHAMPION",
                        True,
                        GOLD
                    )

                    screen.blit(
                        name_surf,
                        (
                            e.x +
                            e.size // 2 -
                            name_surf.get_width() // 2,
                            e.y - 35
                        )
                    )
                    phase_surf = font_tiny.render(f"PHASE {e.phase}", True, WHITE)
                    screen.blit(phase_surf, (e.x + e.size // 2 - phase_surf.get_width() // 2, e.y + e.size + 5))
                    if e.phase_flash > 0:
                        flash = font_ui.render(f"PHASE {e.phase}!", True, GOLD)
                        screen.blit(flash, (WIDTH // 2 - flash.get_width() // 2, 82))

                    continue


                if e.small:

                    enemy_color = ORANGE

                elif e.name == "Mr Deng":

                    enemy_color = PURPLE

                elif e.name == "Darcy":

                    enemy_color = CYAN

                elif e.name == "Jethro":

                    enemy_color = YELLOW

                elif e.name == "Lincoln":

                    enemy_color = DARK_BLUE

                elif e.name == "Jack":

                    enemy_color = (
                        RED
                        if e.enraged
                        else BROWN
                    )

                elif e.name == "Lenny":

                    enemy_color = LIME

                elif e.name == "straight teeth":

                    enemy_color = PINK

                elif e.name == "chudson mcchud":

                    enemy_color = DARK_ORANGE

                elif e.name == "Toby":

                    enemy_color = (
                        YELLOW
                        if e.dash_active > 0
                        else ORANGE
                    )

                elif e.name == "Kirat":

                    enemy_color = CYAN

                elif e.name == "Mr Ginn":

                    enemy_color = PURPLE

                elif e.name == "Bentley":

                    enemy_color = GOLD

                elif e.name == "Beau":

                    enemy_color = (
                        100,
                        150,
                        255
                    )

                elif e.name == "Billy":

                    enemy_color = (
                        255,
                        100,
                        100
                    )

                elif e.name == "Will":

                    enemy_color = (
                        100,
                        255,
                        180
                    )

                elif e.name == "Wyatt":

                    enemy_color = (
                        180,
                        100,
                        255
                    )

                else:

                    enemy_color = RED


                pygame.draw.rect(
                    screen,
                    enemy_color,
                    (e.x, e.y, e.size, e.size),
                    border_radius=7
                )
                pygame.draw.rect(
                    screen,
                    WHITE if e.small else (220, 225, 240),
                    (e.x, e.y, e.size, e.size),
                    1,
                    border_radius=7
                )
                if e.is_elite:
                    pygame.draw.rect(screen, GOLD, (e.x - 3, e.y - 3, e.size + 6, e.size + 6), 3, border_radius=9)
                    elite_tag = font_tiny.render("ELITE", True, GOLD)
                    screen.blit(elite_tag, (e.x + e.size // 2 - elite_tag.get_width() // 2, e.y - 22))


                # =================================================
                # ENEMY HP BAR
                # =================================================

                if not e.small:

                    bar_width = e.size

                    pygame.draw.rect(
                        screen,
                        BLACK,
                        (
                            e.x,
                            e.y - 9,
                            bar_width,
                            5
                        )
                    )

                    hp_width = int(
                        (
                            e.hp /
                            e.max_hp
                        ) *
                        bar_width
                    )

                    hp_width = max(
                        0,
                        min(
                            hp_width,
                            bar_width
                        )
                    )

                    pygame.draw.rect(
                        screen,
                        GREEN,
                        (
                            e.x,
                            e.y - 9,
                            hp_width,
                            5
                        )
                    )


                # Toby dash
                if (
                    e.name == "Toby"
                    and e.dash_active > 0
                ):

                    pygame.draw.rect(
                        screen,
                        WHITE,
                        (
                            e.x - 5,
                            e.y - 5,
                            e.size + 10,
                            e.size + 10
                        ),
                        3
                    )


                # Darcy shield
                if (
                    e.name == "Darcy"
                    and e.shield_timer > 0
                ):

                    pygame.draw.circle(
                        screen,
                        CYAN,
                        (
                            int(
                                e.x +
                                e.size // 2
                            ),
                            int(
                                e.y +
                                e.size // 2
                            )
                        ),
                        e.size,
                        3
                    )


                if e.small:
                    continue


                n_surf = font_enemy.render(
                    e.name,
                    True,
                    YELLOW
                )

                screen.blit(
                    n_surf,
                    (
                        e.x +
                        e.size // 2 -
                        n_surf.get_width() // 2,
                        e.y - 22
                    )
                )


            # ====================================================
            # BOSS HEALTH BAR
            # ====================================================

            bosses = [
                e for e in enemies
                if e.is_boss
            ]

            if bosses:

                boss = bosses[0]

                bar_width = 500

                pygame.draw.rect(
                    screen,
                    GRAY,
                    (
                        WIDTH // 2 -
                        bar_width // 2,
                        45,
                        bar_width,
                        18
                    )
                )

                hp_width = int(
                    (
                        boss.hp /
                        boss.max_hp
                    ) *
                    bar_width
                )

                hp_width = max(
                    0,
                    min(
                        hp_width,
                        bar_width
                    )
                )

                pygame.draw.rect(
                    screen,
                    RED,
                    (
                        WIDTH // 2 -
                        bar_width // 2,
                        45,
                        hp_width,
                        18
                    )
                )

                boss_text = font_small.render(
                    f"MR CHAMPION "
                    f"{boss.hp}/{boss.max_hp}",
                    True,
                    WHITE
                )

                screen.blit(
                    boss_text,
                    (
                        WIDTH // 2 -
                        boss_text.get_width() // 2,
                        65
                    )
                )


            # ====================================================
            # HUD HP
            # ====================================================

            panel(pygame.Rect(10, 10, 250, 54), PANEL, BORDER, 12, 1)
            hp_w = max(0, min(200, int((player.hp / player.max_hp) * 200)))
            bar((20, 18, 200, 12), player.hp, player.max_hp, GREEN if player.hp > player.max_hp * 0.35 else RED)
            hp_label = font_tiny.render("HEALTH", True, MUTED)
            screen.blit(hp_label, (20, 38))

            hp_text_name = player.name
            hp_text_hp = f"{player.hp}/{player.max_hp} HP"
            hp_text_full = f"{player.name}: {hp_text_hp}"
            if font_enemy.size(hp_text_full)[0] > 205:
                while (len(hp_text_name) > 1 and
                       font_enemy.size(f"{hp_text_name}: {hp_text_hp}")[0] > 205):
                    hp_text_name = hp_text_name[:-1]
                hp_text_full = f"{hp_text_name}…: {hp_text_hp}"
            hp_text = font_enemy.render(hp_text_full, True, WHITE)

            screen.blit(
                hp_text,
                (
                    220,
                    12
                )
            )


            # ====================================================
            # SCORE
            # ====================================================

            score_card = pygame.Rect(WIDTH - 180, 10, 170, 54)
            panel(score_card, PANEL, BORDER, 12, 1)
            score_surf = font_ui.render(f"{score:,}", True, GOLD)
            screen.blit(score_surf, (score_card.right - score_surf.get_width() - 15, 16))
            score_label = font_tiny.render("SCORE", True, MUTED)
            screen.blit(score_label, (score_card.x + 15, 38))


            # ====================================================
            # WAVE
            # ====================================================

            wave_surf = font_ui.render(f"WAVE {wave}", True, WHITE)
            wave_box = pygame.Rect(530 - 65, 12, 130, 42)
            panel(wave_box, PANEL, ACCENT, 12, 1)
            screen.blit(
                wave_surf,
                (wave_box.centerx - wave_surf.get_width() // 2, 19)
            )


            # ====================================================
            # ABILITY HUD
            # ====================================================

            if player.ability_cooldown <= 0:

                ability_text = (
                    f"E: {cfg['ability']} READY"
                )

                ability_colour = GREEN

            else:

                seconds = (
                    player.ability_cooldown
                    / FPS
                )

                ability_text = (
                    f"E: {cfg['ability']} "
                    f"{seconds:.1f}s"
                )

                ability_colour = RED

            ability_surf = font_small.render(
                ability_text,
                True,
                ability_colour
            )

            screen.blit(
                ability_surf,
                (
                    10,
                    50
                )
            )


            # ====================================================
            # SHOP / UPGRADE INFO
            # ====================================================

            upgrade_text = font_small.render(
                f"DMG {player.damage} | "
                f"SPD +{player.speed_upgrades} | "
                f"FIRE +{player.fire_upgrades} | "
                f"SCORE x{player.score_multiplier}",
                True,
                LIGHT_GRAY
            )

            upgrade_box = pygame.Rect(205, 536, 390, 30)
            panel(upgrade_box, PANEL, BORDER, 9, 1)
            screen.blit(
                upgrade_text,
                (
                    upgrade_box.centerx - upgrade_text.get_width() // 2,
                    upgrade_box.y + 5
                )
            )


            # ====================================================
            # EFFECT HUD
            # ====================================================

            effect_y = 75

            if player.speed_boost_timer > 0:

                seconds = (
                    player.speed_boost_timer
                    // FPS
                )

                speed_text = font_small.render(
                    f"SPEED BOOST: {seconds + 1}s",
                    True,
                    SPEED_GREEN
                )

                screen.blit(
                    speed_text,
                    (
                        10,
                        effect_y
                    )
                )

                effect_y += 18


            if player.fire_rate_timer > 0:

                seconds = (
                    player.fire_rate_timer
                    // FPS
                )

                fire_text = font_small.render(
                    f"RAPID FIRE: {seconds + 1}s",
                    True,
                    FIRE_RED
                )

                screen.blit(
                    fire_text,
                    (
                        10,
                        effect_y
                    )
                )


            # ====================================================
            # BOSS WARNING
            # ====================================================

            if wave % 5 == 0:

                if not boss_spawned_this_wave:

                    warning = font_ui.render(
                        "MR CHAMPION IS COMING!",
                        True,
                        RED
                    )

                    screen.blit(
                        warning,
                        (
                            WIDTH // 2 -
                            warning.get_width() // 2,
                            HEIGHT // 2 - 100
                        )
                    )


            # ====================================================
            # WAVE TRANSITION BANNER
            # ====================================================

            if player.wave_banner_timer > 0:
                player.wave_banner_timer -= 1
                progress = player.wave_banner_timer / max(1, FPS * 2)
                banner_alpha = int(255 * min(1, progress * 1.8))
                banner_w = min(600, 260 + int((1 - progress) * 340))
                banner_rect = pygame.Rect(WIDTH // 2 - banner_w // 2, HEIGHT // 2 - 55, banner_w, 92)
                banner_surface = pygame.Surface((banner_rect.w, banner_rect.h), pygame.SRCALPHA)
                pygame.draw.rect(banner_surface, (*PANEL, max(20, banner_alpha // 3)), banner_surface.get_rect(), border_radius=18)
                pygame.draw.rect(banner_surface, (*GOLD, banner_alpha), banner_surface.get_rect(), 2, border_radius=18)
                screen.blit(banner_surface, banner_rect.topleft)

                wave_label = font_title.render(f"WAVE {player.wave_banner_wave}", True, WHITE)
                screen.blit(
                    wave_label,
                    wave_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 8))
                )
                next_label = font_tiny.render("UPGRADE LOCKED IN", True, GOLD)
                screen.blit(
                    next_label,
                    next_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 28))
                )

            # ====================================================
            # KILL FEED
            # ====================================================

            feed_y = 78
            for item in player.kill_feed[:]:
                item[1] -= 1
            player.kill_feed = [item for item in player.kill_feed if item[1] > 0]
            for message, ttl in reversed(player.kill_feed):
                alpha_colour = GOLD if "PHASE" in message else WHITE
                feed_surf = font_tiny.render(message, True, alpha_colour)
                screen.blit(feed_surf, (WIDTH - feed_surf.get_width() - 14, feed_y))
                feed_y += 16

            # ====================================================
            # CONTROLS
            # ====================================================

            controls = font_small.render(
                "WASD: Move | Arrows: Shoot | "
                "E: Ability | P: Pause",
                True,
                LIGHT_GRAY
            )

            screen.blit(
                controls,
                (
                    10,
                    HEIGHT - 25
                )
            )


            # ====================================================
            # PICKUP LEGEND
            # ====================================================

            legend = font_small.render(
                "Green S = Speed | Red F = Rapid Fire",
                True,
                LIGHT_GRAY
            )

            screen.blit(
                legend,
                (
                    WIDTH -
                    legend.get_width() -
                    10,
                    HEIGHT - 25
                )
            )


        # ========================================================
        # GAME OVER
        # ========================================================

        else:

            # Game-over is a menu state, so restore the menu soundtrack.
            play_music("menu")

            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            overlay.fill(
                (5, 7, 14, 215)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            panel(pygame.Rect(145, 125, 510, 350), PANEL, RED, 20, 2)

            go_surf = font_title.render(
                "GAME OVER",
                True,
                RED
            )

            screen.blit(
                go_surf,
                (
                    WIDTH // 2 -
                    go_surf.get_width() // 2,
                    HEIGHT // 2 - 130
                )
            )

            score_surf = font_ui.render(
                f"Final Score: {score}",
                True,
                WHITE
            )

            screen.blit(
                score_surf,
                (
                    WIDTH // 2 -
                    score_surf.get_width() // 2,
                    HEIGHT // 2 - 50
                )
            )

            wave_surf = font_ui.render(
                f"Reached Wave: {wave}",
                True,
                YELLOW
            )

            screen.blit(
                wave_surf,
                (
                    WIDTH // 2 -
                    wave_surf.get_width() // 2,
                    HEIGHT // 2
                )
            )

            restart = font_ui.render(
                "Press R to Choose Another Character",
                True,
                GREEN
            )

            screen.blit(
                restart,
                (
                    WIDTH // 2 -
                    restart.get_width() // 2,
                    HEIGHT // 2 + 65
                )
            )


        draw_fx()
        draw_fade_overlay()
        draw_custom_cursor()
        pygame.display.flip()

        clock.tick(FPS)


# ============================================================
# PROGRAM START
# ============================================================

main_menu()

game_loop()
