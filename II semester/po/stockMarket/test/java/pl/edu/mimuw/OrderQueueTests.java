package pl.edu.mimuw;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import pl.edu.mimuw.OrderQueue.OrderQueue;
import pl.edu.mimuw.Investors.RANDOM;
import pl.edu.mimuw.StockMarket.InvalidData;
import pl.edu.mimuw.StockMarket.StockMarket;
import pl.edu.mimuw.Orders.DoOrCancelOrder;
import pl.edu.mimuw.Orders.OpenEndedOrder;
import pl.edu.mimuw.Orders.InstantOrder;
import pl.edu.mimuw.Orders.TimeLimitedOrder;

import java.io.FileNotFoundException;
import java.util.HashMap;

public class OrderQueueTests {
    private static OrderQueue a;
    private static RANDOM random;
    private static RANDOM random2;

    @BeforeAll
    public static void setData() throws InvalidData.InvalidStockId, InvalidData.InvalidStockInWallet,
            InvalidData.InvalidInvestorType, InvalidData.InvalidDataLength,
            FileNotFoundException {
        var s = new StockMarket("plik.txt", 20);
        s.runSimulation();
        a = s.getOrderQueue("APL");
        random = new RANDOM();
        random2 = new RANDOM();
        var map = new HashMap<String, Integer>();
        map.put("APL", 100);
        map.put("GOOGL", 100);
        map.put("MSFT", 100);
        random.SetWallet(1000, map);
        random2.SetWallet(1000, map);
    }


    @Test
    public void OrdersEliminating1() {
        var arkusz = new OrderQueue("APL", 10);
        for (int i = 0; i < 10; i++) {
            arkusz.addOrder(new OpenEndedOrder("APL", 1, 1,
                    1, random, true));
        }
        arkusz.executeTurn();
        arkusz.newTurn();
        assert(arkusz.getOrderQueue(true).size() == 10);
    }

    @Test
    public void OrdersEliminating2() {
        var arkusz = new OrderQueue("APL", 10);
        for (int i = 0; i < 10; i++) {
            arkusz.addOrder(new OpenEndedOrder("APL", 1, 1,
                    0, random, true));
            arkusz.addOrder(new InstantOrder("APL", 1, 1,
                    0, random, true));
        }
        assert(arkusz.getOrderQueue(true).size() == 20);
        arkusz.newTurn();
        assert(arkusz.getOrderQueue(true).size() == 10);
    }

    @Test
    public void orderEliminating3() {
        var arkusz = new OrderQueue("APL", 10);
        for (int i = 0; i < 10; i++) {
            arkusz.addOrder(new OpenEndedOrder("APL", 1, 1,
                    0, random, true));
            arkusz.addOrder(new TimeLimitedOrder("APL", 1, 1,
                    0, random, true, 1));
        }
        assert(arkusz.getOrderQueue(true).size() == 20);
        arkusz.newTurn();
        arkusz.newTurn();
        assert(arkusz.getOrderQueue(true).size() == 10);
    }

    @Test
    public void orderEliminating4() {
        var orderQueue = new OrderQueue("APL", 10);
        var map = new HashMap<String, Integer>();
        map.put("APL", 0);
        map.put("GOOGL", 0);
        map.put("MSFT", 0);
        random.SetWallet(1000, map);
        for (int i = 0; i < 10; i++) {
            orderQueue.addOrder(new OpenEndedOrder("APL", 1, 1,
                    1, random, false));
        }
        orderQueue.executeTurn();
        assert(orderQueue.getOrderQueue(true).isEmpty());
    }

    @Test
    public void orderEliminating5() {
        var orderQueue = new OrderQueue("APL", 10);
        var map = new HashMap<String, Integer>();
        map.put("APL", 30);
        map.put("GOOGL", 30);
        map.put("MSFT", 30);
        for (int i = 0; i < 10; i++) {
            orderQueue.addOrder(new OpenEndedOrder("APL", 1, 1,
                    1, random, true));
        }
        orderQueue.newTurn();
        assert(orderQueue.getOrderQueue(true).size() == 10);
        random.SetWallet(0, map);
        orderQueue.newTurn();
        assert(orderQueue.getOrderQueue(true).isEmpty());
    }

    @Test
    public void orderEliminating6() {
        var orderQueue = new OrderQueue("APL", 10);
        var map = new HashMap<String, Integer>();
        map.put("APL", 0);
        map.put("GOOGL", 0);
        map.put("MSFT", 0);
        for (int i = 0; i < 10; i++) {
            orderQueue.addOrder(new OpenEndedOrder("APL", 1, 1,
                    1, random, false));
        }
        orderQueue.newTurn();
        assert(orderQueue.getOrderQueue(false).size() == 10);
        random.SetWallet(1000, map);
        orderQueue.newTurn();
        assert(orderQueue.getOrderQueue(false).isEmpty());
    }

