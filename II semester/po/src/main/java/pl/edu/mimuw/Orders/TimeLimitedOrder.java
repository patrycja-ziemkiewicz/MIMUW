package pl.edu.mimuw.Orders;

import pl.edu.mimuw.OrderQueue.OrderQueue;
import pl.edu.mimuw.Investors.Investor;

public class TimeLimitedOrder extends Order {
    private final int timeLimit;

    public TimeLimitedOrder(String stockId, int quantity, int priceLimit, int turn, Investor investor,
                            boolean isBuyOrder, int timeLimit) {
        super(stockId, quantity, priceLimit, turn, investor, isBuyOrder);
        this.timeLimit = timeLimit;

    }

    @Override
    public boolean canEliminate(OrderQueue orderQueue, int index1, int index2, int previousOrderQuantity) {
        if (orderQueue.getCurrentTurn() > timeLimit)
            return true;
        return super.canEliminate(orderQueue, index1, index2, previousOrderQuantity);
    }
}
