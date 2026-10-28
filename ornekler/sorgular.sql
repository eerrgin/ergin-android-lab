-- Ergin İz — Ergin Kaplan
-- Ergin Lab sorgu defteri. Ergin İz Atölyesi.
-- dilimler: süre ölçümü
-- sayaclar: sayaç
-- zamanlama: bağlam değişimi

SELECT anahtar, deger FROM ustbilgi ORDER BY anahtar;

SELECT ad, kat, sur, derinlik
FROM dilimler
ORDER BY sur DESC
LIMIT 10;

SELECT ad, COUNT(*) AS adet, AVG(sur) AS ortalama_ns, MAX(sur) AS en_uzun_ns
FROM dilimler
GROUP BY ad
ORDER BY en_uzun_ns DESC;

SELECT ad, COUNT(*) AS adet, MIN(deger) AS en_kucuk, MAX(deger) AS en_buyuk
FROM sayaclar
GROUP BY ad
ORDER BY ad;

SELECT ad, COUNT(*) AS adet, MAX(sonraki - onceki) AS en_buyuk_artis
FROM zamanlama
GROUP BY ad;
