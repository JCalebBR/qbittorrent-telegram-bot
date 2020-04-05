import qbittorrentapi
import json

def queue(status='downloading'):
    AUTH = "auth.json"

    with open(AUTH,"r") as f:
        AUTH = json.loads(f.read())

    client = qbittorrentapi.Client(host=AUTH["host"], port=AUTH["port"])

    try:
        client.auth_log_in()
    except qbittorrentapi.LoginFailed as ex:
        print(ex)

    results = []

    for torrent in client.torrents_info(status_filter=status):
        d_size, d_suffix = check_size(torrent.downloaded)
        t_size, t_suffix = check_size(torrent.total_size)
        s_size, s_suffix = check_size(torrent.dlspeed)
        time = check_time(torrent.eta)
        progress = f"{round(torrent.progress*100, 1)}%"

        results.append(f"""
        {torrent.name} 
        {progress} 
        {d_size}{d_suffix} of {t_size}{t_suffix} 
        {s_size}{s_suffix}/s 
        {time}""")

    return results

def add():
    pass

def check_size(size, precision=2):
    if size / 1024 < 1:
        return round(size, precision), "B"
    elif size / pow(1024,2) < 1:
        return round(size / pow(1024, 1), precision), "KB"
    elif size / pow(1024,3) < 1:
        return round(size / pow(1024, 2), precision), "MB"
    elif size / pow(1024, 4) < 1:
        return round(size / pow(1024, 3), precision), "GB"
    elif size / pow(1024, 5) < 1:
        return round(size / pow(1024, 4), precision), "TB"

def check_time(time):
    if time / 60 < 1:
        return f"{time}s"
    elif time / pow(60, 2) < 1:
        seconds = time % 60
        minutes = (time - seconds) / 60
        return f"{minutes:.0f}m"
    elif time / pow(60, 3) < 1:
        minutes = time % 3600
        hours = (time - minutes) / 3600
        seconds = minutes % 60
        minutes = (minutes - seconds) / 60
        return f"{hours:.0f}h {minutes:.0f}m"
