package pl.edu.mimuw.Investors;

import pl.edu.mimuw.StockMarket.StockMarket;
import pl.edu.mimuw.Orders.*;

import java.util.HashMap;
import java.util.Map;

public abstract class Investor {
    protected int wallet;
    protected HashMap<String, Integer> stockHoldings;

    public Investor() {
    }

    public void SetWallet(int wallet, HashMap<String, Integer> stockAmount) {
        this.wallet = wallet;
        this.stockHoldings = new HashMap<>(stockAmount);
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(wallet);
        sb.append(" ");
        for (Map.Entry<String, Integer> entry: stockHoldings.entrySet()) {
            sb.append(entry.getKey());
            sb.append(":");
            sb.append(entry.getValue());
            sb.append(" ");
        }
        return sb.toString();
    }

    public int getWallet() {
        return wallet;
    }

    public int getStockHoldings(String stockId) {
        return stockHoldings.get(stockId);
    }

    public abstract boolean wantsToPlaceOrder(StockMarket s);

    public void executeTransaction(int income, int stockAmount, String stockId) {
        wallet += income;
        this.stockHoldings.put(stockId, stockHoldings.getOrDefault(stockId, 0) + stockAmount);
    }

    public abstract Order addOrder(StockMarket s);



}
