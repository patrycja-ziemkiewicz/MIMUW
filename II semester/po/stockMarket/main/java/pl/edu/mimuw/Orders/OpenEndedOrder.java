package pl.edu.mimuw.Orders;

import pl.edu.mimuw.Investors.Investor;

public class OpenEndedOrder extends Order {
    public OpenEndedOrder(String stockId, int Quantity, int priceLimit, int turn, Investor investor, boolean isBuyOrder) {
        super(stockId, Quantity, priceLimit,turn, investor, isBuyOrder);

    }


}
