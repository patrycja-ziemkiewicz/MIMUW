package Zdarzenia;

import java.time.LocalTime;

public abstract class Zdarzenie {
    private int kolejnośćZdarzenia;
    public Zdarzenie() {
    }

    public int KolejnośćZdarzenia() {
        return kolejnośćZdarzenia;
    }

    public void UstawKolejnośćZdarzenia(int kolejnośćZdarzenia) {
        this.kolejnośćZdarzenia = kolejnośćZdarzenia;
    }

    public abstract void wykonaj();
    public abstract LocalTime ObecnaGodzina();
    public abstract boolean Następne();

}
