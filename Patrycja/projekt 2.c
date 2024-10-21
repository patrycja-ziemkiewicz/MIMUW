#include <stdio.h>
#include <limits.h>
#include <string.h>

#define LIMIT 101 //Ciągi znaków mają maksymalnie 100 znaków nie licząc kończącego ich znaku '\n', więc jako że w tablicach chce przechowywać kończący ich znak muszę ustawić limit na 101

static void printf_(char tablica[]) {
    int i = 0;
    do {
    putchar(tablica[i]);
    i++;
    } while (tablica[i - 1] != '\n');
}

static void fgets_(char tablica[]) {
    char a;
    int i = 0;
    do {
    a = (char) getchar();
    tablica[i] = a;
    i++;
    } while (a != '\n');
}

static void interpretacja_slowa(int n, char reguly_zamian[][LIMIT], char reguly_interpretacji[][LIMIT], char wyraz[], char interpretowane_litery[], char zamieniane_litery[]) {
    if (n == 0) {
        int i = 0;
        while (wyraz[i] != '\n') {
            if (interpretowane_litery[(int) wyraz[i]] != '\n')
                printf_(reguly_interpretacji[(int) wyraz[i]]);
            i++;
        }
    }
    else {
        int i = 0;
        while (wyraz[i] != '\n') {
             if (zamieniane_litery[(int) wyraz[i]] != '\n') {
                interpretacja_slowa(n - 1, reguly_zamian, reguly_interpretacji, reguly_zamian[(int) wyraz[i]], interpretowane_litery, zamieniane_litery);
             }
             else if (interpretowane_litery[(int) wyraz[i]] != '\n')
                printf_(reguly_interpretacji[(int) wyraz[i]]);
             i++;
        }
    }
}

static void wczytywanie_regul(char tablica_regul[][LIMIT], char tablica_liter[]) {
    char a;
    a = (char) getchar();
    while (a != '\n') {
        tablica_liter[(int) a] = a;
        fgets_(tablica_regul[(int) a]);
        a = (char) getchar();
    }
}

static void wczytywanie_prologow(void) {
    char a, tablica[LIMIT];
    a = (char) getchar();
    while (a != '\n' && a != EOF) {
        ungetc(a, stdin);
        fgets_(tablica);
        printf_(tablica);
        a = (char) getchar();
    }
}

int main(void) {
    char reguly_zamian[CHAR_MAX][LIMIT], aksjomat[LIMIT], reguly_interpretacji[CHAR_MAX][LIMIT], interpretowane_litery[CHAR_MAX], zamieniane_litery[CHAR_MAX];
    int n;
    for (int i = 0; i < CHAR_MAX; i++) {
        interpretowane_litery[i] = '\n';
        zamieniane_litery[i] = '\n';
    }
    scanf("%d", &n);
    getchar();
    fgets_(aksjomat);
    wczytywanie_regul(reguly_zamian, zamieniane_litery);
    wczytywanie_prologow();
    wczytywanie_regul(reguly_interpretacji, interpretowane_litery);
    interpretacja_slowa(n, reguly_zamian, reguly_interpretacji, aksjomat, interpretowane_litery, zamieniane_litery);
    wczytywanie_prologow();
    return 0;
}
