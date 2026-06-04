#!/usr/bin/env python3
import subprocess
import os
import re
import random

# ========== НАСТРОЙКИ ==========
ART_FOLDER = ""  # ПУТЬ К ДИРЕКТОРИИ С ФАЙЛАМИ
# ===============================

def parse_escape_codes(text):
    """Преобразует строковые escape-последовательности в настоящие коды"""
    return text.encode().decode('unicode_escape')

def load_random_art():
    """Загружает случайный ASCII-арт из папки"""
    try:
        if not ART_FOLDER or not os.path.exists(ART_FOLDER):
            return ART, "34", 2
            
        art_files = [f for f in os.listdir(ART_FOLDER) if f.endswith('.py')]
        if not art_files:
            return ART, "34", 2
        
        random_file = random.choice(art_files)
        file_path = os.path.join(ART_FOLDER, random_file)
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        art_match = re.search(r'ART\s*=\s*"""(.*?)"""', content, re.DOTALL)
        color_match = re.search(r'COLOR_FOR_KEYS\s*=\s*"(\d+)"', content)
        offset_match = re.search(r'OFFSET\s*=\s*(\d+)', content)
        
        art_content = ART
        key_color = "34"
        offset = 2
        
        if art_match:
            art_content = parse_escape_codes(art_match.group(1))
        
        if color_match:
            key_color = color_match.group(1)
            
        if offset_match:
            offset = int(offset_match.group(1))
        
        return art_content, key_color, offset
            
    except Exception:
        return ART, "34", 2

# Стандартный арт (фоллбэк)
ART = """
                                               \033[1;34m..
                    \033[1;34m:+++.
              \033[1;37m.:::++\033[1;34m++++\033[1;37m+::.
          \033[1;37m.:+######\033[1;34m++++\033[1;37m######+:.
       \033[1;37m.+#########\033[1;34m+++++\033[1;37m##########:.
     \033[1;37m.+##########\033[1;34m+++++++\033[1;37m##\033[1;34m+\033[1;37m#########+.
    \033[1;37m+###########\033[1;34m+++++++++\033[1;37m############:
   \033[1;37m+##########\033[1;34m++++++\033[1;37m#\033[1;34m++++\033[1;37m#\033[1;34m+\033[1;37m###########+
  \033[1;37m+###########\033[1;34m+++++\033[1;37m###\033[1;34m++++\033[1;37m#\033[1;34m+\033[1;37m###########+
 \033[1;37m:##########\033[1;34m+\033[1;37m#\033[1;34m++++\033[1;37m####\033[1;34m++++\033[1;37m#\033[1;34m+\033[1;37m############:
 \033[1;37m###########\033[1;34m+++++\033[1;37m#####\033[1;34m+++++\033[1;37m#\033[1;34m+\033[1;37m###\033[1;34m++\033[1;37m######+
\033[1;37m.##########\033[1;34m++++++\033[1;37m#####\033[1;34m++++++++++++\033[1;37m#######.
\033[1;37m.##########\033[1;34m+++++++++++++++++++\033[1;37m###########.
 \033[1;37m#####\033[1;34m++++++++++++++\033[1;37m###\033[1;34m++++++++\033[1;37m#########+
 \033[1;37m:###\033[1;34m++++++++++\033[1;37m#########\033[1;34m+++++++\033[1;37m#########:
  \033[1;37m+######\033[1;34m+++++\033[1;37m##########\033[1;34m++++++++\033[1;37m#######+
   \033[1;37m+####\033[1;34m+++++\033[1;37m###########\033[1;34m+++++++++\033[1;37m#####+
    \033[1;37m:##\033[1;34m++++++\033[1;37m############\033[1;34m++++++++++\033[1;37m##:
     \033[1;37m.\033[1;34m++++++\033[1;37m#############\033[1;34m++++++++++\033[1;37m+.
      \033[1;37m:\033[1;34m++++\033[1;37m###############\033[1;34m+++++++\033[1;37m::
     \033[1;37m.\033[1;34m++\033[1;37m. .:+\033[1;37m##############\033[1;34m+++++++\033[1;37m..
     \033[1;34m.:\033[1;37m.      ..::++++++::..:\033[1;34m++++\033[1;37m+.
     \033[1;34m.                       .:+++\033[1;37m.
                                \033[1;34m.:\033[1;37m:

"""

