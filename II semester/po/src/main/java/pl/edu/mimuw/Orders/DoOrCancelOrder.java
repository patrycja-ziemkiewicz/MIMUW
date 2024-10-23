package pl.edu.mimuw.Orders;

import pl.edu.mimuw.OrderQueue.OrderQueue;
import pl.edu.mimuw.Investors.Investor;

import java.util.ArrayList;

public class DoOrCancelOrder extends Order {
    public DoOrCancelOrder(String stockId, int quantity, int priceLimit, int turn, Investor investor, boolean isBuyOrder) {
        super(stockId, quantity, priceLimit,turn, investor, isBuyOrder);
    }

    // Index2 to obecny indeks sprawdzanego zlecenia, index1 odpowiada indexowi od którego możemy
    // zacząć porównywanie zleceń. Funkcja rekurencyjnie dla każdego, zlecenia najpierw sprawdza
    // czy nie trzeba go eliminować a następnie czy można je wykonać z obecnie sprawdzanym zleceniem.
    // iloscPoprzedniegoZlecenia to liczba akcji, które nie zostaly zrealizowane jeszcze przez poprzednie zlecenie.
    @Override
    public boolean canEliminate(OrderQueue orderQueue, int index1, int index2, int previousOrderQuantity) {
        if (orderQueue.getCurrentTurn() != order.getTurn())
            return true;
        if (super.canEliminate(orderQueue, index1, index2, previousOrderQuantity))
            return true;
        var listOfOrders = new ArrayList<>(orderQueue.getOrderQueue(!isBuyOrder()));
        var quantityOfCopy = getQuantity() - previousOrderQuantity;
        if (quantityOfCopy <= 0) return false;
        for (int i = index1; i < listOfOrders.size(); i++) {
            if (!listOfOrders.get(i).canEliminate(orderQueue, index2 + 1, i, quantityOfCopy)) {
                if (listOfOrders.get(i).canBeExecuted(this))
                    quantityOfCopy -= listOfOrders.get(i).getQuantity();
                else
                    return true;
            }
            if (quantityOfCopy <= 0)
                return false;
        }
        return true;

    }


}
