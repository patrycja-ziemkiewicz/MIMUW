package Zdarzenia;

import LinieTramwajowe.LiniaTramwajowa;
import Losowanie.Losowanie;
import Pasazerowie.Pasazer;
import Pojazdy.Tramwaj;
import Przystanki.Przystanek;

import java.time.LocalTime;

public class ZdarzenieTramwajowe extends Zdarzenie {
    private int dzień;
    private Tramwaj tramwaj;
    private Przystanek obecnyPrzystanek;
    private LiniaTramwajowa linia;


    public ZdarzenieTramwajowe(int dzień, Tramwaj tramwaj, Przystanek przystanek, LiniaTramwajowa linia) {
        this.linia = linia;
        this.dzień = dzień;
        this.tramwaj = tramwaj;
        this.obecnyPrzystanek = przystanek;
    }

    @Override
    public void wykonaj() {
        wypuśćPasażerów();
        wpuśćPasażęrów();
    }

    private void wypuśćPasażerów() {
        int i = 0; // numer indeksu pasażera w tramwaju
        while (i < tramwaj.IlośćPasażerów()) {
            if (tramwaj.CzyChceWysiąść(i)) {
                if (!obecnyPrzystanek.CzyPrzepełniony()) {
                    System.out.println(dzień + ", " + tramwaj.ObecnaGodzina() + ": Pasażer "
                            + tramwaj.pasazer(i).Numer() + " wysiada z tramwaju linii " + linia.Numer()
                            + " (nr bocz." + tramwaj.Numer() + ") na przystanku " + obecnyPrzystanek.Nazwa());
                    tramwaj.wypuśćPasażera(i);// nie zwiekszam w tym przypadku indeksu bo w tym wypadku ostani indeks
                    // zamienił sie miejscem z pasazerem ktorego wypuszczam
                }
                else {
                    if (tramwaj.CzyOstatniPrzejazd()) {
                        System.out.println(dzień + ", " + tramwaj.ObecnaGodzina() + ": Pasażerowi "
                                + tramwaj.pasazer(i).Numer() + " nie udalo sie wysiasc na " + obecnyPrzystanek.Nazwa()
                                + " z tramwaju linii " + linia.Numer() + " (nr bocz. " + tramwaj.Numer()
                                + "), ale jest to ostatni przejazd tramwaju, więc jakoś wrócił do domu");
                    }
                    else {
                        int nowyPrzystanek = wybierzPrzystanek(tramwaj.Kierunek(), tramwaj.NumerPrzystanku());
                        tramwaj.pasazer(i).WybierzPrzystanek(linia.przystanek(nowyPrzystanek));
                        System.out.println(dzień + ", " + tramwaj.ObecnaGodzina() + ": Pasażerowi "
                                + tramwaj.pasazer(i).Numer() + " nie udalo sie wysiasc na " + obecnyPrzystanek.Nazwa()
                                + " z tramwaju linii " + linia.Numer() + " (nr bocz. " + tramwaj.Numer()
                                + ") ma zamiar wysiąść na " + linia.przystanek(nowyPrzystanek).Nazwa());
                    }
                    i++;
                }
            }
            else {
                i++;
            }
        }
    }

    private void wpuśćPasażęrów() {
        while (!tramwaj.CzyNieMożnaWejść() && obecnyPrzystanek.IloscOczekujących() > 0) {
            Pasazer przesiadający = obecnyPrzystanek.wypuśćPasażera();
            int nowyPrzystanek = wybierzPrzystanek(tramwaj.Kierunek(), tramwaj.NumerPrzystanku());
            przesiadający.WybierzPrzystanek(linia.przystanek(nowyPrzystanek));
            tramwaj.wpuśćPasażera(przesiadający);
            System.out.println(dzień + ", " + tramwaj.ObecnaGodzina() + ": Pasażer "
                    + tramwaj.ostatniPasazer().Numer() + " wsiada do tramwaju linii " + linia.Numer() + " (nr bocz."
                    + tramwaj.Numer() + ") z zamiarem dojechania na "
                    + tramwaj.ostatniPasazer().ObecnyPrzystanek().Nazwa());
        }
        obecnyPrzystanek.Uaktualnij();
    }


    private int wybierzPrzystanek(int kierunek, int obecnyPrzystanek) {
        if (obecnyPrzystanek != 0 && obecnyPrzystanek != linia.LiczbaPrzystanków() - 1) {
            if (kierunek > 0)
                return Losowanie.losuj(obecnyPrzystanek + 1, linia.LiczbaPrzystanków() - 1);
            else
                return Losowanie.losuj(0, obecnyPrzystanek - 1);
        }
        else if (obecnyPrzystanek == 0)// zakladam ze nie ma jedno przystankowych linii
            return Losowanie.losuj(1, linia.LiczbaPrzystanków() - 1);
        else
            return Losowanie.losuj(0, linia.LiczbaPrzystanków() - 2);
    }

    @Override
    public LocalTime ObecnaGodzina() {
        return tramwaj.ObecnaGodzina();
    }

    @Override
    public boolean Następne() {
        if (tramwaj.PrzejedźDalej()) {
            obecnyPrzystanek = tramwaj.ObecnyPrzystanek();
            return true;
        }
        else {
            return false;
        }
    }

}
