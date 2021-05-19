# Telegram Linux releases tracker

Yet another Linux releases tracker

https://t.me/linux_releases

## Usage

- `pip install -r requirements.txt`
- Edit script path in `kernel.org.service`
- Move `kernel.org.service` to `/etc/systemd/system`
- Set up `chat_id` and `bot_id` in `kernel_org.py`
- `systemctl enable kernel.org.service`
- `systemctl start kernel.org.service`
- Enjoy
