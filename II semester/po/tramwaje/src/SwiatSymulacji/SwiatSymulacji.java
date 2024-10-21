package SwiatSymulacji;

import Kolejka.KolejkaZdarzeń;
import LinieTramwajowe.LiniaTramwajowa;
import Losowanie.Losowanie;
import Pasazerowie.Pasazer;
import Pojazdy.Tramwaj;
import Przystanki.Przystanek;
import Zdarzenia.*;


import java.util.Scanner;

public class SwiatSymulacji {
    private final LiniaTramwajowa[] linieTramwajowe;
    private final int ilośćDni;
    private int obecnyDzień;
    private final Przystanek[] przystanki;
    private final Pasazer[] pasazerowie;
    private final KolejkaZdarzeń kolejkaZdarzeń;

    public SwiatSymulacji() {
        this.kolejkaZdarzeń = new KolejkaZdarzeń();
        Scanner sc = new Scanner(System.in);
        this.ilośćDni = sc.nextInt();
        this.obecnyDzień = 0;
        this.przystanki = wczytaniePrzystanków(sc);
        this.pasazerowie = wczytywaniePasażerów(this.przystanki, kolejkaZdarzeń, sc);
        this.linieTramwajowe = wczytanieLinii(przystanki, kolejkaZdarzeń, sc);
        sc.close();
    }

    public void WykonajSymulację() {
        for (int i = 0; i < ilośćDni; i++) {
            WykonajDzień();
            DajStatystyki();
            NastępnyDzień();
        }
    }

    private void DajStatystyki() {
        int łącznyCzasCzekania = 0;
        int łącznaLiczbaPrzejazdów = 0;
        for (int i = 0; i < pasazerowie.length; i++) {
            łącznaLiczbaPrzejazdów += pasazerowie[i].LiczbaPrzejazdów();
            łącznyCzasCzekania += pasazerowie[i].CzasCzekania();
        }
        System.out.println("Łączna liczba przejazdów: " + łącznaLiczbaPrzejazdów);
        System.out.println("Łączny czas czekania: " + łącznyCzasCzekania);
        System.out.println("Średni cza czekania: " + (int) łącznyCzasCzekania / łącznaLiczbaPrzejazdów);
    }


    private void WykonajDzień() {
        while (!kolejkaZdarzeń.CzyPusta()) {
            Zdarzenie zdarzenie = kolejkaZdarzeń.NastępneZdarzenie();
            zdarzenie.wykonaj();
            if (zdarzenie.Następne()) kolejkaZdarzeń.Dodaj(zdarzenie);
        }
    }

    private void NastępnyDzień() {
        obecnyDzień++;
        for (int i = 0; i < pasazerowie.length; i++) {
            pasazerowie[i].WrocDoDomu();
            Zdarzenie przyjscie = new ZdarzeniaOsob(obecnyDzień, pasazerowie[i].ObecnyPrzystanek(), pasazerowie[i]);
            kolejkaZdarzeń.Dodaj(przyjscie);
        }
        for (int i = 0; i < przystanki.length; i++) {
            przystanki[i].NastępnyDzień();
        }
        for (int i = 0; i < linieTramwajowe.length; i++) {
            linieTramwajowe[i].NastępnyDzień(kolejkaZdarzeń, obecnyDzień);
        }
    }

    private Pasazer[] wczytywaniePasażerów(Przystanek[] przystanki, KolejkaZdarzeń kolejkaZdarzeń, Scanner sc) {
        int liczbaPasażerów = sc.nextInt();
        Pasazer[] pasazerowie = new Pasazer[liczbaPasażerów];
        for (int i = 0; i < liczbaPasażerów; i++) {
            int pierwszyPrzystanek = Losowanie.losuj(obecnyDzień, przystanki.length - 1);
            pasazerowie[i] = new Pasazer(i, przystanki[pierwszyPrzystanek]);
            Zdarzenie przyjscie = new ZdarzeniaOsob(0, pasazerowie[i].ObecnyPrzystanek(), pasazerowie[i]);
            kolejkaZdarzeń.Dodaj(przyjscie);
        }
        return pasazerowie;
    }

    private Przystanek[] wczytaniePrzystanków(Scanner sc) {
        int pojemnoscPrzystanków = sc.nextInt();
        int liczbaPrzystanków = sc.nextInt();
        Przystanek[] przystanki = new Przystanek[liczbaPrzystanków];
        for (int i = 0; i < liczbaPrzystanków; i++) {
            przystanki[i] = new Przystanek(pojemnoscPrzystanków, sc.next());
        }
        return przystanki;
    }

    private LiniaTramwajowa[] wczytanieLinii(Przystanek[] przystanki, KolejkaZdarzeń kolejkaZdarzeń, Scanner sc) {
        int pojemnoscTramwajów = sc.nextInt();
        int liczbaLinii = sc.nextInt();
        LiniaTramwajowa[] linieTramwajowe = new LiniaTramwajowa[liczbaLinii];
        for (int i = 0; i < liczbaLinii; i++) {
            int liczbaTramwajów = sc.nextInt();
            int dlugośćTrasy = sc.nextInt();
            Przystanek[] przystankiLinii = new Przystanek[dlugośćTrasy];
            int[] czasDojazdu = new int[dlugośćTrasy];
            for (int j = 0; j < dlugośćTrasy; j++) {
                String nazwa = sc.next();
                for (int k = 0; k < przystanki.length; k++) {
                    if (nazwa.equals(przystanki[k].Nazwa())) {
                        przystankiLinii[j] = przystanki[k];
                        break;
                    }
                }
                czasDojazdu[j] = sc.nextInt();
            }
            linieTramwajowe[i] = new LiniaTramwajowa(i, liczbaTramwajów, czasDojazdu, przystankiLinii);
            for (int j = 0; j < liczbaTramwajów; j++) {
                Tramwaj tramwaj = new Tramwaj(j, linieTramwajowe[i], pojemnoscTramwajów);
                linieTramwajowe[i].DodajTramwaj(j, tramwaj);
                Zdarzenie zdarzenie = new ZdarzenieTramwajowe(obecnyDzień, tramwaj, tramwaj.ObecnyPrzystanek(), linieTramwajowe[i]);
                kolejkaZdarzeń.Dodaj(zdarzenie);
            }
        }
        return linieTramwajowe;
    }

}
