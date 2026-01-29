#!/usr/bin/env python3

import json
import time
import threading
import logging
import signal
import sys
import paho.mqtt.client as mqtt
import pychrome

# --- logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
log = logging.getLogger(__name__)

# --- Chromium / pychrome setup ---
browser = pychrome.Browser(url="http://127.0.0.1:9222")
tab = browser.new_tab()
tab.start()
tab.Page.enable()

def load_url(url):
    log.info("loading url: %s", url)
    tab.Page.stopLoading()
    tab.Page.navigate(url=url)

# --- shared state ---
lock = threading.Lock()
current_cmd = None
cmd_version = 0

# --- worker ---
def worker():
    global current_cmd, cmd_version
    last_version = -1

    while True:
        with lock:
            cmd = current_cmd
            version = cmd_version

        if cmd is None or version == last_version:
            time.sleep(0.1)
            continue

        last_version = version

        urls = cmd.get("url")
        delay = cmd.get("delay", 0)
        loop = bool(cmd.get("loop", False))

        if isinstance(urls, str):
            load_url(urls)
            continue

        if not isinstance(urls, list):
            log.warning("invalid url field: %r", urls)
            continue

        while True:
            for url in urls:
                with lock:
                    if version != cmd_version:
                        log.info("command superseded, stopping sequence")
                        break
                load_url(url)
                time.sleep(delay)
            else:
                if loop:
                    continue
            break

# --- MQTT callbacks ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info("mqtt connected")
        load_url("data:,Online")
        client.subscribe("spacescreen")
    else:
        log.error("mqtt connect failed: %s", rc)
        load_url("data:,Offline")

def on_disconnect(client, userdata, rc):
    log.warning("mqtt disconnected: %s", rc)
    load_url("data:,Offline")

def on_message(client, userdata, msg):
    global current_cmd, cmd_version
    try:
        data = json.loads(msg.payload.decode())
    except Exception as e:
        log.error("invalid json: %s", e)
        return

    with lock:
        current_cmd = data
        cmd_version += 1
        log.info("new command received: %s", data)

# --- signal handling ---
def cleanup_and_exit(signum, frame):
    log.info("signal received (%s), closing MQTT and tab...", signum)
    try:
        client.disconnect()
    except Exception as e:
        log.warning("error while disconnecting MQTT: %s", e)
    try:
        tab.stop()
        browser.close_tab(tab)
    except Exception as e:
        log.warning("error while closing tab: %s", e)
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, cleanup_and_exit)
    signal.signal(signal.SIGTERM, cleanup_and_exit)

    # --- start worker thread ---
    threading.Thread(target=worker, daemon=True).start()

    # --- start MQTT ---
    client = mqtt.Client()
    client.username_pw_set("username", "password") #you can comment this out if not needed
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    try:
        client.connect("ip-or.mqtt.broker.domainname", 1883)
    except Exception as e:
        log.error("mqtt connection error: %s", e)
        load_url("data:,Offline")
        raise

    client.loop_forever()

if __name__ == "__main__":
    main()
