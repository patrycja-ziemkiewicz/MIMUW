package Pojazdy;

import LinieTramwajowe.LiniaTramwajowa;
import Pasazerowie.Pasazer;

public abstract class Pojazd {
    protected final int numerPojazdu;
    protected final LiniaTramwajowa linia;
    protected final int pojemność;
    protected Pasazer[] pasażerowie;
    protected int ilośćPasażerów;

    public Pojazd(int numerPojazdu, LiniaTramwajowa linia, int pojemność) {
        this.numerPojazdu = numerPojazdu;
        this.linia = linia;
        this.pojemność = pojemność;
        this.pasażerowie = new Pasazer[pojemność];
        this.ilośćPasażerów = 0;
    }

    public abstract boolean CzyNieMożnaWejść() ;

    public int IlośćPasażerów() {
        return ilośćPasażerów;
    }

    public Pasazer ostatniPasazer() {
        return pasażerowie[ilośćPasażerów - 1];
    }
    public Pasazer pasazer(int i) {
        return pasażerowie[i];
    }

    public int Numer() {
        return numerPojazdu;
    }
}
