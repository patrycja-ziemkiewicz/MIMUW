package pl.edu.mimuw.Orders;

import pl.edu.mimuw.OrderQueue.OrderQueue;
import pl.edu.mimuw.Investors.Investor;

public abstract class Order implements Comparable<Order> {
    protected OrderType order;

    public Order(String stockId, int quantity, int priceLimit, int turn, Investor investor, boolean isBuyOrder) {
        if (isBuyOrder) {
            order = new BuyOrder(stockId,quantity,priceLimit,turn, investor);
        }
        else {
            order = new SellOrder(stockId,quantity,priceLimit,turn, investor);
        }
    }

    public int compareTo(Order o) {
        return order.compareTo(o.order);
    }

    public boolean isBuyOrder() {
        return (order instanceof BuyOrder);
    }

    public void setOrderNumber(int orderId) {
        order.setOrderId(orderId);
    }

    // index1, index2, previousOrderQuantity używam w klasie DoOrCancelOrder.
    public boolean canEliminate(OrderQueue orderQueue, int index1, int index2, int previousOrderQuantity) {
        return order.canEliminate();
    }

    public int execute(Order newOrder) {
           return order.execute(newOrder.order);
    }

    public boolean canBeExecuted(Order z) {
        return order.canBeExecuted(z.order);
    }

    public String stockId(){
        return order.getStockId();
    }

    public int gerPriceLimit() {
        return order.getPriceLimit();
    }


    public int getQuantity() {
        return order.getQuantity();
    }


}
