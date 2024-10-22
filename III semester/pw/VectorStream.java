package lab01.examples;


import java.util.Arrays;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;
import java.util.function.IntBinaryOperator;

public class VectorStream {
    private static final int STREAM_LENGTH = 10;
    private static final int VECTOR_LENGTH = 100;
    private static int VectorSum = 0;
    private static final int[] vector = new int[VECTOR_LENGTH];
    private static int counter;
    private static final CyclicBarrier barrier = new CyclicBarrier(VECTOR_LENGTH, VectorStream :: Sum);

    private static void Sum() {
        VectorSum = 0;
        for (int x : vector) {
            VectorSum += x;
        }
        System.out.println(counter + " -> " + VectorSum);
        counter++;
    }
    /**
     * Function that defines how vectors are computed: the i-th element depends on
     * the previous sum and the index i.
     * The sum of elements in the previous vector is initially given as zero.
     */
    private final static IntBinaryOperator vectorDefinition = (previousSum, i) -> {
        int a = 2 * i + 1;
        return (previousSum / VECTOR_LENGTH + 1) * (a % 4 - 2) * a;
    };

    private static void computeVectorStreamSequentially() {
        int[] vector = new int[VECTOR_LENGTH];
        int sum = 0;
        for (int vectorNo = 0; vectorNo < STREAM_LENGTH; ++vectorNo) {
            for (int i = 0; i < VECTOR_LENGTH; ++i) {
                vector[i] = vectorDefinition.applyAsInt(sum, i);
            }
            sum = 0;
            for (int x : vector) {
                sum += x;
            }
            System.out.println(vectorNo + " -> " + sum);
        }
    }

    private static class Helper implements Runnable {
        private final int i;

        public Helper(int i) {
            this.i = i;
        }

        public void run(){
            try {
                for (int vectorNo = 0; vectorNo < STREAM_LENGTH; vectorNo++) {
                    if (Thread.interrupted()) {
                        throw new InterruptedException();
                    }
                    vector[i] = vectorDefinition.applyAsInt(VectorSum, i);
                    barrier.await();
                }
            } catch (InterruptedException | BrokenBarrierException e) {
                System.err.println(Thread.currentThread().getName() + " interrupted.");
            }
        }

    }

    private static void computeVectorStreamInParallel() throws InterruptedException {
        // FIXME: implement, using VECTOR_LENGTH threads.
            Thread[] threads = new Thread[VECTOR_LENGTH];
            for (int i = 0; i < VECTOR_LENGTH; ++i) {
                threads[i] = new Thread(new Helper(i));
                threads[i].start();
            }
            try {
                for (Thread t : threads)
                    t.join();

            } catch(InterruptedException e) {
                System.err.println(Thread.currentThread().getName() + " interrupted.");
                for (Thread t : threads)
                    t.interrupt();
                throw e;
            }

    }

    public static void main(String[] args) {
        try {
            System.out.println("-- Sequentially --");
            computeVectorStreamSequentially();
            System.out.println("-- Parallel --");
            computeVectorStreamInParallel();
            System.out.println("-- End --");
        } catch (InterruptedException e) {
            System.err.println("Main interrupted.");
        }
    }
}
