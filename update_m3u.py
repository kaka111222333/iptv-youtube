from pathlib import Path
import subprocess

M3U_OUTPUT = "live_tv.m3u"
CHANNEL_FILE = "channels.txt"

def get_stream_url(youtube_url):
    try:
        r = subprocess.run(
            ["yt-dlp", "-f", "best", "-g", youtube_url],
            capture_output=True, text=True, timeout=15
        )
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None

def main():
    lines = Path(CHANNEL_FILE).read_text(encoding="utf-8").splitlines()
    valid_lines = [l for l in lines if "," in l]

    with open(M3U_OUTPUT, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")

        for line in valid_lines:
            name, url = line.split(",", 1)
            stream = get_stream_url(url)
            if not stream:
                print(f"❌ 无效: {name}")
                continue

            f.write(f'#EXTINF:-1,{name}\n')
            f.write(f"{stream}\n")
            print(f"✅ 添加: {name}")

    print("✅ live_tv.m3u 生成完成")

if __name__ == "__main__":
    main()
