# LAB 7 (JWT authentication bypass via algorithm confusion)

Bu labda JWT token’lar RSA ile imzalanıyor ama uygulamada algoritma karışıklığı (algorithm confusion) zafiyeti var. Yani sunucu, `alg` parametresine göre doğru kontrolü yapmıyor.

Öncelikle labda kendi hesabınla giriş yapıp `/my-account` isteğini Burp Repeater’a gönderiyorsun. Oradan yolu `/admin` olarak değiştirip admin paneline erişmeye çalışıyorsun ama erişim reddediliyor.

Sonra tarayıcıda `/jwks.json` adresine gidip sunucunun herkese açık **public key**’ini JWK formatında alıyorsun. Bu anahtarı Burp JWT Editor’da **New RSA Key** seçeneğiyle kaydediyorsun. Ardından oluşturduğun bu anahtara sağ tıklayıp **Copy Public Key as PEM** yapıyorsun.

PEM formatındaki public key’i Burp’un Decoder sekmesinde Base64’e çevirip kopyalıyorsun. Sonra JWT Editor’da yeni bir **Symmetric Key (HS256)** oluşturup `k` değerine bu Base64 kodunu yapıştırıyorsun.

Tekrar Repeater’daki `/admin` isteğine dönüp JWT token’ın header kısmındaki `alg` parametresini `HS256` yapıyorsun, payload’daki `sub` değerini `administrator` olarak değiştiriyorsun. Token’ı az önce oluşturduğun symmetric key ile imzalıyorsun.

Bu sahte ama geçerli token’la isteği gönderdiğinde admin paneline erişiyorsun. Son olarak da `/admin/delete?username=carlos` isteğiyle carlos kullanıcısını silip labı tamamlıyorsun.

Özetle, labda sunucu RSA imzası beklerken, sen public key’i gizli anahtar gibi kullanıp HS256 ile imzalayarak sistemi kandırıyorsun.
