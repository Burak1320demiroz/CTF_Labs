# LAB 5 (JWT authentication bypass via jku header injection)

## **Hazırlık Aşaması**

1. **Burp Suite’i aç.**
2. **BApp Store’dan `JWT Editor` eklentisini yükle.**
3. Tarayıcını Burp proxy’ye yönlendir.
4. Lab sitesine git, `wiener:peter` ile giriş yap.
5. Giriş yaptıktan sonra `/my-account` isteğini yakala.
6. Bu isteği **Burp Repeater**'a gönder.

---

## **Admin Paneline Erişimi Deneme**

7. Repeater’da yolunu `/admin` yap.
8. Gönder, **403 yetkisiz** dönüyorsa bu normal. Çünkü admin değilsin.

---

## **Kendi RSA Anahtarını Oluştur**

9. Burp ana sekmesinde **JWT Editor > Keys** kısmına git.
10. **New RSA Key** butonuna bas.
11. `Generate` diyerek key oluştur, **Tamam** de.

---

## **Kötü Amaçlı JWK Seti Oluştur**

12. Lab sayfasında **exploit server**’a git.
13. Sayfanın body kısmını şu şekilde yap:

```json
{
  "keys": []
}
```

14. JWT Editor > Keys kısmına geri dön.
15. Oluşturduğun anahtarın üzerine sağ tıkla → `Copy public key as JWK`.
16. Exploit server’daki `"keys": []` kısmının içine bu key’i yapıştır.
17. Save et. Örnek:

```json
{
  "keys": [
    {
      "kty": "RSA",
      "e": "AQAB",
      "kid": "abc123",
      "n": "base64-uzun-anahtar"
    }
  ]
}
```

---

## **JWT Token'ı Sahteleme**

18. Repeater’daki `/admin` isteğine geri dön.
19. JWT token’ı **JWT Editor** sekmesinde aç.
20. **Header** kısmına şu iki şeyi ekle:

* `kid`: JWK içindeki `kid`
* `jku`: Exploit server’daki JWK seti URL’si

Örnek header:

```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "abc123",
  "jku": "https://exploit-0a9900a7033c.exploit-server.net/jwk.json"
}
```

21. Payload kısmındaki `"sub"` değerini `"administrator"` yap.
22. Altta **Sign** butonuna tıkla → oluşturduğun RSA anahtarıyla imzala.
23. Token otomatik imzalanacak.

---

## **İsteği Gönder ve Admin Paneline Gir**

24. İsteği gönder.
25. Artık `/admin` sayfasına erişebiliyor olmalısın.

---

## **Carlos’u Silerek Lab’ı Bitir**

26. Admin panelde `GET /admin/delete?username=carlos` isteğini gönder.
27. Lab başarıyla tamamlanır 

---

Bu laboratuvarda, JWT doğrulamasında yapılan bir güvenlik açığını kullanarak admin paneline erişim sağlıyoruz. Sistem, JWT tokenlarının doğruluğunu kontrol ederken `jku` (JSON Key URL) başlığındaki adrese gidip token’ı doğrulamak için gereken public key’i buradan alıyor. Ancak sunucu, bu URL’nin güvenilir bir domainden gelip gelmediğini kontrol etmiyor. Bu da saldırganın kendi oluşturduğu sahte bir anahtar çiftinin public key’ini barındıran bir JWK seti yükleyerek, imzası geçerli görünen sahte bir JWT üretmesine olanak sağlıyor.

İlk olarak Burp Suite’in BApp Store’undan “JWT Editor” eklentisini yükleyip, kendi hesabımızla lab’a giriş yapıyoruz. Ardından `/my-account` isteğini yakalayıp Burp Repeater’a gönderiyor ve bu isteği `/admin` olarak değiştirip admin paneline erişmeye çalışıyoruz ama yetkimiz olmadığı için reddediliyoruz. Buradan sonra Burp'taki JWT Editor sekmesinde bir RSA anahtar çifti oluşturuyoruz. Daha sonra exploit server’a giderek, içine bu oluşturduğumuz public key’i gömeceğimiz boş bir JWK seti hazırlıyoruz. Bu seti JSON formatında exploit server’a yüklüyoruz. Şimdi elimizde hem private key (imzalama için) hem de public key’i içeren bir JWK adresi var.

Sonrasında tekrar Burp Repeater’daki `/admin` isteğine dönüp JWT token’ı JWT Editor sekmesinde açıyoruz. Token’ın header kısmına `kid` olarak kendi key'imizin ID’sini, `jku` olarak da exploit server’daki JWK adresini yazıyoruz. Payload (yük) kısmındaki `"sub"` alanını `"administrator"` olarak değiştiriyoruz. Ardından bu sahte token’ı oluşturduğumuz private key ile imzalıyoruz. Bu sahte ama imzası geçerli görünen token ile isteği gönderdiğimizde artık admin paneline erişim sağlamış oluyoruz. Son olarak admin paneldeki `carlos` kullanıcısını silen isteği göndererek laboratuvarı başarıyla tamamlıyoruz. Bu açık, sunucunun dış kaynaktan gelen public key’lere körü körüne güvenmesi nedeniyle oluşur.
