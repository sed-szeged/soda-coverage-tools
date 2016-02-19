package clover2soda;

public class Mutant {

  public static final int C_ID = 0;
  public static final int C_METHOD = 4;
  public static final int C_LINE = 5;

  private int id;
  private String method;
  private int line;

  public Mutant(int id, String method, int line) {
    super();
    this.id = id;
    this.method = method;
    this.line = line;
  }

  public int getId() {
    return id;
  }

  public String getMethod() {
    return method;
  }

  public int getLine() {
    return line;
  }

  public static Mutant createFromLog(String logLine) throws Exception {
    try {
      String[] columns = logLine.split(":");

      int id = Integer.valueOf(columns[C_ID]);
      String method = columns[C_METHOD].replaceAll("@", ".").replaceAll("\\.", "/");
      int line = Integer.valueOf(columns[C_LINE]);

      return new Mutant(id, method, line);
    } catch (ArrayIndexOutOfBoundsException | NumberFormatException e) {
      throw new Exception(String.format("Cannot parse line '%s': %s", logLine, e));
    }
  }

  @Override
  public String toString() {
    return "Mutant [id=" + id + ", method=" + method + ", line=" + line + "]";
  }

  @Override
  public int hashCode() {
    return id;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj)
      return true;
    if (obj == null)
      return false;
    if (getClass() != obj.getClass())
      return false;
    Mutant other = (Mutant) obj;
    if (id != other.id)
      return false;
    return true;
  }

}
