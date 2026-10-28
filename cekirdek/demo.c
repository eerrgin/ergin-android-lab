/* © 2026 Ergin Kaplan
 * Ergin İz — Ergin İz Atölyesi — Ergin Lab
 */

#include "halka.h"

#include <stdio.h>
#include <string.h>

int main(void) {
    printf("Ergin İz halka — Ergin İz\n");
    printf("Ergin İz Atölyesi · Ergin Kaplan · Ergin Lab\n");

    ErginHalka *halka = ergin_halka_olustur(4096);
    if (!halka) {
        return 1;
    }

    int tamam = 0;
    for (int i = 0; i < 100; i++) {
        char mesaj[64];
        int n = snprintf(mesaj, sizeof mesaj, "ergin-lab-%d", i);
        if (n > 0 && ergin_halka_yaz(halka, mesaj, (uint32_t)n)) {
            tamam++;
        }
    }

    int okun = 0;
    char hedef[64];
    int m;
    while ((m = ergin_halka_oku(halka, hedef, sizeof hedef - 1)) > 0) {
        hedef[m] = 0;
        okun++;
    }
    printf("yazilan=%d okunan=%d dusen=%u\n", tamam, okun, ergin_halka_dusen(halka));
    ergin_halka_birak(halka);
    if (tamam != 100 || okun != 100) {
        return 2;
    }

    halka = ergin_halka_olustur(64);
    if (!halka) {
        return 1;
    }
    int dus = 0;
    char blok[20];
    memset(blok, 'K', sizeof blok);
    for (int i = 0; i < 20; i++) {
        if (!ergin_halka_yaz(halka, blok, 20)) {
            dus++;
        }
    }
    printf("kucuk_halka_dusen=%d sayac=%u\n", dus, ergin_halka_dusen(halka));
    ergin_halka_birak(halka);
    if (dus == 0) {
        return 3;
    }
    printf("Ergin Lab halka tamam\n");
    return 0;
}
