package pl.edu.mimuw.Investors;

import pl.edu.mimuw.StockMarket.smaCalculator;
import pl.edu.mimuw.StockMarket.StockMarket;
import pl.edu.mimuw.Orders.*;

import java.util.*;

public class SMA extends Investor {
    private smaCalculator smaCalculator;

    public SMA(smaCalculator smaCalculator) {
        this.smaCalculator = smaCalculator;
    }

    //SMA chce dodać zlecenie zawsze jak conajmniej jedna akcja spełnia warunek kalkulatoraSMA.
    public boolean wantsToPlaceOrder(StockMarket s) {
        if (s.getCurrentTurn() < 10 ||(getStockIdForSale(s) == null && getStockIdForPurchase(s) == null))
            return false;
        return true;
    }

    protected String getStockIdForPurchase(StockMarket s) {
        List<String> keys = new ArrayList<>();
        //Może kupić tylko wtedy, gdy ma zasoby i kalkulator dla danej akcji wyniesie 1
        for(Map.Entry<String, Integer> entry : stockHoldings.entrySet()) {
            if (s.getLastStockPrice(entry.getKey()) <= wallet
                    && smaCalculator.calculateSMA(entry.getKey(), s.getCurrentTurn()) == 1)
                keys.add(entry.getKey());
        }
        if (keys.isEmpty()) {
            return null;
        }

        Random random = new Random();

        int randomIndex = random.nextInt(keys.size());
        return keys.get(randomIndex);
    }

    private String getStockIdForSale(StockMarket s) {
        //Może sprzedać tylko wtedy, gdy ma zasoby i kalkulator dla danej akcji wyniesie -1
        List<String> keys = new ArrayList<>();
        for(Map.Entry<String, Integer> entry : stockHoldings.entrySet()) {
            if (entry.getValue() > 0 && smaCalculator.calculateSMA(entry.getKey(), s.getCurrentTurn()) == -1)
                keys.add(entry.getKey());
        }

        if (keys.isEmpty()) {
            return null;
        }
        Random random = new Random();
        // Losowanie indeksu z zakresu rozmiaru listy kluczy
        int randomIndex = random.nextInt(keys.size());

        // Zwrócenie wylosowanego klucza
        return keys.get(randomIndex);
    }

    public Order addOrder(StockMarket s) {
        Random x = new Random();
        String stockId;
        boolean isBuyOrder = isBuyOrder(s, x);
        int stockAmount;
        int turn = s.getCurrentTurn();
        int stockPrice;

        if (isBuyOrder) {
            stockId = getStockIdForPurchase(s);
            stockPrice = setBuyingPrice(stockId, s);
            stockAmount = setBuyingQuantity(stockPrice);
        }
        else {
            stockId = getStockIdForSale(s);
            stockPrice = setSellingPrice(stockId, s);
            stockAmount = setSellingQuantity(stockId);
        }
        return switch (x.nextInt(4)) {
            case 0 -> new OpenEndedOrder(stockId, stockAmount, stockPrice, turn, this, isBuyOrder);
            case 1 -> new InstantOrder(stockId, stockAmount, stockPrice, turn, this, isBuyOrder);
            case 2 -> new DoOrCancelOrder(stockId, stockAmount, stockPrice, turn, this, isBuyOrder);
            default -> new TimeLimitedOrder(stockId, stockAmount, stockPrice, turn, this,
                    isBuyOrder, x.nextInt(10) + turn);
        };
    }

    private boolean isBuyOrder(StockMarket s, Random x){
        if (getStockIdForPurchase(s) == null)
            return false;
        else if (getStockIdForSale(s) == null)
            return true;
        else return x.nextInt(2) != 0;
    }

    private int setBuyingQuantity(int stockPrice){
        int maxNumberOfStocks = wallet / stockPrice;
        Random x = new Random();
        return x.nextInt(maxNumberOfStocks) + 1;
    }

    private int setSellingQuantity(String stockId){
        Random x = new Random();
        return x.nextInt(stockHoldings.get(stockId)) + 1;
    }

    private int setSellingPrice(String stockId, StockMarket s) {
        int stockPrice = s.getLastStockPrice(stockId);
        Random x = new Random();
        int minimum = Integer.max(1, stockPrice - 10);
        return x.nextInt(stockPrice + 10 - minimum) + minimum;
    }

    private int setBuyingPrice(String stockId, StockMarket s) {
        int stockPrice = s.getLastStockPrice(stockId);
        Random x = new Random();
        int minimum = Integer.max(1, stockPrice - 10);
        int maximum = Integer.min(wallet, stockPrice + 10);
        return x.nextInt(maximum - minimum) + minimum;
    }

}
