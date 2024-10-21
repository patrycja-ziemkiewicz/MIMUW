#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAKS 1000000000000000000
#define ZMIENNE 26

typedef unsigned long long u_llong;

typedef struct instrukcje {
    int zmienna0;
    int tablica[ZMIENNE];
    int poziom;
    bool czy_optymalna;
    struct instrukcje *adres;
    struct instrukcje *next;
}instrukcje_;

void printf_(u_llong *tab, int dlugosc[], int zmienna) {
    printf("%llu", tab[dlugosc[zmienna] - 1]);
    for (int i = dlugosc[zmienna] - 2; i >= 0; i--)
        printf("%018llu", tab[i]);
    printf("\n");
}

void free_(instrukcje_ *poczatek_instrukcji) {
    instrukcje_ *temp;
    while(poczatek_instrukcji != NULL) {
        temp = poczatek_instrukcji;
        poczatek_instrukcji = poczatek_instrukcji -> next;
        free(temp);
    }
}

void zwiekszenie(u_llong **tablica, int dlugosc[], int zmienna) {
    u_llong *tab = *tablica;
    dlugosc[zmienna]++;
    tab = realloc(tab, (size_t) dlugosc[zmienna] * sizeof *tab);
    assert(tab != NULL);
    tab[dlugosc[zmienna] - 1] = 1;
    *tablica = tab;
}

instrukcje_* wczytaj_instrukcje(void) {
    int poziom = 0, optymalizacja = 0;
    instrukcje_ *poczatek, *koniec, *atrapa = (instrukcje_ *)malloc(sizeof(instrukcje_));
    atrapa->next = NULL;
    koniec = atrapa;
    do {
        int a = getchar();
        instrukcje_ *temp = (instrukcje_ *)malloc(sizeof(instrukcje_));
        temp->next = NULL;
        temp->czy_optymalna = false;
        temp->zmienna0 = -1;
        for (int i = 0; i < ZMIENNE; i++)
            temp->tablica[i] = 0;
        if (a == (int) '(') {
            optymalizacja = 1;
            poziom++;
            temp->zmienna0 = (int) getchar() - 'a';
            a = getchar();
        }
        temp->poziom = poziom;
        while (a != (int) '(' && a != (int) ')') {
            temp->tablica[(int) a - 'a']++;
            a = getchar();
        }
        if (a == (int) ')') {
            if (optymalizacja == 1) {
                temp->czy_optymalna = true;
                temp->poziom--; // Instrukcje optymalne traktuje jakby były na niższym poziomie, gdyż będę je wykonywać na poziomie niższym niż ten, który im odpowiada.
            }
            optymalizacja = 0;
            while (a == (int) ')') { // By uniknąć pustych instrukcji, wczytuje wszystkie nawiasy końcowe występujące bezpośrednio po sobie.
                poziom--;
                a = getchar();
            }
        }
        ungetc(a, stdin);
        koniec->next = temp;
        koniec = temp;
    } while (poziom != 0);
    poczatek = atrapa->next;
    free(atrapa);
    return poczatek;
}

void ADD(u_llong **tablica1, u_llong *tablica2,
                        int dlugosc[], int zmienna1, int zmienna2) {
    u_llong suma, temp, *tab1 = *tablica1;
    unsigned int mem = 0;
    if (dlugosc[zmienna1] < dlugosc[zmienna2]) {
        tab1 = realloc(tab1, (size_t) dlugosc[zmienna2] * sizeof *tab1);
        assert(tab1 != NULL);
        for (int i = dlugosc[zmienna1]; i < dlugosc[zmienna2]; i++)
            tab1[i] = 0;
        dlugosc[zmienna1] = dlugosc[zmienna2];
    }
    for (int i = 0; i < dlugosc[zmienna1]; i++) {
        if (dlugosc[zmienna2] - 1 < i)
            temp = 0;
        else
            temp = tablica2[i];
        suma = MAKS - temp - mem;
        if (suma > tab1[i]) {
            tab1[i] += temp + mem;
            mem = 0;
        }
        else {
            tab1[i] -= suma;
            mem = 1;
        }
    }
    if (mem ==  1)
        zwiekszenie(&tab1, dlugosc, zmienna1);
    *tablica1 = tab1;
}

void INC(u_llong **tablica, int dlugosc[], int zmienna) {
    int  mem = 1;
    u_llong *tab = *tablica;
    for (int i = 0; i < dlugosc[zmienna]; i++) {
        if (MAKS - 1 > tab[i]) {
            tab[i]++;
            mem = 0;
            break;
        }
        else {
            tab[i] = 0;
        }
    }
    if (mem == 1)
        zwiekszenie(&tab, dlugosc, zmienna);
    *tablica = tab;
}

void DC(u_llong **tablica, int dlugosc[], int zmienna) {
    int mem = 1;
    u_llong *tab = *tablica;
    for (int i = 0; i < dlugosc[zmienna] - 1; i++) {
        if (1 <= tab[i]) {
            tab[i]--;
            mem = 0;
            break;
        }
        else {
            tab[i] = MAKS - 1;
        }
    }
    if (mem == 1) {
        if (tab[dlugosc[zmienna] - 1] == 1 && dlugosc[zmienna] > 1) {
            dlugosc[zmienna]--;
            tab = realloc(tab, (size_t) dlugosc[zmienna] * sizeof *tab);
        }
        else {
            tab[dlugosc[zmienna] - 1]--;
        }
    }
    *tablica = tab;
}

void CLR(u_llong **tablica, int dlugosc[], int zmienna) {
    u_llong *tab = *tablica;
    dlugosc[zmienna] = 1;
    tab = realloc(tab, (size_t) sizeof *tab);
    tab[0] = 0;
    *tablica = tab;
}

