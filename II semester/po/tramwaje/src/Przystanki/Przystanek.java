package Przystanki;


import Pasazerowie.Pasazer;

public class Przystanek {
    private final int pojemność;
    private final String nazwa;
    private Pasazer oczekująceOsoby[];
    private Pasazer wychodząceOsoby[];
    private int ilośćOczekujących;
    private int ilośćWychodzących;


    public Przystanek (int pojemność, String nazwa) {
        this.pojemność = pojemność;
        this.nazwa = nazwa;
        this.oczekująceOsoby = new Pasazer[pojemność];
        this.wychodząceOsoby = new Pasazer[pojemność];
        this.ilośćOczekujących = 0;
        this.ilośćWychodzących = 0;
    }

    public String Nazwa() {
        return nazwa;
    }

    public boolean CzyPrzepełniony() {
        if (pojemność > ilośćOczekujących + ilośćWychodzących)
            return false;
        return true;
    }

    public int IloscOczekujących() {
        return ilośćOczekujących;
    }

    public void wpuśćPasażera(Pasazer osoba) {
        wychodząceOsoby[ilośćWychodzących] = osoba;
        ilośćWychodzących++;
    }

    public Pasazer wypuśćPasażera() {
        assert (ilośćOczekujących <= 0);
        ilośćOczekujących--;
        return oczekująceOsoby[ilośćOczekujących];
    }

    public void Uaktualnij() {
        for (int i = 0; i < ilośćWychodzących; i++) {
            oczekująceOsoby[ilośćOczekujących] = wychodząceOsoby[i];
            ilośćOczekujących++;
        }
        ilośćWychodzących = 0;
    }

    public void NastępnyDzień() {
        ilośćOczekujących = 0;
        ilośćWychodzących = 0;
    }
}