def get_system_info(key_color):
    info = []
    
    info.append(f"\033[1;{key_color}m{os.getlogin()}@{os.uname().nodename}\033[0m")
    info.append(f"\033[1;{key_color}m--------\033[0m")
    
    with open('/etc/os-release', 'r') as f:
        for line in f:
            if line.startswith('PRETTY_NAME='):
                os_name = line.split('=')[1].strip().strip('"')
                arch = subprocess.getoutput('uname -m')
                info.append(f"\033[1;{key_color}mOS:\033[0m {os_name} {arch}")
                break
    
    try:
        with open('/sys/devices/virtual/dmi/id/product_name', 'r') as f:
            host = f.read().strip()
        with open('/sys/devices/virtual/dmi/id/product_version', 'r') as f:
            version = f.read().strip()
        info.append(f"\033[1;{key_color}mHost:\033[0m {host} {version}")
    except:
        info.append(f"\033[1;{key_color}mHost:\033[0m Unknown")
    
    kernel = subprocess.getoutput('uname -r')
    info.append(f"\033[1;{key_color}mKernel:\033[0m {kernel}")
    
    uptime = subprocess.getoutput('uptime -p').replace('up ', '')
    info.append(f"\033[1;{key_color}mUptime:\033[0m {uptime}")
    
    packages = ""
    if os.path.exists('/var/lib/dpkg/status'):
        packages = subprocess.getoutput('dpkg -l | wc -l') + " (dpkg)"
    elif os.path.exists('/var/lib/pacman/local'):
        packages = subprocess.getoutput('pacman -Q | wc -l') + " (pacman)"
    else:
        packages = "Unknown"
    info.append(f"\033[1;{key_color}mPackages:\033[0m {packages}")
    
    shell = os.path.basename(os.getenv('SHELL'))
    shell_version = subprocess.getoutput(f'{shell} --version | head -1')
    version_match = re.search(r'(\d+\.\d+\.\d+)', shell_version)
    shell_ver = version_match.group(1) if version_match else ""
    info.append(f"\033[1;{key_color}mShell:\033[0m {shell} {shell_ver}")
    
    resolution = subprocess.getoutput('xrandr 2>/dev/null | grep "*" | head -1 | cut -d" " -f4')
    info.append(f"\033[1;{key_color}mResolution:\033[0m {resolution}")
    
    de = "Unknown"
    de_version = ""
    
    xdg_de = os.getenv('XDG_CURRENT_DESKTOP')
    if xdg_de:
        de = xdg_de.replace('X-', '').split(':')[-1]
    
    if 'GNOME' in de.upper():
        gnome_version = subprocess.getoutput('gnome-shell --version 2>/dev/null')
        if gnome_version and 'GNOME Shell' in gnome_version:
            de_version = gnome_version.split()[-1]
    elif 'KDE' in de.upper() or 'PLASMA' in de.upper():
        plasma_version = subprocess.getoutput('plasmashell --version 2>/dev/null | head -1')
        if plasma_version:
            version_match = re.search(r'(\d+\.\d+\.\d+|\d+\.\d+)', plasma_version)
            if version_match:
                de_version = version_match.group(1)
    elif 'CINNAMON' in de.upper():
        cinnamon_version = subprocess.getoutput('cinnamon --version 2>/dev/null')
        if cinnamon_version:
            version_match = re.search(r'(\d+\.\d+\.\d+|\d+\.\d+)', cinnamon_version)
            if version_match:
                de_version = version_match.group(1)
    
    de_output = f"{de} {de_version}".strip()
    info.append(f"\033[1;{key_color}mDE:\033[0m {de_output}")
    
    wm = "Unknown"
    
    try:
        result = subprocess.run(['xprop', '-root', '_NET_WM_NAME'], 
                              capture_output=True, text=True, timeout=1)
        if result.returncode == 0 and '_NET_WM_NAME' in result.stdout:
            wm_name = result.stdout.split('=')[1].strip().strip('"')
            if wm_name and wm_name != "": 
                wm = wm_name
    except:
        pass
    
    if wm == "Unknown":
        process_wm_map = [
            ('gnome-shell', 'Mutter'),
            ('kwin_x11', 'KWin'), 
            ('kwin_wayland', 'KWin'),
            ('xfwm4', 'XFWM4'),
            ('openbox', 'Openbox'),
            ('i3', 'i3'),
            ('cinnamon', 'Mutter (Muffin)'),
            ('mutter', 'Mutter'),
        ]
        
        for process, wm_name in process_wm_map:
            try:
                check = subprocess.run(['pgrep', '-x', process], 
                                     capture_output=True, text=True, timeout=1)
                if check.returncode == 0 and check.stdout.strip():
                    wm = wm_name
                    break
            except:
                continue
    
    info.append(f"\033[1;{key_color}mWM:\033[0m {wm}")

    wm_theme = subprocess.getoutput('gsettings get org.cinnamon.theme name 2>/dev/null | tr -d "\'"') or "Unknown"
    info.append(f"\033[1;{key_color}mWM Theme:\033[0m {wm_theme}")
    
    theme = subprocess.getoutput('gsettings get org.gnome.desktop.interface gtk-theme 2>/dev/null | tr -d "\'"') or "Unknown"
    info.append(f"\033[1;{key_color}mTheme:\033[0m {theme}")
    
    icons = subprocess.getoutput('gsettings get org.gnome.desktop.interface icon-theme 2>/dev/null | tr -d "\'"') or "Unknown"
    info.append(f"\033[1;{key_color}mIcons:\033[0m {icons}")
    
    terminal = os.getenv('TERM_PROGRAM') or os.path.basename(os.getenv('TERM')) or "Unknown"
    info.append(f"\033[1;{key_color}mTerminal:\033[0m {terminal}")
    
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if 'model name' in line:
                cpu_full = line.split(':')[1].strip()
                cpu_clean = re.sub(r'\(R\)|\(TM\)|CPU', '', cpu_full)
                cpu_clean = ' '.join(cpu_clean.split())
                cores = subprocess.getoutput('nproc')
                cpu = f"{cpu_clean} ({cores})"
                info.append(f"\033[1;{key_color}mCPU:\033[0m {cpu}")
                break
    
    gpu_full = subprocess.getoutput('lspci | grep VGA | cut -d":" -f3').strip()
    gpu_clean = re.sub(r'\(rev\s+\w+\)|Corporation', '', gpu_full)
    gpu_clean = ' '.join(gpu_clean.split())
    if not gpu_clean or gpu_clean.isspace():
        gpu_clean = "Unknown"
    
    info.append(f"\033[1;{key_color}mGPU:\033[0m {gpu_clean}")
    
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
            mem_dict = {}
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    mem_dict[key.strip()] = int(value.split()[0]) // 1024

        total = mem_dict.get('MemTotal', 0)
        free = mem_dict.get('MemFree', 0) 
        buffers = mem_dict.get('Buffers', 0)
        cached = mem_dict.get('Cached', 0)
        sreclaimable = mem_dict.get('SReclaimable', 0)
        shmem = mem_dict.get('Shmem', 0)

        used = total - free - buffers - cached - sreclaimable + shmem
        
        memory = f"{used}MiB / {total}MiB"
    except:
        memory = "Unknown"
    
    info.append(f"\033[1;{key_color}mMemory:\033[0m {memory}")

    info.append("")

    dark_colors = [
        "\033[40m   \033[0m",
        "\033[41m   \033[0m", 
        "\033[42m   \033[0m",
        "\033[43m   \033[0m",
        "\033[44m   \033[0m",
        "\033[45m   \033[0m",
        "\033[46m   \033[0m",
        "\033[47m   \033[0m",
    ]
    
    bright_colors = [
        "\033[100m   \033[0m",
        "\033[101m   \033[0m",
        "\033[102m   \033[0m",
        "\033[103m   \033[0m",
        "\033[104m   \033[0m",
        "\033[105m   \033[0m",
        "\033[106m   \033[0m",
        "\033[107m   \033[0m",
    ]
    
    info.append("".join(dark_colors))
    info.append("".join(bright_colors))
    
    return info

