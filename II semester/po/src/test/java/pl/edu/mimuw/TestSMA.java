package pl.edu.mimuw;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import pl.edu.mimuw.Investors.SMA;
import pl.edu.mimuw.StockMarket.InvalidData;
import pl.edu.mimuw.StockMarket.StockMarket;

import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Map;

public class TestSMA {
    private static StockMarket s;
    private static SMA sma;


    @BeforeAll
    public static void setData() throws InvalidData.InvalidStockId, InvalidData.InvalidStockInWallet,
            InvalidData.InvalidInvestorType, InvalidData.InvalidDataLength,
            FileNotFoundException {
        s = new StockMarket("plik.txt", 100);
        s.runSimulation();
        sma = new SMA(s.getSMACalculator());
        var map = new HashMap<String, Integer>();
        map.put("APL", 100);
        map.put("GOOGL", 100);
        map.put("MSFT", 100);
        sma.SetWallet(1000, map);
    }

    @Test
    public void Test0() {
        var mapa = s.getLastStockPrice();
        var kalkulator = s.getSMACalculator();
        for (Map.Entry<String, Integer> entry : mapa.entrySet()) {
            if (kalkulator.calculateSMA(entry.getKey(), s.getCurrentTurn()) != 0)
                assert (sma.wantsToPlaceOrder(s));

        }
    }

    @Test
    public void Test1() {
        var map = s.getLastStockPrice();
        var calculator = s.getSMACalculator();
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            if (calculator.calculateSMA(entry.getKey(), s.getCurrentTurn()) != 0) {
                var newOrder = sma.addOrder(s);
                assert ((calculator.calculateSMA(newOrder.stockId(), s.getCurrentTurn()) == 1 && newOrder.isBuyOrder())
                        || (calculator.calculateSMA(newOrder.stockId(), s.getCurrentTurn()) == -1
                        && !newOrder.isBuyOrder()));
            }
        }

    }

    @Test
    public void Test2() {
        var map = s.getLastStockPrice();
        var calculator = s.getSMACalculator();
        for (int i = 0; i < 100; i++) {
            for (Map.Entry<String, Integer> entry : map.entrySet()) {
                if (calculator.calculateSMA(entry.getKey(), s.getCurrentTurn()) != 0) {
                    var newOrder = sma.addOrder(s);
                    assert ((calculator.calculateSMA(newOrder.stockId(), s.getCurrentTurn()) == 1 && newOrder.isBuyOrder())
                            || (calculator.calculateSMA(newOrder.stockId(), s.getCurrentTurn()) == -1
                            && !newOrder.isBuyOrder()));
                }
            }
            s.executeTurn();
        }
    }
}
