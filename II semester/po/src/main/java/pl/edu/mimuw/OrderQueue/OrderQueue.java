package pl.edu.mimuw.OrderQueue;

import pl.edu.mimuw.Orders.Order;

import java.util.PriorityQueue;


public class OrderQueue {
    private int currentTurn;
    private int nextOrderNumber;
    private PriorityQueue<Order> buyOrder;
    private PriorityQueue<Order> sellOrder;
    private final String stockId;
    private int lastTransactionPrice;

    public OrderQueue(String stockId, int lastTransactionPrice){
        currentTurn = 0;
        nextOrderNumber = 0;
        buyOrder = new PriorityQueue<>();
        sellOrder = new PriorityQueue<>();
        this.stockId = stockId;
        this.lastTransactionPrice = lastTransactionPrice;
    }

    public int newTurn() {
        currentTurn++;
        nextOrderNumber = 0;
        // Usuwam zlecenia, które straciły ważność
        buyOrder = delete(buyOrder);
        sellOrder = delete(sellOrder);
        return lastTransactionPrice;
    }

    public void addOrder(Order order){
        order.setOrderNumber(nextOrderNumber++);
        if (order.isBuyOrder()) {
            buyOrder.add(order);
        }
        else {
            sellOrder.add(order);
        }
    }

    public void executeTurn(){
        //sort();
        boolean continueProcessing = true;
        do {
            if (removeFirst(buyOrder) || removeFirst(sellOrder)) {
                break;
            }
            //Biore pierwsze zlecenie z kupna i sprzedaży, które można wykonać.
            var firstBuy = buyOrder.peek();
            var firstSell = sellOrder.peek();
            if (firstBuy.canBeExecuted(firstSell)) {
                // Jeśli nie można zrealizować, to znaczy że dla następnych akcji też nie będzie można zrealizować.
                lastTransactionPrice = firstBuy.execute(firstSell);
            }
            else {
                continueProcessing = false;
            }
        } while(continueProcessing);
    }

    //Funkcja daje true jeśli lista jest pusta i usuwa wszystkie pierwsze elementy, których nie można realizować.
    private boolean removeFirst(PriorityQueue<Order> z) {
        while (!z.isEmpty() && z.peek().canEliminate(this, 0, 0, 0)) {
            z.poll();
        }
        return z.isEmpty();
    }

    //Funkcja usuwa wszystkie zlecenia których nie można realizować
    private PriorityQueue<Order> delete(PriorityQueue<Order> orderQueue) {
        var newOrderQueue = new PriorityQueue<>(orderQueue);
        for (Order z : orderQueue) {
            if (z.canEliminate(this, 0, 0, 0))
                newOrderQueue.remove(z);
        }
        return newOrderQueue;
    }

    public int getCurrentTurn() {
        return currentTurn;
    }

    public PriorityQueue<Order> getOrderQueue(boolean isBuyOrder) {
        if (isBuyOrder)
            return buyOrder;
        else
            return sellOrder;
    }
}
