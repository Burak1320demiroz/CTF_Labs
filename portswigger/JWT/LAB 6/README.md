# LAB 6 (JWT authentication bypass via kid header path traversal)

Elbette, bu JWT `kid` header path traversal zaafiyetini adım adım şu şekilde uygulayabilirsin:

---

### JWT authentication bypass via **kid header path traversal** — Adım Adım

#### 1. **Hazırlık ve Giriş**

1. Burp Suite’i aç, BApp Store’dan **JWT Editor** uzantısını yükle.
2. Tarayıcını proxy'ye ayarla.
3. `wiener` / `peter` ile laboratuvara giriş yap.
4. Giriş sonrası `/my-account` isteğini yakala ve **Burp Repeater**’a gönder.

---

#### 2. **Admin Paneline Erişimi Test Et**

5. Repeater’daki isteğin yolunu `/admin` olarak değiştir.
6. İsteği gönder, admin paneline sadece `administrator` kullanıcısının erişebildiğini gör.

---

#### 3. **Sahte Anahtar (Null Byte) Oluştur**

7. Burp ana sekmesinde **JWT Editor > Keys** kısmına git.
8. **New Symmetric Key** seçeneğiyle yeni bir simetrik anahtar oluştur.
9. `Generate` butonuna basarak key oluştur.
10. `k` değerini şu şekilde değiştir: `AA==` → bu Base64 ile `null byte` (`\x00`) karşılığıdır.
11. `OK` diyerek anahtarı kaydet.

---

#### 4. **JWT Token’ı Değiştir ve İmzala**

12. Repeater’daki `/admin` isteğinde, JWT Editor sekmesine geç.
13. Header içindeki `kid` alanını şu şekilde değiştir:

```
../../../../../../../dev/null
```

14. Payload (yük) kısmında `sub` değerini `"administrator"` olarak değiştir.

15. Sayfanın altındaki **Sign** butonuna tıkla, biraz önce oluşturduğun **null byte içeren simetrik key**’i seç.

16. **Don’t modify header** seçeneği işaretli olsun, sonra **OK**’e tıkla.

17. Token sahte ama geçerli imza ile yeniden oluşturulmuş olacak.

---

#### 5. **Admin Paneline Erişim ve Kullanıcıyı Silme**

18. İsteği gönder, admin paneline eriştiğini gör.
19. Yanıtta, `carlos` kullanıcısını silmek için verilen URL’yi bul:

```
GET /admin/delete?username=carlos
```

---

Bu laboratuvarda, JWT doğrulamasında kullanılan `kid` (Key ID) parametresine karşı yapılan path traversal saldırısı ile admin paneline erişim sağlıyoruz. Sistem, JWT imzasını doğrularken `kid` değerini dosya sistemi üzerinde bir dosya olarak arıyor ve bu dosyanın içeriğini imzalama anahtarı olarak kullanıyor. Ancak, bu işlem sırasında `kid` parametresine yapılan dizin geçişlerini (örneğin `../../`) filtrelemediği için, saldırganlar sistemdeki herhangi bir dosyayı anahtar olarak kullandırabiliyor. Biz de bu zafiyeti kullanarak `kid` parametresini `/dev/null` dosyasına yönlendiriyoruz. Ardından Burp Suite üzerinden JWT Editor eklentisiyle bir simetrik anahtar oluşturuyor ve bu anahtarın içeriğini `null byte` (Base64 karşılığı `AA==`) olarak ayarlıyoruz. Daha sonra JWT'nin payload kısmındaki `"sub"` alanını `"administrator"` olarak değiştiriyoruz ve token'ı bu null byte ile imzalıyoruz. Çünkü `/dev/null` dosyasının içeriği boş olduğu için sunucu bu imzayı geçerli kabul ediyor. Son olarak bu sahte ama geçerli imzalanmış token ile `/admin` sayfasına erişiyoruz. Admin panelde yer alan `carlos` kullanıcısını silme isteğini göndererek laboratuvarı başarıyla tamamlıyoruz. Bu açık, sunucunun `kid` parametresini işlerken path traversal saldırılarına karşı önlem almamasından kaynaklanıyor.