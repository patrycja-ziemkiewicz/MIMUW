package pl.edu.mimuw.StockMarket;



public class InvalidData extends Exception{
    public static class InvalidStockId extends InvalidData {}
    public static class InvalidInvestorType extends InvalidData {}
    public static class InvalidStockInWallet extends InvalidData {}
    public static class InvalidDataLength extends InvalidData {}

}
