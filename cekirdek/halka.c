/* © 2026 Ergin Kaplan
 * Ergin Android Lab — Ergin Android Atölyesi — Ergin Lab
 */

#include "halka.h"

#include <stdatomic.h>
#include <stdlib.h>
#include <string.h>

struct ErginHalka {
    uint32_t capacity;
    atomic_uint write_pos;
    atomic_uint read_pos;
    atomic_uint dropped;
    uint32_t magic;
    uint8_t *data;
};

static void koy(ErginHalka *halka, uint32_t konum, const void *kaynak, uint32_t boy) {
    uint32_t cap = halka->capacity;
    uint32_t i = konum % cap;
    const uint8_t *s = kaynak;
    uint32_t ilk = cap - i;
    if (ilk > boy) {
        ilk = boy;
    }
    memcpy(halka->data + i, s, ilk);
    if (ilk < boy) {
        memcpy(halka->data, s + ilk, boy - ilk);
    }
}

static void al(const ErginHalka *halka, uint32_t konum, void *hedef, uint32_t boy) {
    uint32_t cap = halka->capacity;
    uint32_t i = konum % cap;
    uint8_t *d = hedef;
    uint32_t ilk = cap - i;
    if (ilk > boy) {
        ilk = boy;
    }
    memcpy(d, halka->data + i, ilk);
    if (ilk < boy) {
        memcpy(d + ilk, halka->data, boy - ilk);
    }
}

ErginHalka *ergin_halka_olustur(uint32_t kapasite) {
    if (kapasite < 64 || (kapasite & (kapasite - 1)) != 0) {
        return NULL;
    }
    ErginHalka *halka = calloc(1, sizeof(*halka));
    if (!halka) {
        return NULL;
    }
    halka->data = calloc(1, kapasite);
    if (!halka->data) {
        free(halka);
        return NULL;
    }
    halka->capacity = kapasite;
    halka->magic = 0x4B4C4845u; /* Ergin Lab halka */
    atomic_init(&halka->write_pos, 0);
    atomic_init(&halka->read_pos, 0);
    atomic_init(&halka->dropped, 0);
    return halka;
}

void ergin_halka_birak(ErginHalka *halka) {
    if (!halka) {
        return;
    }
    free(halka->data);
    free(halka);
}

bool ergin_halka_yaz(ErginHalka *halka, const void *veri, uint32_t boyut) {
    uint32_t cap = halka->capacity;
    uint32_t need = boyut + 4;
    if (boyut == 0 || need > cap) {
        atomic_fetch_add_explicit(&halka->dropped, 1, memory_order_relaxed);
        return false;
    }
    uint32_t w = atomic_load_explicit(&halka->write_pos, memory_order_relaxed);
    uint32_t r = atomic_load_explicit(&halka->read_pos, memory_order_acquire);
    if ((w - r) + need > cap) {
        atomic_fetch_add_explicit(&halka->dropped, 1, memory_order_relaxed);
        return false;
    }
    koy(halka, w, &boyut, 4);
    koy(halka, w + 4, veri, boyut);
    atomic_store_explicit(&halka->write_pos, w + need, memory_order_release);
    return true;
}

int ergin_halka_oku(ErginHalka *halka, void *hedef, uint32_t hedef_kap) {
    uint32_t w = atomic_load_explicit(&halka->write_pos, memory_order_acquire);
    uint32_t r = atomic_load_explicit(&halka->read_pos, memory_order_relaxed);
    if (w == r) {
        return 0;
    }
    if ((w - r) < 4) {
        return -1;
    }
    uint32_t boy = 0;
    al(halka, r, &boy, 4);
    if (boy == 0 || boy > halka->capacity || (w - r) < 4 + boy) {
        return -1;
    }
    if (boy > hedef_kap) {
        return -1;
    }
    al(halka, r + 4, hedef, boy);
    atomic_store_explicit(&halka->read_pos, r + 4 + boy, memory_order_release);
    return (int)boy;
}

uint32_t ergin_halka_dusen(const ErginHalka *halka) {
    return atomic_load_explicit(&halka->dropped, memory_order_relaxed);
}