def colorize(text, art_color):
    if '{#00aaff}' in text or '{!}' in text:
        text = text.replace('{#00aaff}', f'\033[1;{art_color}m')
        text = text.replace('{!}', '\033[1;37m')
        return '\033[1m' + text + '\033[0m'
    else:
        return text

def get_visual_width(text):
    """Возвращает видимую ширину текста без цветовых кодов"""
    clean_text = re.sub(r'\033\[[0-9;]*m', '', text)
    return len(clean_text)

def truncate_info_line(info_line, max_width):
    """Обрезает строку информации до максимальной ширины"""
    clean_text = re.sub(r'\033\[[0-9;]*m', '', info_line)
    if len(clean_text) <= max_width:
        return info_line
    
    result = ""
    current_length = 0
    in_escape = False
    escape_seq = ""
    
    for char in info_line:
        if char == '\033':
            in_escape = True
            escape_seq = char
        elif in_escape:
            escape_seq += char
            if char == 'm':
                in_escape = False
                result += escape_seq
        else:
            if current_length < max_width - 3:
                result += char
                current_length += 1
            else:
                break
    
    return result + "..."

# ========== ОСНОВНОЙ КОД ==========
art_content, key_color, info_offset = load_random_art()
info = get_system_info(key_color)
art_lines = art_content.strip().split('\n')

try:
    term_width = int(subprocess.getoutput('tput cols'))
except:
    term_width = 80

art_width = max(get_visual_width(line) for line in art_lines)
info_start_pos = art_width + 4
info_width = term_width - info_start_pos

for i, line in enumerate(art_lines):
    if '{#00aaff}' in line or '{!}' in line:
        display_line = colorize(line, "34")
        current_art_width = get_visual_width(display_line)
    else:
        display_line = line
        current_art_width = get_visual_width(line)
    
    info_index = i - info_offset
    if info_index >= 0 and info_index < len(info):
        info_line = info[info_index]
        truncated_line = truncate_info_line(info_line, info_width)
        
        padding = info_start_pos - current_art_width
        print(f"{display_line}{' ' * padding}{truncated_line}")
    else:
        print(display_line)

for i in range(len(art_lines) - info_offset, len(info)):
    if i >= 0:
        info_line = info[i]
        truncated_line = truncate_info_line(info_line, info_width)
        print(" " * info_start_pos + truncated_line)
