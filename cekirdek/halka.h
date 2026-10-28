/* © 2026 Ergin Kaplan
 * Ergin Android Lab — Ergin Android Atölyesi — Ergin Lab
 *
 * Tek üretici, tek tüketici halka tamponu.
 * Sayaçlar stdatomic serbest bırakma / edinme sırası kullanır.
 */
#ifndef ERGIN_HALKA_H
#define ERGIN_HALKA_H

#include <stdbool.h>
#include <stdint.h>

typedef struct ErginHalka ErginHalka;

ErginHalka *ergin_halka_olustur(uint32_t kapasite);
void ergin_halka_birak(ErginHalka *halka);
bool ergin_halka_yaz(ErginHalka *halka, const void *veri, uint32_t boyut);
int ergin_halka_oku(ErginHalka *halka, void *hedef, uint32_t hedef_kap);
uint32_t ergin_halka_dusen(const ErginHalka *halka);

#endif
