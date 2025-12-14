#!/usr/bin/env python3
"""
QR Code Generator for ReviewFlow Dashboard
Generates a QR code for easy mobile access to the dashboard
"""
import qrcode
import socket
import os

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Create a socket to find local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

def generate_qr_code():
    """Generate and display QR code for dashboard access"""

    # Get local IP
    local_ip = get_local_ip()

    # Dashboard URL
    dashboard_url = f"http://{local_ip}:8000/dashboard/?token=demo-token-123"

    print("\n" + "="*70)
    print("🎯 REVIEWFLOW - MOBILE ACCESS QR CODE")
    print("="*70)
    print()

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(dashboard_url)
    qr.make(fit=True)

    # Print ASCII QR code to terminal
    qr.print_ascii(invert=True)

    print()
    print("="*70)
    print("📱 SCAN WITH YOUR MOBILE CAMERA")
    print("="*70)
    print()
    print(f"📍 Local IP:      {local_ip}")
    print(f"🌐 Dashboard URL: {dashboard_url}")
    print()
    print("="*70)
    print()
    print("💡 INSTRUCTIONS:")
    print("   1. Make sure your mobile is on the SAME WiFi network")
    print("   2. Open your mobile camera app")
    print("   3. Point it at the QR code above")
    print("   4. Tap the notification that appears")
    print("   5. Enjoy the dashboard on your mobile! 📱✨")
    print()
    print("="*70)
    print()

    # Also save as image
    try:
        img = qr.make_image(fill_color="black", back_color="white")
        qr_file = "data/reviewflow_qr_code.png"
        img.save(qr_file)
        print(f"✅ QR Code image saved as: {qr_file}")
        print(f"   (You can open this image to display on a larger screen)")
        print()
    except Exception as e:
        print(f"⚠️  Could not save QR code image: {e}")
        print()

if __name__ == "__main__":
    generate_qr_code()
