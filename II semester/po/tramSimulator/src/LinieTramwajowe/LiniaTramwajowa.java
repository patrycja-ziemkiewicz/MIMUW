package LinieTramwajowe;

import Kolejka.KolejkaZdarzeń;
import Przystanki.Przystanek;
import Pojazdy.*;
import Zdarzenia.Zdarzenie;
import Zdarzenia.ZdarzenieTramwajowe;

public class LiniaTramwajowa {
    private final int numer;
    private final int odstępy;
    private final int czasDojazdu[];
    private final Przystanek przystanki[];
    private Tramwaj[] tramwaje;

    public LiniaTramwajowa (int numer, int iloscTramwajow, int[] czasDojazdu, Przystanek[] przystanki) {
        this.numer = numer;
        this.czasDojazdu = czasDojazdu;
        this.przystanki = przystanki;
        int odstępy = 0;
        for (int i = 0; i < czasDojazdu.length; i++) {
            odstępy += czasDojazdu[i];
        }
        this.odstępy = (2 * odstępy) / iloscTramwajow;
        this.tramwaje = new Tramwaj[iloscTramwajow];
    }

    public void DodajTramwaj(int i, Tramwaj tramwaj) {
        tramwaje[i] = tramwaj;
    }

    public int LiczbaPrzystanków() { return przystanki.length;}

    public int Numer() {
        return numer;
    }

    public int Odstępy() {
        return odstępy;
    }

    public int CzasDojazdu(int i) {
        return czasDojazdu[i];
    }

    public Przystanek przystanek(int i) {// nwm co z tym
        return przystanki[i];
    }

    public int IloscTramwajów() {return tramwaje.length;}

    public void NastępnyDzień(KolejkaZdarzeń kolejkaZdarzeń, int obecnyDzień) {
        for(int i = 0; i < IloscTramwajów(); i++) {
            tramwaje[i].NastępnyDzień();
            Zdarzenie zdarzenie = new ZdarzenieTramwajowe(obecnyDzień, tramwaje[i], tramwaje[i].ObecnyPrzystanek(), this);
            kolejkaZdarzeń.Dodaj(zdarzenie);
        }
    }
}
