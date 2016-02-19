package clover2soda.exceptions;

public class AmbiguousMethodException extends Exception {

  private static final long serialVersionUID = -8004003430581783398L;

  public AmbiguousMethodException() {
    super();
  }

  public AmbiguousMethodException(String message) {
    super(message);
  }

  public AmbiguousMethodException(String message, Throwable cause) {
    super(message, cause);
  }

}
