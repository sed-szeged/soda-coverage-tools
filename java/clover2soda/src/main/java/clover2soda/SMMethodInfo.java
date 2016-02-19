package clover2soda;

import org.apache.commons.csv.CSVRecord;

public class SMMethodInfo {

  public static final String C_NAME = "Name";
  public static final String C_LONG_NAME = "LongName";
  public static final String C_PATH = "Path";
  public static final String C_LINE = "Line";
  public static final String C_END_LINE = "EndLine";

  private String name;
  private String longName;
  private String path;
  private int line;
  private int endLine;

  private SMMethodInfo(String name, String longName, String path, int line, int endLine) {
    this.name = name;
    this.longName = longName;
    this.path = path;
    this.line = line;
    this.endLine = endLine;
  }

  public String getName() {
    return name;
  }

  public String getLongName() {
    return longName;
  }

  public String getPath() {
    return path;
  }

  public long getLine() {
    return line;
  }

  public int getEndLine() {
    return endLine;
  }

  public static SMMethodInfo createFromCSV(CSVRecord record) {
    String name = record.get(C_NAME);
    String longName = record.get(C_LONG_NAME).replaceAll("\\.", "/").replaceAll(";", ",");
    String path = record.get(C_PATH);
    int line = Integer.valueOf(record.get(C_LINE));
    int endLine = Integer.valueOf(record.get(C_END_LINE));

    return new SMMethodInfo(name, longName, path, line, endLine);
  }

}
