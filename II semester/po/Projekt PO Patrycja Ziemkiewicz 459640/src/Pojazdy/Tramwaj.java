package Pojazdy;

import LinieTramwajowe.LiniaTramwajowa;
import Pasazerowie.Pasazer;
import Przystanki.Przystanek;

import java.time.*;

public class Tramwaj extends Pojazd{
    private int obecnyPrzystanek;
    private final int pierwszyPrzystanek;
    private final LocalTime godzinaWyjazdu;
    private LocalTime obecnaGodzina;
    private final int kierunekWyjazdu;
    private int kierunek;
    static final LocalTime OSTATNIA_GODZINA = LocalTime.parse("23:00");

    public Tramwaj(int numerPojazdu, LiniaTramwajowa linia, int pojemność) {
        super(numerPojazdu, linia, pojemność);
        if (numerPojazdu % 2 == 0) {
            obecnyPrzystanek = 0;
            kierunekWyjazdu = 1;
        }
        else {
            obecnyPrzystanek = linia.LiczbaPrzystanków() - 1;
            kierunekWyjazdu = -1;
        }
        pierwszyPrzystanek = obecnyPrzystanek;
        kierunek = kierunekWyjazdu;
        LocalTime początek = LocalTime.parse("06:00:00");
        this.obecnaGodzina = początek.plusMinutes((numerPojazdu / 2) * linia.Odstępy());
        this.godzinaWyjazdu = this.obecnaGodzina;
    }

    public LocalTime ObecnaGodzina() {
        return obecnaGodzina;
    }


    public boolean PrzejedźDalej() {
        if (CzyOstatniPrzejazd()) {
            obecnyPrzystanek = pierwszyPrzystanek;
            obecnaGodzina = godzinaWyjazdu;
            kierunek = kierunekWyjazdu;
            return false;
        }
        if (obecnyPrzystanek + kierunek >= linia.LiczbaPrzystanków() || obecnyPrzystanek + kierunek < 0) {
            kierunek *= -1;
            obecnaGodzina = obecnaGodzina.plusMinutes(linia.CzasDojazdu(linia.LiczbaPrzystanków() - 1));
        }
        else {
            int pomoc = 0; // na podstawie kierunku pomaga wziąć odpowiednią wartość z tablicy czasu dojazdu
            if (kierunek < 0) pomoc = -1;
            obecnaGodzina = obecnaGodzina.plusMinutes(linia.CzasDojazdu(obecnyPrzystanek + pomoc));
            obecnyPrzystanek += kierunek;
        }
        return true;
    }

    public boolean CzyChceWysiąść(int i) {
        if (pasażerowie[i].ObecnyPrzystanek() == linia.przystanek(obecnyPrzystanek))
            return true;
        return false;
    }

    public void wypuśćPasażera(int i) {
        Przystanek przystanek = linia.przystanek(obecnyPrzystanek);
        przystanek.wpuśćPasażera(pasażerowie[i]);
        pasażerowie[i].ZacznijCzekać(obecnaGodzina);
        pasażerowie[i] = pasażerowie[ilośćPasażerów - 1];
        ilośćPasażerów--;
    }

    public int Kierunek() {
        return kierunek;
    }

    public void wpuśćPasażera(Pasazer osoba) {
        assert (ilośćPasażerów >= pojemność);
        pasażerowie[ilośćPasażerów] = osoba;
        ilośćPasażerów++;
        osoba.Przejedź(obecnaGodzina);
    }

    public Przystanek ObecnyPrzystanek() {
        return linia.przystanek(obecnyPrzystanek);
    }

    public int NumerPrzystanku() {
        return obecnyPrzystanek;
    }

    public boolean CzyNieMożnaWejść() {
        if (ilośćPasażerów >= pojemność)
            return true;
        if (CzyOstatniPrzejazd())
            return true;
        return false;
    }

    public void NastępnyDzień() {
        ilośćPasażerów = 0;
        obecnyPrzystanek = pierwszyPrzystanek;
        obecnaGodzina = godzinaWyjazdu;
        kierunek = kierunekWyjazdu;
    }

    public boolean CzyOstatniPrzejazd() {
        if (obecnaGodzina.compareTo(OSTATNIA_GODZINA) >= 0
                && (obecnyPrzystanek == 0 || obecnyPrzystanek == linia.LiczbaPrzystanków() - 1))
            return true;
        return false;
    }

}
