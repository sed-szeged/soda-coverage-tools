package clover2soda;

import hu.sed.soda.data.CoverageMatrix;

import java.io.FileNotFoundException;
import java.io.PrintStream;
import java.util.Set;

import com.atlassian.clover.CloverDatabase;
import com.atlassian.clover.CoverageData;
import com.atlassian.clover.CoverageDataSpec;
import com.atlassian.clover.api.CloverException;
import com.atlassian.clover.registry.entities.TestCaseInfo;

public class Main {

  static {
    System.loadLibrary("SoDAJni");
  }

  public static void main(String[] args) throws CloverException, FileNotFoundException {
    if (args.length != 2) {
      System.out.println("Usage: clover.jar <clover.db> <output>");

      return;
    }

    CoverageMatrix matrix = new CoverageMatrix();

    CloverDatabase db = CloverDatabase.loadWithCoverage(args[0], new CoverageDataSpec());

    CoverageData cov = db.getCoverageData();

    Set<TestCaseInfo> tests = cov.getTests();

    try (PrintStream out = new PrintStream("tc-log.txt")) {
      for (TestCaseInfo testCaseInfo : tests) {
        String tcname = testCaseInfo.getQualifiedName();

        matrix.addTestcaseName(tcname);

        out.println(String.format("id=%d name=%s", testCaseInfo.getId(), tcname));
        out.println("\t" + cov.getHitsFor(testCaseInfo));
      }
    }

    System.out.println("=================================================");

    try (PrintStream out = new PrintStream("ce-log.txt")) {
      addCodeElements(db, matrix, out);
    }

    matrix.refitMatrixSize();

    System.out.println("=================================================");

    try (PrintStream out = new PrintStream("cov-log.txt")) {
      addCoverage(db, matrix, out);
    }

    matrix.save(args[1]);
    matrix.dispose();
  }

  private static void addCodeElements(CloverDatabase db, CoverageMatrix matrix, PrintStream out) {
    CodeElementVisitor v = new CodeElementVisitor(matrix);
    v.setOut(out);
    DatabaseWalker dw = new DatabaseWalker(db, v);
    dw.setOut(out);
    dw.run();
  }

  private static void addCoverage(CloverDatabase db, CoverageMatrix matrix, PrintStream out) {
    CoverageVisitor v = new CoverageVisitor(db, matrix);
    v.setOut(out);
    DatabaseWalker dw = new DatabaseWalker(db, v);
    dw.setOut(out);
    dw.run();
  }

}
