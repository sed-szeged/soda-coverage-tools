package clover2soda.exceptions;

public class MethodNotFoundException extends Exception {

  private static final long serialVersionUID = 1022988900114981648L;

  public MethodNotFoundException() {
    super();
  }

  public MethodNotFoundException(String message) {
    super(message);
  }

  public MethodNotFoundException(String message, Throwable cause) {
    super(message, cause);
  }

}
