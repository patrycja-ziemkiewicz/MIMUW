package cp2024.solution;

import cp2024.circuit.*;


import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;

public class ParallelCircuitSolver implements CircuitSolver {
    private final AtomicBoolean acceptComputations;
    private final ExecutorService pool;

    public ParallelCircuitSolver () {
        this.pool = Executors.newCachedThreadPool();
        this.acceptComputations = new AtomicBoolean(true);
    }

    @Override
    public CircuitValue solve(Circuit c) {
        if (!acceptComputations.get())
            return new ParallelCircuitValueInterrupted();
        List<Future<Boolean>> future = new ArrayList<>(1);
        try {
            ParallelComputing solver = new ParallelComputing(c.getRoot());
            future.add(pool.submit(solver));
            return new ParallelCircuitValue(future.get(0));
        }
        catch (InterruptedException | RejectedExecutionException e) {
            cancelFutures(future);
            return new ParallelCircuitValueInterrupted();
        }
    }

    @Override
    public void stop() {
        if (acceptComputations.compareAndSet(true, false))
            pool.shutdownNow();
    }

    private class ParallelComputing implements Callable<Boolean> {
        private final CircuitNode n;
        private final CircuitNode[] args;

        public ParallelComputing(CircuitNode n) throws InterruptedException {
            this.n = n;
            this.args = n.getArgs();
        }

        @Override
        public Boolean call() throws InterruptedException {
            if (Thread.interrupted()) {
                throw new InterruptedException();
            }

            if (n.getType() == NodeType.LEAF)
                return ((LeafNode) n).getValue();

            return switch (n.getType()) {
                case IF -> solveIF(args);
                case AND -> solveAND(args);
                case OR -> solveOR(args);
                case GT -> solveGT(args, ((ThresholdNode) n).getThreshold());
                case LT -> solveLT(args, ((ThresholdNode) n).getThreshold());
                case NOT -> solveNOT(args);
                default -> throw new InterruptedException();

            };
        }

        private boolean solveAND(CircuitNode[] args) throws InterruptedException {
            CompletionService<Boolean> completionService = new ExecutorCompletionService<>(pool);
            List<Future<Boolean>> futures = new ArrayList<>(args.length);
            try {
                for (CircuitNode c : args) {
                    futures.add(completionService.submit(new ParallelComputing(c)));
                }
                for (int i = 0; i < args.length; ++i) {
                    Future<Boolean> future = completionService.take();
                    if (!future.get()) {
                        cancelFutures(futures);
                        return false;
                    }
                }
                return true;
            } catch (InterruptedException | ExecutionException | RejectedExecutionException e) {
                cancelFutures(futures);
                throw new InterruptedException();
            }
        }

        private boolean solveOR(CircuitNode[] args) throws InterruptedException {
            CompletionService<Boolean> completionService = new ExecutorCompletionService<>(pool);
            List<Future<Boolean>> futures = new ArrayList<>(args.length);
            try {
                for (CircuitNode c : args) {
                    futures.add(completionService.submit(new ParallelComputing(c)));
                }
                for (int i = 0; i < args.length; ++i) {
                    Future<Boolean> future = completionService.take();
                    if (future.get()) {
                        cancelFutures(futures);
                        return true;
                    }
                }
                return false;
            } catch (InterruptedException | ExecutionException | RejectedExecutionException e) {
                cancelFutures(futures);
                throw new InterruptedException();
            }
        }

        private boolean solveGT(CircuitNode[] args, int threshold) throws InterruptedException {
            int n = args.length;
            if (threshold >= n) return false;
            CompletionService<Boolean> completionService = new ExecutorCompletionService<>(pool);
            List<Future<Boolean>> futures = new ArrayList<>(n);
            int gotTrue = 0, maximumFalse = n - threshold;
            try {
                for (CircuitNode c : args) {
                    futures.add(completionService.submit(new ParallelComputing(c)));
                }
                for (int i = 0; i < n; ++i) {
                    Future<Boolean> future = completionService.take();
                    if (future.get())
                        gotTrue++;
                    if (gotTrue > threshold) {
                        cancelFutures(futures);
                        return true;
                    } else if (i - gotTrue + 1 > maximumFalse) {
                        cancelFutures(futures);
                        return false;
                    }
                }
                return gotTrue > threshold;
            } catch (InterruptedException | ExecutionException | RejectedExecutionException e) {
                cancelFutures(futures);
                throw new InterruptedException();
            }

        }

        private boolean solveLT(CircuitNode[] args, int threshold) throws InterruptedException {
            int n = args.length;
            if (threshold > n) return true;
            if (threshold == 0) return false;
            CompletionService<Boolean> completionService = new ExecutorCompletionService<>(pool);
            List<Future<Boolean>> futures = new ArrayList<>(n);
            int gotTrue = 0, minimumFalse = n - threshold;
            try {
                for (CircuitNode c : args) {
                    futures.add(completionService.submit(new ParallelComputing(c)));
                }
                for (int i = 0; i < n; ++i) {
                    Future<Boolean> future = completionService.take();
                    if (future.get())
                        gotTrue++;
                    if (gotTrue > threshold) {
                        cancelFutures(futures);
                        return false;
                    } else if (i - gotTrue + 1 > minimumFalse) {
                        cancelFutures(futures);
                        return true;
                    }
                }
                return gotTrue < threshold;
            } catch (InterruptedException | ExecutionException | RejectedExecutionException e) {
                cancelFutures(futures);
                throw new InterruptedException();
            }
        }


        private boolean solveNOT(CircuitNode[] args) throws InterruptedException {
            return !(new ParallelComputing(args[0]).call());
        }

        private boolean solveIF(CircuitNode[] args) throws InterruptedException {
            List<Future<Boolean>> futures = new ArrayList<>(2);
            try {
                futures.add(pool.submit(new ParallelComputing(args[0])));
                if (futures.get(0).get())
                    futures.add(pool.submit(new ParallelComputing(args[1])));
                else
                    futures.add(pool.submit(new ParallelComputing(args[2])));
                return futures.get(1).get();
            } catch (InterruptedException | ExecutionException | RejectedExecutionException e) {
                cancelFutures(futures);
                throw new InterruptedException();
            }
        }
    }


    private void cancelFutures(List<Future<Boolean>> futures)  {
        for (Future<Boolean> future: futures)
            future.cancel(true);

        int i = 0, n = futures.size();
        while (i < n) {
            try {
                futures.get(i).get();
                i++;
            }

            catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            catch (CancellationException | ExecutionException e) {
                i++;
            }
        }

    }


}
