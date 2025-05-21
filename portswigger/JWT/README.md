# JWT

### Portswigger Labları Cözümleri

- LAB 1 (JWT Authentication Bypass via Unverified Signature)
- LAB 2 (JWT authentication bypass via flawed signature verification)
- LAB 3 (JWT authentication bypass via weak signing key)
- LAB 4 (JWT authentication bypass via JWK header injection)
- LAB 5 (JWT authentication bypass via jku header injection)
- LAB 6 (JWT authentication bypass via kid header path traversal)
- LAB 7 (JWT authentication bypass via algorithm confusion)
- LAB 8 (JWT authentication bypass via algorithm confusion with no exposed key)

--- 

### jku-jwk warkı ==> 
İki saldırı türü benzer görünse de temel fark, sahte anahtarın **nerede barındırıldığıdır**. `jku` saldırısında, saldırgan kendi **JWK setini dış bir sunucuda (örneğin exploit server)** barındırır ve token’ın header kısmına `jku` parametresi ekleyerek sunucunun bu adresten public key’i almasını sağlar. Bu, **dış kaynağa güven sorununa** dayanır. Öte yandan `jwk` saldırısında, saldırgan **JWK’yı doğrudan JWT token’ın içine gömer** (header içine `jwk` parametresi eklenir). Sunucu bu gömülü anahtara güvenip imzayı buna göre doğrular. Yani `jku` saldırısında dış bir URL’ye başvuru yapılırken, `jwk` saldırısında tüm bilgi token içinde taşınır. (LAB 4-5 )

--- 

JWT'deki `kid` (Key ID) parametresi, imzayı doğrulamak için hangi anahtarın kullanılacağını belirtir. Bu laboratuvarda sunucu, `kid` içindeki değeri dosya sisteminden anahtar dosyasının yolu olarak alıyor. Biz de bu parametreyi `../../../../../../../dev/null` olarak değiştiriyoruz.

`/dev/null`, Linux sistemlerinde boş bir dosya gibi çalışır; içine ne yazarsan yaz yok olur, okunduğunda da boş döner. Yani içeriği "boş"tur.

Sunucu bu dosyayı anahtar olarak kullandığında, aslında boş bir içerikle (yani null byte gibi) imzayı kontrol eder. Biz de JWT token'ı aynı şekilde (null byte ile) imzalarsak, sunucu token'ı geçerli sayar. Bu sayede doğrulama mekanizması kandırılır. (LAB 6)

--- 

