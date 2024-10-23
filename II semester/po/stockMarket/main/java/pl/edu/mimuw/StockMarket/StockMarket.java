package pl.edu.mimuw.StockMarket;

import pl.edu.mimuw.OrderQueue.OrderQueue;
import pl.edu.mimuw.Investors.Investor;
import pl.edu.mimuw.Investors.RANDOM;
import pl.edu.mimuw.Investors.SMA;
import pl.edu.mimuw.StockMarket.InvalidData.*;


import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class StockMarket {
    private int numberOfTurns;
    private int currentTurn;
    private ArrayList<Investor> investors;
    private HashMap<String, OrderQueue> orderQueues;
    private HashMap<String, Integer> lastStockPrice;
    private smaCalculator SMACalculator;

    public StockMarket(String fileName, int numberOfTurns) throws FileNotFoundException, InvalidInvestorType,
            InvalidDataLength, InvalidStockId, InvalidStockInWallet {
        this.numberOfTurns = numberOfTurns;
        currentTurn = 0;
        SMACalculator = new smaCalculator();
        var file = new FileReader(fileName);
        // Wczytywanie danych z pliku.
        try (Scanner sc = new Scanner(file)) {
            loadInvestors(sc);
            loadStocks(sc);
            loadWallet(sc);
        }

        orderQueues = new HashMap<>(lastStockPrice.size());
        for (String stockId: lastStockPrice.keySet()) {
            orderQueues.put(stockId, new OrderQueue(stockId, lastStockPrice.get(stockId)));
        }

    }

    // Funkcja pyta inwestorów czy chcą dodać zlecenie, jeśli odpowiedzą pozytywnie to dodaje ich zlecenie
    // do arkusza zleceń.
    private void askInvestors() {
        Collections.shuffle(investors);
        for (Investor i : investors) {
            if (i.wantsToPlaceOrder(this)) {
                var newOrder = i.addOrder(this);
                orderQueues.get(newOrder.stockId()).addOrder(newOrder);
            }
        }
    }

    public void executeTurn() {
        askInvestors();
        currentTurn++;
        for(Map.Entry<String, OrderQueue> entry: orderQueues.entrySet()) {
            entry.getValue().executeTurn();
            lastStockPrice.put(entry.getKey(), entry.getValue().newTurn());
        }
        SMACalculator.update(lastStockPrice, currentTurn);
    }

    private void printInvestors() {
        for (Investor i : investors)
            System.out.println(i);
    }

    public smaCalculator getSMACalculator() {
        return SMACalculator;
    }

    private void printLastStockPrices() {
        for (Map.Entry<String, Integer> entry : lastStockPrice.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
    }

    public void runSimulation() {
        for (int i = 0; i < numberOfTurns; i++) {
            executeTurn();
        }
        printInvestors();
        //WypiszOstatnieCeny();
    }

    public int getLastStockPrice(String stockId) {
        return lastStockPrice.get(stockId);
    }

    public int getCurrentTurn() {
        return currentTurn;
    }

    private void loadInvestors(Scanner sc) throws InvalidInvestorType, InvalidDataLength {
        String line;
        while (sc.hasNextLine()) {
            line = sc.nextLine();
            if (!line.startsWith("#")) {
                // Ignoruj linie rozpoczynające się od '#'
                String[] split = line.split(" ");
                investors = new ArrayList<>(split.length);
                for (String p : split) {
                    switch (p) {
                        case "R":
                            investors.add(new RANDOM());
                            break;
                        case "S":
                            investors.add(new SMA(SMACalculator));
                            break;
                        default:
                            throw new InvalidInvestorType();
                    }
                }
                return;
            }
        }
        throw new InvalidDataLength();
    }

    private void loadStocks(Scanner sc) throws InvalidStockId, InvalidDataLength {
        String line;
        while (sc.hasNextLine()) {
            line = sc.nextLine();
            if (!line.startsWith("#")) {
                String[] split = line.split(" ");
                Pattern pattern = Pattern.compile("([A-Z]{1,5}):([1-9][0-9]*)");
                lastStockPrice = new HashMap<>();
                for (String p: split) {
                    Matcher matcher = pattern.matcher(p);
                    if (matcher.matches()) {
                        lastStockPrice.put(matcher.group(1), Integer.parseInt(matcher.group(2)));
                    }
                    else
                        throw new InvalidStockId();
                }
                SMACalculator.UstawKalkulatorSMA(lastStockPrice);
                return;
            }
        }
        throw new InvalidDataLength();
    }

    private void loadWallet(Scanner sc) throws InvalidStockInWallet, InvalidDataLength {
        String line;
        while (sc.hasNextLine()) {
            line = sc.nextLine();
            if (!line.startsWith("#")) {
                int wallet;
                var numberOfStocks = new HashMap<String, Integer>(lastStockPrice.size());
                //Najpierw dziele wczytaną linię na dwie części oddzielone spacją
                String[] split = line.split(" ", 2);
                Pattern pattern1 = Pattern.compile("([1-9][0-9]*)");
                Pattern pattern2 = Pattern.compile("([A-Z]{1,5}):([1-9][0-9]*)");
                Matcher matcher1 = pattern1.matcher(split[0]);
                if (matcher1.matches())
                    wallet = Integer.parseInt(split[0]);
                else
                    throw new InvalidStockInWallet();
                String[] splits = split[1].split(" ");
                for (String p: splits) {
                    Matcher matcher = pattern2.matcher(p);
                    if (matcher.matches() && lastStockPrice.containsKey(matcher.group(1))) {
                        numberOfStocks.put(matcher.group(1), Integer.parseInt(matcher.group(2)));
                    }
                    else
                        throw new InvalidStockInWallet();
                }
                //Dodaje akcję, które nie pojawiły się w pliku i ustawiam ich wartość na 0 dla każdego inwestora
                for (String stockId: lastStockPrice.keySet()) {
                    if (!numberOfStocks.containsKey(stockId))
                        numberOfStocks.put(stockId, 0);
                }
                for (Investor i : investors) {
                    i.SetWallet(wallet, numberOfStocks);
                }
                return;
            }
        }
        throw new InvalidDataLength();
    }

    public OrderQueue getOrderQueue(String stockId) {
        return orderQueues.get(stockId);
    }

    public HashMap<String, Integer> getLastStockPrice() {
        return lastStockPrice;
    }
}
