package clover2soda;

import java.io.FileNotFoundException;
import java.io.PrintStream;
import java.util.Set;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.MissingOptionException;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;

import com.atlassian.clover.CloverDatabase;
import com.atlassian.clover.CoverageData;
import com.atlassian.clover.CoverageDataSpec;
import com.atlassian.clover.api.CloverException;
import com.atlassian.clover.registry.entities.TestCaseInfo;

import hu.sed.soda.data.CoverageMatrix;
import hu.sed.soda.data.ResultsMatrix;
import hu.sed.soda.data.ResultsMatrix.TestResultType;

public class Main {

  static {
    System.loadLibrary("SoDAJni");
  }

  public static void main(String[] args) throws CloverException, FileNotFoundException {
    CommandLineParser parser = new DefaultParser();

    Options options = new Options();
    Option optHelp = Option.builder("h")
                           .longOpt("help")
                           .desc("print this message")
                           .build();
    options.addOption(optHelp);
    Option optDB = Option.builder("d")
                         .longOpt("clover-database")
                         .desc("the path to the clover.db file")
                         .hasArg()
                         .build();
    options.addOption(optDB);
    Option optCov = Option.builder("c")
                          .longOpt("coverage")
                          .desc("save the coverage binary to the given file")
                          .hasArg()
                          .build();
    options.addOption(optCov);
    Option optRes = Option.builder("r")
                          .longOpt("results")
                          .desc("save the results binary to the given file")
                          .hasArg()
                          .build();
    options.addOption(optRes);

    try {
      CommandLine line = parser.parse(options, args);

      if (args.length < 2 || line.hasOption("help")) {
        new HelpFormatter().printHelp("clover2soda.jar", options);
        return;
      }

      CloverDatabase db = null;

      if (line.hasOption("clover-database")) {
        String dbPath = line.getOptionValue("clover-database");
        db = CloverDatabase.loadWithCoverage(dbPath, new CoverageDataSpec());
      } else {
        throw new MissingOptionException("Option -d,--clover-database must be specified.");
      }

      boolean calcCov = line.hasOption("coverage");
      boolean calcRes = line.hasOption("results");

      if (!calcCov && !calcRes) {
        throw new MissingOptionException("At least one of the following options must be specified: -c,--coverage or -r,--results");
      }

      if (calcCov) {
        String covPath = line.getOptionValue("coverage");
        createCoverage(db, covPath);
      }

      if (calcRes) {
        String resPath = line.getOptionValue("results");
        createResults(db, resPath);
      }
    } catch (Exception e) {
      System.err.println("ERROR: " + e.getMessage());
    }
  }

  /**
   * Creates, populates and saves a results binary.
   *
   * @param db A {@link CloverDatabase}
   * @param resultsPath The path where the binary file should be saved.
   */
  private static void createResults(CloverDatabase db, String resultsPath) {
    ResultsMatrix results = new ResultsMatrix();
    results.addRevisionNumber(0); // TODO: Get revision number from e.g. the database or command line.

    TestNameManager tnm = new TestNameManager();
    Set<TestCaseInfo> tests = db.getCoverageData().getTests();

    for (TestCaseInfo test : tests) {
      results.addTestcaseName(tnm.getUniqueNameFor(test));
    }

    results.refitMatrixSize();
    tnm.reset();

    for (TestCaseInfo test : tests) {
      TestResultType result;

      if (test.isFailure()) {
        result = TestResultType.Failed;
      } else if (test.isSuccess()) {
        result = TestResultType.Passed;
      } else {
        result = TestResultType.NotExecuted;
      }

      results.setResult(0, tnm.getUniqueNameFor(test), result); // TODO: Add support for different revisions.
    }

    results.save(resultsPath);
    results.dispose();
  }

  /**
   * Creates, populates and saves a coverage binary.
   *
   * @param db A {@link CloverDatabase}
   * @param coveragePath The path where the binary file should be saved.
   *
   * @throws FileNotFoundException
   */
  private static void createCoverage(CloverDatabase db, String coveragePath) throws FileNotFoundException {
    CoverageMatrix matrix = new CoverageMatrix();
    CoverageData cov = db.getCoverageData();

    TestNameManager tnm = new TestNameManager();
    Set<TestCaseInfo> tests = cov.getTests();

    try (PrintStream out = new PrintStream("tc-log.txt")) {
      for (TestCaseInfo testCaseInfo : tests) {
        matrix.addTestcaseName(tnm.getUniqueNameFor(testCaseInfo));

        out.println(String.format("id=%d name=%s", testCaseInfo.getId(), testCaseInfo.getQualifiedName()));
        out.println("\t" + cov.getHitsFor(testCaseInfo));
      }
    }

    try (PrintStream out = new PrintStream("ce-log.txt")) {
      addCodeElements(db, matrix, out);
    }

    matrix.refitMatrixSize();

    try (PrintStream out = new PrintStream("cov-log.txt")) {
      addCoverage(db, matrix, out);
    }

    matrix.save(coveragePath);
    matrix.dispose();
  }

  /**
   * Adds all the code elements to the given matrix.
   *
   * @param db A {@link CloverDatabase}
   * @param matrix A {@link CoverageMatrix}
   * @param out A {@link PrintStream} to log on.
   */
  private static void addCodeElements(CloverDatabase db, CoverageMatrix matrix, PrintStream out) {
    CodeElementVisitor v = new CodeElementVisitor(matrix);
    v.setOut(out);
    DatabaseWalker dw = new DatabaseWalker(db, v);
    dw.setOut(out);
    dw.run();
  }

  /**
   * Populates the given matrix with coverage data.
   *
   * @param db A {@link CloverDatabase}
   * @param matrix A {@link CoverageMatrix}
   * @param out A {@link PrintStream} to log on.
   */
  private static void addCoverage(CloverDatabase db, CoverageMatrix matrix, PrintStream out) {
    CoverageVisitor v = new CoverageVisitor(db, matrix);
    v.setOut(out);
    DatabaseWalker dw = new DatabaseWalker(db, v);
    dw.setOut(out);
    dw.run();
  }

}
