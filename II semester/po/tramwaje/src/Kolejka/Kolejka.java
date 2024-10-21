package Kolejka;

import Zdarzenia.Zdarzenie;

public interface Kolejka {

    boolean CzyPusta();
    void Dodaj(Zdarzenie zdarzenie);
    Zdarzenie NastępneZdarzenie();
}
