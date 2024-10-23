package pl.edu.mimuw;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import pl.edu.mimuw.Investors.RANDOM;
import pl.edu.mimuw.StockMarket.InvalidData;
import pl.edu.mimuw.StockMarket.StockMarket;

import java.io.FileNotFoundException;
import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.assertNull;

public class OrderTests {
    private static RANDOM random;
    private static StockMarket s;

    @BeforeAll
    public static void setData() throws InvalidData.InvalidStockId, InvalidData.InvalidStockInWallet,
            InvalidData.InvalidInvestorType, InvalidData.InvalidDataLength,
            FileNotFoundException {
        s = new StockMarket("plik.txt", 10000);
        random = new RANDOM();
    }

    @Test
    void normalTest()  {
        var map = new HashMap<String, Integer>();
        map.put("APL", 100);
        map.put("GOOGL", 100);
        map.put("MSFT", 100);
        random.SetWallet(1000, map);
        assert(random.addOrder(s) != null);
    }

    @Test
    void onlyBuy()  {
        var map = new HashMap<String, Integer>();
        map.put("APL", 0);
        map.put("GOOGL", 0);
        map.put("MSFT", 0);
        random.SetWallet(1000, map);
        assert(random.addOrder(s).isBuyOrder());
    }

    @Test
    void onlySell() {
        var map = new HashMap<String, Integer>();
        map.put("APL", 45);
        map.put("GOOGL", 20);
        map.put("MSFT", 10);
        random.SetWallet(0, map);
        assert(!random.addOrder(s).isBuyOrder());
    }

    @Test
    void onlySellAPL() {
        var mapa = new HashMap<String, Integer>();
        mapa.put("APL", 45);
        mapa.put("GOOGL", 0);
        mapa.put("MSFT", 0);
        random.SetWallet(0, mapa);
        assert(random.addOrder(s).stockId() == "APL" && !random.addOrder(s).isBuyOrder());
    }

    @Test
    void onlyBuyGOOGL() {
        var map = new HashMap<String, Integer>();
        map.put("APL", 0);
        map.put("GOOGL", 0);
        map.put("MSFT", 0);
        random.SetWallet(3, map);
        assert(random.addOrder(s).stockId() == "GOOGL" && random.addOrder(s).isBuyOrder());
    }

    @Test
    void noOrder() {
        var map = new HashMap<String, Integer>();
        map.put("APL", 0);
        map.put("GOOGL", 0);
        map.put("MSFT", 0);
        random.SetWallet(0, map);
        assert(!random.wantsToPlaceOrder(s));
    }

    @Test
    void priceTest() {
        var map = new HashMap<String, Integer>();
        map.put("APL", 10);
        map.put("GOOGL", 10);
        map.put("MSFT", 10);
        random.SetWallet(100000, map);
        var newOrder = random.addOrder(s);
        var limit = s.getLastStockPrice(newOrder.stockId());
        assert(newOrder.gerPriceLimit() <= limit + 10 && newOrder.gerPriceLimit() >= limit - 10);
    }

    @Test
    void BuyOrderQuantityTest() {
        var map = new HashMap<String, Integer>();
        map.put("APL", 0);
        map.put("GOOGL", 0);
        map.put("MSFT", 0);
        random.SetWallet(100000, map);
        var newOrder = random.addOrder(s);
        assert(newOrder.gerPriceLimit() * newOrder.getQuantity() <= random.getWallet());
    }

    @Test
    void SellOrderQuantityTest() {
        var map = new HashMap<String, Integer>();
        map.put("APL", 1430);
        map.put("GOOGL", 100);
        map.put("MSFT", 10);
        random.SetWallet(0, map);
        var newOrder = random.addOrder(s);
        assert(newOrder.getQuantity() <= random.getStockHoldings(newOrder.stockId()));
    }






}
