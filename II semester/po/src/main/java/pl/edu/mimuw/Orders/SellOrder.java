package pl.edu.mimuw.Orders;

import pl.edu.mimuw.Investors.Investor;

public class SellOrder extends OrderType {
    public SellOrder(String stockId, int quantity, int priceLimit, int turn, Investor investor) {
        super(stockId, quantity, priceLimit, turn, investor);
    }

    @Override
    protected int compare(OrderType o) {
        if (o instanceof SellOrder) {
            return priceLimit.compareTo(o.priceLimit);
        }
        return 0;
    }

    @Override
    protected void execute(int quantity, int price) {
        investor.executeTransaction(quantity * price, -quantity, stockId);
        this.quantity -= quantity;
    }

    @Override
    protected boolean canBeExecuted(OrderType z) {
        if (z instanceof BuyOrder) {
            return priceLimit <= z.priceLimit;
        }
        return false;
    }

    //Eliminuje zlecenie w momencie, gdy inwestor nie jest wstanie go zrealizować lub zostało zrealizowane
    // w całości.
    @Override
    protected boolean canEliminate() {
        if (quantity > investor.getStockHoldings(stockId))
            return true;
        else if (quantity == 0)
            return true;
        return false;
    }
}
