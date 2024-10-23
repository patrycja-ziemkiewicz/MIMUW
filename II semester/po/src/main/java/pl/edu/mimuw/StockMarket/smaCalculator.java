package pl.edu.mimuw.StockMarket;

import java.util.HashMap;
import java.util.Map;

public class smaCalculator {
    private HashMap<String, Integer[]> lastStockPrices;

    public smaCalculator() {}

    public void UstawKalkulatorSMA(HashMap<String, Integer> lastStockPrices) {
        this.lastStockPrices = new HashMap<>(lastStockPrices.size());
        for (Map.Entry<String, Integer> entry: lastStockPrices.entrySet()) {
            var tab = new Integer[10];
            tab[0] = entry.getValue();
            this.lastStockPrices.put(entry.getKey(), tab);
        }
    }

    // Funkcja uaktualnia dane dla każdej akcji po wykonaniu tury.
    public void update(HashMap<String, Integer> lastStockPrice, int currentTurn) {
        for (Map.Entry<String, Integer[]> entry: lastStockPrices.entrySet()) {
            var tab = entry.getValue();
            tab[currentTurn % 10] = lastStockPrice.get(entry.getKey());
            lastStockPrices.put(entry.getKey(), tab);
        }
    }

    public int calculateSMA(String stockId, int currentTurn) {
        var lastStockPrices = this.lastStockPrices.get(stockId);
        int SMA10 = calculateSMA(0, 10, lastStockPrices);
        int previousSMA5 = calculateSMA((currentTurn - 4 )% 10, (currentTurn - 1) % 10, lastStockPrices);
        int SMA5 = calculateSMA((currentTurn - 5 )% 10, currentTurn % 10, lastStockPrices);
        if (SMA5 > SMA10 && previousSMA5 <= SMA10)
            return 1;
        if (SMA5 < SMA10 && previousSMA5 >= SMA10)
            return -1;
        return 0;
    }

    private int calculateSMA(int p, int k, Integer[] lastStockPrices) {
        int SMA = 0;
        for (int i = p; i < k; i++)
            SMA += lastStockPrices[i];
        return SMA / (k - p);
    }


}
