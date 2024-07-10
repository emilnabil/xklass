import os
import platform
import subprocess
import sys
import time

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()

def check_python_version():
    python_version = platform.python_version()
    if python_version.startswith("3"):
        return "PY3"
    else:
        return "PY2"

def install_packages(packages):
    for package in packages:
        run_command(f"{installer} install {package}")

def remove_old_plugin():
    stdout, stderr = run_command(f"grep -qs 'Package: {PACKAGE}' {STATUS}")
    if stdout or stderr:
        print("   >>>>   Remove old version   <<<<")
        run_command(f"{remover} {PACKAGE}")
        run_command(f"rm -rf /usr/lib/enigma2/python/Plugins/Extensions/XKlass")
        time.sleep(1)
    else:
        print("   >>>>   No Older Version Was Found   <<<<")
        time.sleep(1)

TMPDIR = '/tmp'
PACKAGE = 'enigma2-plugin-extensions-xklass'
MY_URL = 'https://dreambox4u.com/emilnabil237/plugins/xklass'
MY_EM = "============================================================================================================"
PYTHON = check_python_version()

if os.path.exists("/etc/opkg/opkg.conf"):
    STATUS = '/var/lib/opkg/status'
    OSTYPE = 'Opensource'
    installer = 'opkg'
    remover = 'opkg remove --force-depends'
elif os.path.exists("/etc/apt/apt.conf"):
    STATUS = '/var/lib/dpkg/status'
    OSTYPE = 'DreamOS'
    installer = 'apt-get'
    remover = 'apt-get purge --auto-remove'
    dpkg_installer = 'dpkg -i --force-overwrite'

# Remove previous files
run_command(f"rm -rf {TMPDIR}/{PACKAGE}* > /dev/null 2>&1")

# Remove old plugin
remove_old_plugin()

# Install new plugin
print("============================================================================================================================")
print("   Install Plugin please wait ")

if OSTYPE == "Opensource":
    if PYTHON == "PY3":
        packages = [
            'python3-requests', 'python3-pillow', 'p7zip', 'curl', 
            'enigma2-plugin-systemplugins-serviceapp', 'ffmpeg', 
            'exteplayer3', 'gstplayer', 'gstreamer1.0-plugins-good', 
            'gstreamer1.0-plugins-ugly'
        ]
    else:
        packages = [
            'python-requests', 'python-multiprocessing', 'python-image', 
            'python-imaging', 'enigma2-plugin-systemplugins-serviceapp', 
            'ffmpeg', 'exteplayer3', 'gstplayer', 'gstreamer1.0-plugins-good', 
            'gstreamer1.0-plugins-ugly', 'gstreamer1.0-plugins-base', 
            'gstreamer1.0-plugins-bad'
        ]
    install_packages(packages)
    print("Installing XKlass plugin Please Wait ......")
    time.sleep(2)
    run_command(f"curl -k -Lbk -m 55532 -m 555104 '{MY_URL}/enigma2-plugin-extensions-xklass_all.ipk' > /tmp/enigma2-plugin-extensions-xklass_all.ipk")
    run_command(f"{installer} install /tmp/enigma2-plugin-extensions-xklass_all.ipk")

elif OSTYPE == "DreamOS":
    if PYTHON == "PY3":
        packages = ['python3-requests', 'python3-multiprocessing']
    else:
        packages = ['python-requests', 'python-image', 'python-imaging', 'wget']
    install_packages(packages)
    print("Installing XKlass plugin Please Wait ......")
    time.sleep(2)
    run_command(f"curl -k -Lbk -m 55532 -m 555104 '{MY_URL}/enigma2-plugin-extensions-xklass_all.deb' > /tmp/enigma2-plugin-extensions-xklass_all.deb")
    run_command(f"{dpkg_installer} /tmp/enigma2-plugin-extensions-xklass_all.deb")

# Download playlists
print(" DOWNLOAD Playlists By Emil_Nabil ")
time.sleep(3)
run_command(f"wget -O /etc/enigma2/xklass/playlists.txt '{MY_URL}/playlists.txt'")

# Remove any files
print(MY_EM)
run_command(f"rm -rf {TMPDIR}/{PACKAGE}*")

time.sleep(1)
print("\n****************************************************************************************")
print(MY_EM)
print("**                xklass **")
print("****************************************************************************************\n")

if OSTYPE == "Opensource":
    run_command("killall -9 enigma2")
else:
    run_command("systemctl restart enigma2")


