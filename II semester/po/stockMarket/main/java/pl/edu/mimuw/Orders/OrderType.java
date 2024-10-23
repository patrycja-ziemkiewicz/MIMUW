package pl.edu.mimuw.Orders;

import pl.edu.mimuw.Investors.Investor;

// Zlecenie Kupna lub Sprzedaży, możemy tworzyć tylko za pośrednictwem klasy Zlecenie.
public abstract class OrderType implements Comparable<OrderType>{
    protected final String stockId;
    protected int quantity;
    protected final Integer priceLimit;
    protected final Integer turn;
    protected Integer OrderId;
    protected final Investor investor;

    protected OrderType(String stockId, int quantity, int priceLimit, int turn, Investor investor) {
        this.stockId = stockId;
        this.quantity = quantity;
        this.priceLimit = priceLimit;
        this.turn = turn;
        this.investor = investor;
    }

    protected void setOrderId(int orderId) {
        this.OrderId = orderId;
    }

    // Funkcja pomocnicz do metody compareTo.
    protected abstract int compare(OrderType o);

    @Override
    public int compareTo(OrderType o) {
        if (this.compare(o) != 0) {
            return this.compare(o);
        }
        else if (!this.turn.equals(o.turn)) {
            return turn.compareTo(o.turn);
        }
        return OrderId.compareTo(o.OrderId);
    }

    protected Integer getTurn() {
        return turn;
    }

    protected abstract void execute(int ile, int cena);

    // Funkcja sprawdzająca czy zlecenie można realizować tzw. czy cena kupna jest większa równa od sprzedaży.
    protected abstract boolean canBeExecuted(OrderType z);

    // Funkcja zwraca cenę za jaką wykonana została transakcja.
    protected int execute(OrderType z) {
        int price;
        // Wybieram cenę za którą, będą realizowane dane zlecenia.
        if (this.compareTo(z) < 0)
            price = priceLimit;
        else
            price = z.priceLimit;
        // Realizowane w całości jest zlecenie o mniejszejszej ilości akcji.
        if (quantity <= z.quantity) {
            z.execute(quantity, price);
            this.execute(quantity, price);
        }
        else {
            this.execute(z.quantity, price);
            z.execute(z.quantity, price);
        }
        return price;
    }

    public int getQuantity() {
        return quantity;
    }

    protected abstract boolean canEliminate();

    public String getStockId() {
        return stockId;
    }

    public Integer getPriceLimit() {
        return priceLimit;
    }

}