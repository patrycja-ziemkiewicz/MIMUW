package pl.edu.mimuw.Investors;

import pl.edu.mimuw.StockMarket.StockMarket;
import pl.edu.mimuw.Orders.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;

public class RANDOM extends Investor {
    public RANDOM() {
        super();
    }

    public boolean wantsToPlaceOrder(StockMarket s) {
        if (getStockIdForSale(s) == null && getStockIdForPurchase(s) == null)
            return false;
        Random x = new Random();
        if (x.nextInt(2) == 1)
            return true;
        else
            return false;
    }

    protected String getStockIdForPurchase(StockMarket s) {

        // Uzyskanie listy kluczy
        List<String> keys = new ArrayList<>();
        for(Map.Entry<String, Integer> entry : stockHoldings.entrySet()) {
            if (s.getLastStockPrice(entry.getKey()) <= wallet)
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

    protected String getStockIdForSale(StockMarket s) {
        // Uzyskanie listy kluczy, które mają wartość większą niż zero
        List<String> keys = new ArrayList<>();
        for(Map.Entry<String, Integer> entry : stockHoldings.entrySet()) {
            if (entry.getValue() > 0)
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

    protected int setBuyingQuantity(int stockPrice){
        int maxNumberOfStocks = wallet / stockPrice;
        Random x = new Random();
        return x.nextInt(maxNumberOfStocks) + 1;
    }

    protected int setSellingQuantity(String stockId){
        Random x = new Random();
        return x.nextInt(stockHoldings.get(stockId)) + 1;
    }

    protected int setSellingPrice(String stockId, StockMarket s) {
        int stockPrice = s.getLastStockPrice(stockId);
        Random x = new Random();
        int minimum = Integer.max(1, stockPrice - 10);
        return x.nextInt(stockPrice + 10 - minimum) + minimum;
    }

    protected int setBuyingPrice(String stockId, StockMarket s) {
        int stockPrice = s.getLastStockPrice(stockId);
        Random x = new Random();
        int minimum = Integer.max(1, stockPrice - 10);
        int maximum = Integer.min(wallet, stockPrice + 10);
        return x.nextInt(maximum - minimum) + minimum;
    }

}
