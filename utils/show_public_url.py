#!/usr/bin/env python3
"""
Display public URL for ReviewFlow Dashboard
Shows the public URL with QR code for easy mobile access
"""

import re
import subprocess
import sys
import qrcode
from io import BytesIO

def get_public_url():
    """Extract public URL from localhost.run log"""
    try:
        with open('localhostrun.log', 'r') as f:
            content = f.read()
            # Look for the URL pattern
            match = re.search(r'(https://[a-z0-9]+\.lhr\.life)', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        return None
    return None

def generate_qr_terminal(url):
    """Generate QR code for terminal display"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Print QR code in terminal
    qr.print_ascii(invert=True)

def save_qr_image(url, filename="data/public_url_qr.png"):
    """Save QR code as image file"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    return filename

def main():
    """Display public URL information"""
    print("\n" + "="*70)
    print("🌐  REVIEWFLOW DASHBOARD - PUBLIC ACCESS")
    print("="*70 + "\n")

    url = get_public_url()

    if not url:
        print("❌ Could not find public URL")
        print("   Make sure localhost.run tunnel is running")
        print("\n💡 Start tunnel with:")
        print("   ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \\")
        print("       -R 80:localhost:8000 nokey@localhost.run\n")
        sys.exit(1)

    login_url = f"{url}/dashboard/login"
    dashboard_url = url

    print(f"✅ Your dashboard is publicly accessible!\n")
    print(f"📱 Login Page:")
    print(f"   {login_url}\n")
    print(f"🔐 Credentials:")
    print(f"   Username: shubham-dev")
    print(f"   Password: yourlaptop\n")
    print(f"📊 Dashboard:")
    print(f"   {dashboard_url}/dashboard/\n")

    print("="*70)
    print("📲  SCAN QR CODE TO OPEN ON MOBILE")
    print("="*70 + "\n")

    # Generate and display QR code
    generate_qr_terminal(login_url)

    # Save QR code image
    try:
        qr_file = save_qr_image(login_url)
        print(f"\n💾 QR Code saved: {qr_file}\n")
    except Exception as e:
        print(f"\n⚠️  Could not save QR code image: {e}\n")

    print("="*70)
    print("💡  FEATURES")
    print("="*70)
    print("""
✅ Login with username/password authentication
✅ "Forgot Password?" feature (requires SMTP config)
✅ View PR reviews and AI analysis
✅ Approve/Close PRs directly from dashboard
✅ Real-time GitHub integration
✅ Beautiful responsive UI
✅ Secure session management
    """)

    print("="*70)
    print("⚠️   IMPORTANT NOTES")
    print("="*70)
    print("""
• This URL is temporary and changes on each tunnel restart
• Tunnel will stay active as long as the SSH connection is alive
• If tunnel disconnects, run: ./scripts/start_public_tunnel.sh
• For permanent URLs, sign up at https://localhost.run/docs/
• Keep the server and tunnel running in background
    """)

    print("="*70)
    print("🔧  MANAGEMENT COMMANDS")
    print("="*70)
    print("""
Check tunnel status:  ps aux | grep "localhost.run"
Kill tunnel:          pkill -f "localhost.run"
Restart tunnel:       ./scripts/start_public_tunnel.sh
View server logs:     tail -f server.log
Stop all services:    ./stop.sh
    """)

    print("="*70)
    print(f"🎉  Dashboard is live at: {login_url}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
