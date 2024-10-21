package Losowanie;

import java.util.Random;

public class Losowanie {
    public static int losuj(int dolna, int gorna) {
        Random liczba = new Random();

        return liczba.nextInt(gorna - dolna + 1) + dolna;
    }

}
