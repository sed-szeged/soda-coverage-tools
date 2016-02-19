package clover2soda;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;

import clover2soda.exceptions.AmbiguousMethodException;
import clover2soda.exceptions.MethodNotFoundException;

public class MethodFinder {

  private List<SMMethodInfo> methods = new ArrayList<SMMethodInfo>();

  public MethodFinder() {
  }

  public void init(String csvFile) {
    readCSV(csvFile);
  }

  private void readCSV(String path) {
    try (Reader in = new FileReader(path)) {
      Iterable<CSVRecord> records = CSVFormat.DEFAULT.withHeader().parse(in);

      for (CSVRecord record : records) {
        methods.add(SMMethodInfo.createFromCSV(record));
      }
    } catch (FileNotFoundException e) {
      System.err.println("File not found: " + path);
    } catch (IOException e) {
      System.err.println("IO error: " + e.getMessage());
    }
  }

  private List<SMMethodInfo> findByName(String name) {
    List<SMMethodInfo> methods = new ArrayList<SMMethodInfo>();

    for (SMMethodInfo method : this.methods) {
      if (method.getLongName().startsWith(name)) {
        methods.add(method);
      }
    }

    return methods;
  }

  private List<SMMethodInfo> findByPosition(long line, List<SMMethodInfo> universe) {
    List<SMMethodInfo> methods = new ArrayList<SMMethodInfo>();

    for (SMMethodInfo method : universe) {
      if (method.getLine() <= line && line <= method.getEndLine()) {
        methods.add(method);
      }
    }

    return methods;
  }

  /**
   * Searches for a method in the SourceMeter data based on a {@link Mutant}.
   *
   * The search has a phases:
   *  #1 {@link #findByName(String)}: matching the name of the method aka. pre-filtering
   *  #2 {@link #findByPosition(String, long)}: matching the position (line) of the method
   *
   * @param mutant
   *          A {@link Mutant mutant}.
   *
   * @return A {@link SMMethodInfo method info}.
   *
   * @throws MethodNotFoundException
   *           If a method is not found.
   * @throws AmbiguousMethodException
   *           If multiple matches exist.
   */
  public SMMethodInfo findMethod(Mutant mutant) throws MethodNotFoundException, AmbiguousMethodException {
    List<SMMethodInfo> found = findByName(mutant.getMethod());

    found = findByPosition(mutant.getLine(), found);

    int numFound = found.size();

    if (numFound == 0) {
      throw new MethodNotFoundException();
    } else if (numFound == 1) {
      return found.get(0);
    } else {
      throw new AmbiguousMethodException();
    }
  }

}
