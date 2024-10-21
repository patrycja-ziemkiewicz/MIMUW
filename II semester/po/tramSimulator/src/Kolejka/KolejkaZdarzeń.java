package Kolejka;

import Zdarzenia.Zdarzenie;
import Zdarzenia.ZdarzenieTramwajowe;

import java.time.LocalTime;

public class KolejkaZdarzeń implements Kolejka {
    private int ilość;
    private Zdarzenie[] kolejka;
    private int numerNastępnegoZdarzenia;

    public KolejkaZdarzeń() {
        this.numerNastępnegoZdarzenia = 0;
        this.ilość = 0;
        this.kolejka = new ZdarzenieTramwajowe[1];
    }


    protected void NowyRozmiar() {
        if (ilość >= kolejka.length ||  ilość * 2 < kolejka.length) {
            int nowyRozmiar;
            if (ilość >= kolejka.length) nowyRozmiar = kolejka.length * 2 + 1;
            else nowyRozmiar = kolejka.length / 2 + 1;
            Zdarzenie[] nowa = new Zdarzenie[nowyRozmiar];
            for (int i = 0; i < ilość; i++) {
                nowa[i] = kolejka[i];
            }
            kolejka = nowa;
        }
    }

    public Zdarzenie NastępneZdarzenie() {
        assert (ilość == 0); // ZATRZYMUJE GDY POBIERAM Z PUSTEJ KOLEJKI
        LocalTime pierwszeZdarzenie = kolejka[0].ObecnaGodzina();
        int index = 0;
        for (int i = 1; i < ilość; i++) {
            if (pierwszeZdarzenie.compareTo(kolejka[i].ObecnaGodzina()) > 0) {
                pierwszeZdarzenie = kolejka[i].ObecnaGodzina();
                index = i;
            }
            else if (pierwszeZdarzenie.compareTo(kolejka[i].ObecnaGodzina()) == 0) {
                if (kolejka[i].KolejnośćZdarzenia() < kolejka[index].KolejnośćZdarzenia()) {
                    index = i;
                }
            }
        }
        Zdarzenie następneZdarzenie = kolejka[index];
        kolejka[index] = kolejka[ilość - 1];
        ilość--;
        NowyRozmiar();
        return następneZdarzenie;
    }
    public boolean CzyPusta() {
        if (ilość == 0) {
            numerNastępnegoZdarzenia = 0; // resetuję kolejkę
            return true;
        }
        return false;
    }

    public void Dodaj(Zdarzenie zdarzenie) {
        NowyRozmiar();
        kolejka[ilość] = zdarzenie;
        zdarzenie.UstawKolejnośćZdarzenia(numerNastępnegoZdarzenia);
        ilość++;
        numerNastępnegoZdarzenia++;
    }

}