bool czy_zero(u_llong *tab, int dlugosc) {
    if (dlugosc == 1 && tab[0] == 0)
        return true;
    else
        return false;
}

void zwykla_instrukcja(u_llong ***tablica, int dlugosc[], instrukcje_ *obecna_instrukcja) {
    u_llong **tab = *tablica;
    for (int i = 0; i < ZMIENNE; i++) {
        for (int j = 0; j < obecna_instrukcja->tablica[i]; j++)
            INC(&tab[i], dlugosc, i);
    }
    *tablica = tab;
}

void zooptymalizowana_instrukcja(u_llong ***tablica, int dlugosc[], instrukcje_ *obecna_instrukcja) {
    u_llong **tab = *tablica;
    for (int i = 0; i < ZMIENNE; i++) {
        for (int j = 0; j < obecna_instrukcja->tablica[i]; j++)
            ADD(&tab[i], tab[obecna_instrukcja->zmienna0], dlugosc, i, obecna_instrukcja->zmienna0);
    }
    CLR(&tab[obecna_instrukcja->zmienna0], dlugosc, obecna_instrukcja->zmienna0);
    *tablica = tab;
}

bool czy_dalej(int poziom, instrukcje_ *nast) { // Funkcja sprawdzająca czy dana instrukcja znajduje się wewnatrz obecnej instrukcji.
    if (nast->poziom > poziom)
        return true;
    else if (nast->poziom < poziom)
        return false;
    else if (nast->czy_optymalna || nast->zmienna0 == -1)
        return true;
    else
        return false;
}

instrukcje_ *JMP(instrukcje_ *pierwsza_instrukcja, instrukcje_ *obecna_instrukcja) {
    int poziom = obecna_instrukcja->poziom;
    instrukcje_ *nast = obecna_instrukcja->next;
    while (nast != NULL && czy_dalej(poziom, nast))
        nast = nast->next;
    if (nast == NULL)
        return pierwsza_instrukcja;
    else
        return nast;
}

void wykonaj_instrukcje(u_llong ***tablica, int dlugosc[], instrukcje_ *pierwsza_instrukcja) {
    instrukcje_ *obecna_instrukcja = pierwsza_instrukcja;
    pierwsza_instrukcja->adres = NULL;
    u_llong **tab = *tablica;
    int poziom = 1;
    while (obecna_instrukcja != NULL) {
         if (czy_zero(tab[pierwsza_instrukcja->zmienna0], dlugosc[pierwsza_instrukcja->zmienna0]) && obecna_instrukcja == pierwsza_instrukcja) {
            pierwsza_instrukcja = pierwsza_instrukcja->adres;
            if (pierwsza_instrukcja == NULL) {
                obecna_instrukcja = NULL;
            }
            else {
                obecna_instrukcja = JMP(pierwsza_instrukcja, obecna_instrukcja);
                poziom = pierwsza_instrukcja->poziom;
            }
        }
        if (obecna_instrukcja != NULL) {
            if (obecna_instrukcja->czy_optymalna == true) {
                zooptymalizowana_instrukcja(&tab, dlugosc, obecna_instrukcja);
                obecna_instrukcja = obecna_instrukcja->next;
            }
            else if (obecna_instrukcja->zmienna0 == -1) {
                zwykla_instrukcja(&tab, dlugosc, obecna_instrukcja);
                obecna_instrukcja = obecna_instrukcja->next;
            }
            else if (!czy_zero(tab[obecna_instrukcja->zmienna0], dlugosc[obecna_instrukcja->zmienna0])) {
                DC(&tab[obecna_instrukcja->zmienna0], dlugosc,obecna_instrukcja->zmienna0);
                zwykla_instrukcja(&tab, dlugosc, obecna_instrukcja);
                obecna_instrukcja = obecna_instrukcja->next;
            }
            if (obecna_instrukcja == NULL || !czy_dalej(poziom, obecna_instrukcja)) {
                obecna_instrukcja = pierwsza_instrukcja;
            }
            else if (poziom < obecna_instrukcja->poziom) {
                poziom = obecna_instrukcja->poziom;
                obecna_instrukcja->adres = pierwsza_instrukcja;
                pierwsza_instrukcja = obecna_instrukcja;
            }
        }
    }
    *tablica = tab;
}

bool wczytaj_dane(u_llong ***tablica, int dlugosc[]) {
    u_llong **tab = *tablica;
    int a = getchar();
    while (a != (int) '\n') {
        if (a == EOF) {
            return false;
        }
        else if (a == (int) '=') {
            a = (int) getchar();
            printf_(tab[(int) a - 'a'], dlugosc, (int) a - 'a');
        }
        else if (a == (int) '(') {
            ungetc(a, stdin);
            instrukcje_  *pierwsza_instrukcja = wczytaj_instrukcje();
            wykonaj_instrukcje(&tab, dlugosc, pierwsza_instrukcja);
            free_(pierwsza_instrukcja);
        }
        else {
            INC(&tab[(int) a - 'a'], dlugosc, (int) a - 'a');
        }
        a = getchar();
    }
    *tablica = tab;
    return true;
}

int main(void) {
    int dlugosc[ZMIENNE];
    bool wykonuj = true;
    u_llong** tablica = (u_llong**)malloc(ZMIENNE * sizeof(u_llong*));
    for (int i = 0; i < ZMIENNE; i++) {
        tablica[i] = (u_llong*)malloc(sizeof(u_llong));
        tablica[i][0] = 0;
        dlugosc[i] = 1;
    }
    while(wykonuj)
        wykonuj = wczytaj_dane(&tablica, dlugosc);
    for(int i = 0; i < ZMIENNE; i++)
        free(tablica[i]);
    free(tablica);
    return 0;
}
