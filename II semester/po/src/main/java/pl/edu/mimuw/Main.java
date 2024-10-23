package pl.edu.mimuw;

import pl.edu.mimuw.StockMarket.InvalidData.InvalidStockInWallet;
import pl.edu.mimuw.StockMarket.InvalidData.InvalidDataLength;
import pl.edu.mimuw.StockMarket.InvalidData.InvalidStockId;
import pl.edu.mimuw.StockMarket.InvalidData.InvalidInvestorType;
import pl.edu.mimuw.StockMarket.StockMarket;
import pl.edu.mimuw.InvalidParameters.*;
import java.io.FileNotFoundException;

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class Main {
    public static void main(String[] args) throws InvalidInvestorType,
            InvalidDataLength, InvalidStockId, InvalidStockInWallet, InvalidParameterCount,
            InvalidFirstParameter, InvalidSecondParameter {

        // Sprawdzam poprawną ilość parametrów.
        if (args.length < 2)
            throw new InvalidParameterCount();

        // Wykonuje program, jednocześnie wychwycając, błędy związane z niepoprawnymi parametrami.
        try {
            int numberOfTurns = Integer.parseInt(args[1]);
            var s = new StockMarket(args[0], numberOfTurns);
            s.runSimulation();
        } catch (NumberFormatException e) {
            throw new InvalidSecondParameter();
        } catch (FileNotFoundException e) {
            throw new InvalidFirstParameter();
        }

    }
}