    @Test
    public void orderExecuting1() {
        var orderQueue = new OrderQueue("APL", 10);
        for (int i = 0; i < 10; i++) {
            orderQueue.addOrder(new OpenEndedOrder("APL", 1, 1,
                    1, random, false));
            orderQueue.addOrder(new OpenEndedOrder("APL", 1, 1,
                    1, random, true));
        }
        orderQueue.executeTurn();
        orderQueue.newTurn();
        assert(orderQueue.getOrderQueue(true).isEmpty()
                && orderQueue.getOrderQueue(false).isEmpty());
    }

    @Test
    public void orderExecuting2() {
        var orderQueue = new OrderQueue("APL", 10);
        for (int i = 0; i < 10; i++) {
            orderQueue.addOrder(new OpenEndedOrder("APL", 2, 1,
                    1, random, false));
            orderQueue.addOrder(new OpenEndedOrder("APL", 1, 1,
                    1, random, true));
        }
        orderQueue.executeTurn();
        orderQueue.newTurn();
        assert(orderQueue.getOrderQueue(false).size() == 5 &&
                orderQueue.getOrderQueue(true).isEmpty());
    }

    @Test
    public void orderExecuting3() {
        var orderQueue = new OrderQueue("APL", 10);
        for (int i = 0; i < 10; i++) {
            orderQueue.addOrder(new OpenEndedOrder("APL", 1, 10,
                    1, random, false));
            orderQueue.addOrder(new OpenEndedOrder("APL", 1, 1,
                    1, random, true));
        }
        orderQueue.executeTurn();
        orderQueue.newTurn();
        assert(orderQueue.getOrderQueue(false).size() == 10 &&
                orderQueue.getOrderQueue(true).size() == 10 );
    }

    @Test
    public void DoOrCancelOrders1() {
        var orderQueue = new OrderQueue("APL", 10);
        var p1 = random.getWallet();
        var p2 = random2.getWallet();
        for (int i = 0; i < 10; i++) {
            orderQueue.addOrder(new DoOrCancelOrder("APL", 1, 1,
                    0, random, false));
            orderQueue.addOrder(new DoOrCancelOrder("APL", 1, 1,
                    0, random2, true));
        }
        orderQueue.executeTurn();
        assert (random2.getWallet() == p2 - 10 && random.getWallet() == p1 + 10);
    }

    @Test
    public void DoOrCancelOrders2() {
        var orderQueue = new OrderQueue("APL", 10);
        var order = new DoOrCancelOrder("APL", 30, 1,
                0, random, false);
        var order2 = new DoOrCancelOrder("APL", 30, 1,
                0, random, true);
        orderQueue.addOrder(order2);
        orderQueue.addOrder(order);
        assert(!order2.canEliminate(orderQueue, 0, 0, 0) &&
                !order.canEliminate(orderQueue, 0, 0, 0));
    }

    @Test
    public void DoOrCancelOrders3() {
        var orderQueue = new OrderQueue("APL", 10);
        var p1 = random.getWallet();
        var p2 = random2.getWallet();
        var order = new DoOrCancelOrder("APL", 3, 1,
                0, random, false);
        var order2 = new OpenEndedOrder("APL", 30, 1,
                0, random2, true);
        orderQueue.addOrder(order);
        orderQueue.addOrder(order2);
        orderQueue.executeTurn();
        assert(random.getWallet() == p1 + 3 && random2.getWallet() == p2 - 3);
    }

    @Test
    public void DoOrCancelOrders4() {
        var orderQueue = new OrderQueue("APL", 10);
        var order = new DoOrCancelOrder("APL", 20, 1,
                0, random, false);
        var order2 = new DoOrCancelOrder("APL", 30, 1,
                0, random, true);
        orderQueue.addOrder(order2);
        orderQueue.addOrder(order);
        assert(order2.canEliminate(orderQueue, 0, 0, 0) &&
                order.canEliminate(orderQueue, 0, 0, 0));
    }

    @Test
    public void DoOrCancelOrders5() {
        var orderQueue = new OrderQueue("APL", 10);
        var order = new DoOrCancelOrder("APL", 20, 1,
                0, random, false);
        var order2 = new OpenEndedOrder("APL", 10, 1,
                0, random, true);
        orderQueue.addOrder(order2);
        orderQueue.addOrder(order);
        assert(!order2.canEliminate(orderQueue, 0, 0, 0) &&
                order.canEliminate(orderQueue, 0, 0, 0));
    }

    @Test
    public void DoOrCancelOrders6() {
        var orderQueue = new OrderQueue("APL", 10);
        var p1 = random.getWallet();
        var p2 = random2.getWallet();
        for (int i = 0; i < 10; i++) {
            orderQueue.addOrder(new DoOrCancelOrder("APL", 3, 1,
                    0, random, false));
            orderQueue.addOrder(new DoOrCancelOrder("APL", 1, 1,
                    0, random2, true));
        }
        orderQueue.executeTurn();
        assert (random2.getWallet() == p2 - 9 && random.getWallet() == p1 + 9);
    }

}

