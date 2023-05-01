import os
import subprocess

# Create a user with a given username and password
def create_user(username, password):
    os.system(f"useradd -m {username}")
    os.system(f"echo '{username}:{password}' | sudo chpasswd")
    os.system(f"adduser {username} sudo")
    os.system("sed -i 's/\/bin\/sh/\/bin\/bash/g' /etc/passwd")
    print("User created and configured")

# Install Chrome Remote Desktop and a desktop environment
def install_desktop():
    subprocess.run(['wget', 'https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb'], stdout=subprocess.PIPE)
    subprocess.run(['dpkg', '--install', 'chrome-remote-desktop_current_amd64.deb'], stdout=subprocess.PIPE)
    subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'], stdout=subprocess.PIPE)
    os.system("export DEBIAN_FRONTEND=noninteractive")
    os.system("apt install --assume-yes xfce4 desktop-base xfce4-terminal")
    os.system("bash -c 'echo \"exec /etc/X11/Xsession /usr/bin/xfce4-session\" > /etc/chrome-remote-desktop-session'")
    os.system("apt remove --assume-yes gnome-terminal")
    os.system("apt install --assume-yes xscreensaver")
    os.system("systemctl disable lightdm.service")
    print("Desktop environment installed")

# Install Google Chrome
def install_chrome():
    subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"], stdout=subprocess.PIPE)
    subprocess.run(["dpkg", "--install", "google-chrome-stable_current_amd64.deb"], stdout=subprocess.PIPE)
    subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'], stdout=subprocess.PIPE)
    print("Google Chrome installed")

# Install and configure VPS
def install_vps(username, password, CRP, Pin):
    create_user(username, password)
    install_desktop()
    install_chrome()
    os.system(f"adduser {username} chrome-remote-desktop")
    command = f"{CRP} --pin={Pin}"
    os.system(f"su - {username} -c '{command}'")
    os.system("service chrome-remote-desktop start")
    print("VPS installed successfully")

# Example usage
username = "user"
password = "root"
CRP = input('Input Code')
Pin = 123456

install_vps(username, password, CRP, Pin)
