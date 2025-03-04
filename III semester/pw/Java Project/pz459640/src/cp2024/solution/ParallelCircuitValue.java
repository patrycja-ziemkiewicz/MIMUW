package cp2024.solution;

import cp2024.circuit.CircuitValue;
import java.util.concurrent.*;

public class ParallelCircuitValue implements CircuitValue {
    private final Future<Boolean> future;

    public ParallelCircuitValue(Future<Boolean> future) {
        this.future = future;
    }

    @Override
    public boolean getValue() throws InterruptedException {
        try {
            return future.get();
        }
        catch (InterruptedException | ExecutionException | CancellationException e) {
            throw new InterruptedException();
        }
    }
}
