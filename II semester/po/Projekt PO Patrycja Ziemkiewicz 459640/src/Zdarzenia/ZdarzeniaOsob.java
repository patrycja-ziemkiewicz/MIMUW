package Zdarzenia;

import Pasazerowie.Pasazer;
import Przystanki.Przystanek;

import java.time.LocalTime;

public class ZdarzeniaOsob extends Zdarzenie {
    private Przystanek przystanek;
    private Pasazer pasażer;
    private int dzień;

    public ZdarzeniaOsob(int dzień, Przystanek przystanek, Pasazer pasażer) {
        this.przystanek = przystanek;
        this.pasażer = pasażer;
        this.dzień = dzień;
    }

    @Override
    public void wykonaj() {
        System.out.println(dzień + ", " + ObecnaGodzina() + ": Pasażer " + pasażer.Numer() + " przyszedł na przystanek "
                + przystanek.Nazwa());
        if (!przystanek.CzyPrzepełniony()){
            przystanek.wpuśćPasażera(pasażer);
            przystanek.Uaktualnij();
        }
        else {
            System.out.println(dzień + ", " + ObecnaGodzina() + ": Pasażer " + pasażer.Numer() + " zawrócił do domu ");
        }
    }

    @Override
    public LocalTime ObecnaGodzina() {
        return pasażer.GodzinaPrzyjścia();
    }

    @Override
    public boolean Następne(){
            return false;
    }
}
