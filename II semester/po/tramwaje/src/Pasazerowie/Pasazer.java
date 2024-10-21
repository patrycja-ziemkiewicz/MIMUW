package Pasazerowie;


import Przystanki.Przystanek;
import java.time.*;
import Losowanie.Losowanie;

public class Pasazer {
    private final int numer;
    private final Przystanek pierwszyPrzystanek;
    private Przystanek obecnyPrzystanek;  // JEST TO TEZ PRZYSTANEK NA KTORYM PLANUJE WYSIAŚĆ
    private LocalTime godzinaPrzyjścia;
    private final LocalTime PIERWSZA_GODZINA = LocalTime.parse("06:00");
    private int liczbaPrzejazdów;
    private int czasCzekania;
    private LocalTime przyjścieNaPrzystanek;

    public Pasazer(int numer, Przystanek pierwszyPrzystanek) {
        this.numer = numer;
        this.pierwszyPrzystanek = pierwszyPrzystanek;
        WrocDoDomu();
    }

    public int CzasCzekania() {
        return czasCzekania;
    }

    public int LiczbaPrzejazdów() {
        return liczbaPrzejazdów;
    }

    public void Przejedź(LocalTime obecnaGodzina) {
        liczbaPrzejazdów++;
        czasCzekania +=  (obecnaGodzina.getHour() - przyjścieNaPrzystanek.getHour()) * 60;
        czasCzekania +=  (obecnaGodzina.getMinute() - przyjścieNaPrzystanek.getMinute()) ;

    }

    public void ZacznijCzekać(LocalTime obecnaGodzina) {
        przyjścieNaPrzystanek = obecnaGodzina;
    }

    public void UstawGodzinęPrzyjścia(int minuty){
        this.godzinaPrzyjścia = this.PIERWSZA_GODZINA.plusMinutes(minuty);
    }

    public int Numer() {
        return numer;
    }

    public LocalTime GodzinaPrzyjścia() {
        return godzinaPrzyjścia;
    }

    public void WybierzPrzystanek(Przystanek przystanek) {
        obecnyPrzystanek = przystanek;
    }

    public Przystanek ObecnyPrzystanek() {
        return obecnyPrzystanek;
    }

    public void WrocDoDomu() {
        UstawGodzinęPrzyjścia(Losowanie.losuj(0, 360));
        przyjścieNaPrzystanek = godzinaPrzyjścia;
        obecnyPrzystanek = pierwszyPrzystanek;
        liczbaPrzejazdów = 0;
        czasCzekania = 0;
    }
}
