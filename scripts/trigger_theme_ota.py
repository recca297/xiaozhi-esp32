#!/usr/bin/env python3
"""
Trigger Theme OTA Upgrade on XiaoZhi ESP32-S3
Usage:
    python scripts/trigger_theme_ota.py --theme otto
    python scripts/trigger_theme_ota.py --theme dbrobot
    python scripts/trigger_theme_ota.py --device 98:c3:77:a1:a7:f4 --theme otto
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

SERVER_IP = "192.168.1.50"
SERVER_HTTP_PORT = 8002
DEFAULT_DEVICE_ID = "98:c3:77:a1:a7:f4"

THEMES = {
    "otto": {
        "name": "Otto Robot",
        "file": "assets_otto.bin",
        "size": "1.22 MB",
        "emojis": 21
    },
    "dbrobot": {
        "name": "DB-Robot (Default Component)",
        "file": "assets_dbrobot.bin",
        "size": "2.03 MB",
        "emojis": 26
    }
}

def call_mcp_tool(device_id, tool_name, args, token=None):
    url = f"http://{SERVER_IP}:{SERVER_HTTP_PORT}/xiaozhi/device/tools/call/{device_id}"
    payload = json.dumps({"name": tool_name, "arguments": args}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        return {"code": e.code, "msg": f"HTTP Error {e.code}: {err_body}"}
    except Exception as e:
        return {"code": -1, "msg": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Kích hoạt nạp OTA Theme cho XiaoZhi ESP32-S3")
    parser.add_argument("--theme", choices=["otto", "dbrobot"], required=True, help="Theme cần nạp: 'otto' hoặc 'dbrobot'")
    parser.add_argument("--device", default=DEFAULT_DEVICE_ID, help=f"MAC / Device ID (mặc định: {DEFAULT_DEVICE_ID})")
    parser.add_argument("--token", default="70add36c1dc0fe2ff625333bf7ece1f7", help="Auth token của tài khoản quản trị")
    args = parser.parse_args()

    theme_info = THEMES[args.theme]
    download_url = f"http://{SERVER_IP}:{SERVER_HTTP_PORT}/{theme_info['file']}"

    print("=" * 60)
    print(f"🚀 XIAOZHI THEME OTA TRIGGER")
    print(f"Theme được chọn : {theme_info['name']} ({theme_info['emojis']} emojis, {theme_info['size']})")
    print(f"Thiết bị        : {args.device}")
    print(f"URL tải về      : {download_url}")
    print("=" * 60)

    # 1. Kiểm tra trạng thái thiết bị
    print("\n[1/3] Đang kiểm tra trạng thái thiết bị...")
    status_res = call_mcp_tool(args.device, "self.get_device_status", {}, args.token)
    if status_res.get("code") != 0:
        print(f"⚠️ Cảnh báo thiết bị chưa online: {status_res.get('msg')}")
        print("💡 Hãy đảm bảo mạch ESP32 đã bật nguồn và kết nối Wi-Fi.")
        choice = input("Bạn có muốn tiếp tục gửi lệnh OTA không? (y/N): ").strip().lower()
        if choice != "y":
            sys.exit(1)
    else:
        print("✅ Thiết bị đang Online và sẵn sàng!")

    # 2. Cài đặt download URL vào NVS
    print(f"\n[2/3] Đang gửi URL tải về qua MCP: self.assets.set_download_url...")
    set_res = call_mcp_tool(args.device, "self.assets.set_download_url", {"url": download_url}, args.token)
    if set_res.get("code") != 0:
        print(f"❌ Lỗi cài đặt download URL: {set_res.get('msg')}")
        sys.exit(1)
    print("✅ Đã ghi nhận download_url vào bộ nhớ ESP32 thành công!")

    # 3. Gửi lệnh Reboot để thiết bị tải và ghi Flash
    print(f"\n[3/3] Đang gửi lệnh khởi động lại: self.reboot...")
    reboot_res = call_mcp_tool(args.device, "self.reboot", {}, args.token)
    print("✅ Đã gửi lệnh Reboot!")

    print("\n" + "=" * 60)
    print("🎉 QUÁ TRÌNH NẠP OTA ĐÃ ĐƯỢC KÍCH HOẠT THÀNH CÔNG!")
    print("📺 Hãy nhìn vào màn hình LCD của ESP32:")
    print("   1. Thiết bị đang khởi động lại.")
    print("   2. Màn hình sẽ hiện icon download và thanh phần trăm % tải về.")
    print("   3. Sau khi ghi Flash phân vùng 0x800000 xong, ESP32 sẽ tự nạp theme mới!")
    print("=" * 60)

if __name__ == "__main__":
    main()

