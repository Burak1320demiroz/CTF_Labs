# LAB 2 (JWT authentication bypass via flawed signature verification)

## Burp Suite ile Çözüm Adımları

### 1. **Giriş yap (`wiener:peter`)**

* Tarayıcında Burp açıkken şu sayfaya git:
  `https://<lab-url>/login`
* Kullanıcı adı: `wiener`
  Şifre: `peter`

---

### 2. **JWT Token’ını Bul**

* Giriş yaptıktan sonra Burp’ta **HTTP History** sekmesine git.
* `GET /my-account` isteğini seç.
* Sağ tarafta **Cookies** bölümüne bak: `session` çerezi JWT formatındadır:
  Örn: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

---

### 3. **JWT’yi İncele ve Değiştir**

1. JWT'yi [jwt.io](https://jwt.io) adresinde aç veya Burp'taki **Inspector / Decoder** panelini kullan.
2. **Payload** kısmındaki `"sub"` değerini `"administrator"` olarak değiştir.
3. **Header** kısmındaki `"alg"` değerini `"none"` olarak değiştir.
4. Yeni JWT şöyle görünmeli:

   ```
   header.payload.
   ```

   > Sonunda imza **yok** ama iki nokta üst üste (.) bırakılmalı.

---

### 4. **JWT'yi Test Et**

* `GET /admin` isteği oluştur.
* Burp'ta **Repeater**'a geç, yeni bir istek oluştur:

  ```
  GET /admin HTTP/1.1
  Host: <lab-host>
  Cookie: session=<yeni JWT>
  ```
* Gönder’e tıkla. Eğer başarılıysa admin paneli açılacaktır.

---

### 5. **Carlos’u Sil**

* Yanıttaki HTML'de şu URL'yi bul:
  `/admin/delete?username=carlos`
* Yeni bir `GET` isteği oluştur:

  ```
  GET /admin/delete?username=carlos HTTP/1.1
  Host: <lab-host>
  Cookie: session=<yeni JWT>
  ```
* Bu isteği gönder ve “Congratulations” mesajını gör.

---

## Özet:

* Sunucu `alg: none` olan JWT'leri imzasız olarak kabul ediyor.
* Sen de bu sayede token’ı elle değiştirip admin oluyorsun.
* Burp ile bu değişiklikleri manuel olarak yapabilir, isteği Repeater’da test edebilirsin.

---

## Python Script ile Çözüm Adımları

Bu script, PortSwigger Web Security Academy'deki **"JWT authentication bypass via flawed signature verification"** adlı güvenlik zafiyetine sahip bir laboratuvarı çözmek için geliştirilmiştir.

### 📌 Açıklama

Bu zafiyet, sunucunun imzasız JWT'leri (`alg: none`) kabul etmesi sonucu oluşur. Bu durum, kötü niyetli bir kullanıcının kendi kimliğini kolayca **administrator** olarak değiştirmesine ve sistem üzerinde tam yetki elde etmesine olanak tanır.

### ⚙️ Script Ne Yapar?

1. **Giriş yapar**
   `wiener:peter` kullanıcı adı ve şifresiyle uygulamaya oturum açılır.

2. **JWT token’ı elde eder**
   `/my-account` sayfası çağrılarak `session` çerezi içerisindeki JWT alınır.

3. **JWT yeniden oluşturulur**

   * JWT'nin header kısmı `{"alg": "none", "typ": "JWT"}` olarak değiştirilir.
   * Payload kısmındaki `"sub"` değeri `"administrator"` olarak güncellenir.
   * İmza kısmı tamamen kaldırılır (`header.payload.` şeklinde oluşturulur).

4. **Admin paneline erişim sağlanır**
   Oluşturulan sahte JWT, admin yetkisiyle `/admin` sayfasına gönderilir.

5. **Carlos adlı kullanıcı silinir**
   `/admin/delete?username=carlos` endpoint'i çağrılarak hedef kullanıcı sistemden kaldırılır.