package hu.sed.soda.instrumenter;

import java.util.concurrent.atomic.AtomicInteger;

public final class IDFactory {
  
  private static final class Holder {
    static final IDFactory INSTANCE = new IDFactory();
  }

  private AtomicInteger id = new AtomicInteger(0);

  private IDFactory() {
  }

  public static IDFactory getInstance() {
    return Holder.INSTANCE;
  }

  public int createId() {
    return id.getAndIncrement();
  }

}
