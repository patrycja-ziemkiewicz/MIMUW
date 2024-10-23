package pl.edu.mimuw.Orders;

import pl.edu.mimuw.OrderQueue.OrderQueue;
import pl.edu.mimuw.Investors.Investor;

public class InstantOrder extends Order {

    public InstantOrder(String stockId, int quantity, int priceLimit, int turn, Investor investor,
                        boolean isBuyOrder) {
        super(stockId, quantity, priceLimit,turn, investor, isBuyOrder);

    }

    @Override
    public boolean canEliminate(OrderQueue orderQueue, int index1, int index2, int previousOrderQuantity) {
        if (orderQueue.getCurrentTurn() != order.getTurn())
            return true;
        return super.canEliminate(orderQueue, index1, index2, previousOrderQuantity);

    }
}
