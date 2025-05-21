# LAB 4 (JWT authentication bypass via JWK header injection)


1. **Burp Suite’i aç**, BApp Store’dan **JWT Editor** uzantısını yükle.

2. Tarayıcını proxy’ye ayarla.

3. `wiener` / `peter` ile giriş yap.

4. Giriş sonrası `/my-account` isteğini Burp Proxy ile yakala ve **Burp Repeater**’a gönder.

5. İstek yolunu `/admin` olarak değiştir, admin paneline erişimi test et.

6. Burp ana sekmesinde **JWT Editor > Keys** sekmesine git.

7. **New RSA Key** oluştur, `Generate` ile anahtar çifti oluştur ve kaydet.

8. Burp Repeater’da `/admin` isteğindeki JWT tokenını aç.

9. Token içindeki `sub` değerini `administrator` olarak değiştir.

10. **Attack → Embedded JWK** seçeneğini seç, yeni oluşturduğun RSA anahtarını seç.

11. JWT header’ında `jwk` parametresi gömüldüğünü gör, token otomatik imzalanır.

12. İsteği gönder, admin paneline eriştiğini doğrula.

13. Admin panelden `carlos` kullanıcısını silmek için şu isteği gönder:

```
GET /admin/delete?username=carlos
```

---

Buradaki açık, sunucunun JWT tokenlarının doğrulamasında yaptığı bir hataya dayanıyor. Normalde bir JWT token,` sunucunun sahip olduğu bir gizli anahtarla imzalanır ve sunucu gelen her tokenı bu anahtarla kontrol eder.`  Ama bu sistemde, JWT tokenının içine bir `jwk` yani "JSON Web Key" parametresi gömülmesine izin veriliyor. Bu parametre, tokenı imzalamak için hangi açık anahtarın kullanılacağını belirtiyor.

Burp Suite içinde kendi RSA anahtar çiftini oluşturuyorsun. Bu çiftin bir özel (private) anahtarı, bir de açık (public) anahtarı var. Özel anahtarla bir token imzalıyorsun, içine de kendi açık anahtarını `jwk` şeklinde tokenın header kısmına gömüyorsun. Normalde bu güvenli değildir çünkü` sunucu senin gömdüğün anahtara güvenmemeli.`  Ama bu sunucu, gelen tokenın header kısmındaki `jwk` anahtarına güveniyor ve imzanın doğruluğunu buna göre kontrol ediyor.

Sen de bunu kullanarak token içindeki kullanıcı bilgisini (sub) "administrator" olarak değiştiriyorsun, kendi oluşturduğun özel anahtarla imzalıyorsun ve içine kendi açık anahtarını gömüyorsun. Sonra bu sahte ama geçerli gözüken tokenı sunucuya gönderiyorsun. Sunucu da bu tokenı kabul ediyor, çünkü imzayı kontrol ederken senin içine gömdüğün anahtara güveniyor. Bu sayede admin yetkisi kazanıyorsun.
