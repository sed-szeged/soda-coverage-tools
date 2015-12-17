package hu.sed.soda.tools;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.EmptyStackException;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Stack;
import java.util.logging.FileHandler;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

import org.jacoco.core.tools.ExecDumpClient;
import org.jacoco.core.tools.ExecFileLoader;
import org.junit.runner.Description;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;
import org.junit.runner.notification.RunListener;
import org.testng.ITestContext;
import org.testng.ITestListener;
import org.testng.ITestResult;

/**
 * Custom test execution listener for JUnit 4.x and TestNG.
 */
public class CustomTestExecutionListener extends RunListener implements ITestListener {

  private static final Logger LOGGER = Logger.getLogger(CustomTestExecutionListener.class.getName());

  /**
   * The version number of the program under test.
   * 
   * TODO: Get this value automatically.
   */
  private static String revision = "0";

  /**
   * Directory for coverage data.
   */
  private static File outputDirectory;

  /**
   * Numeric index of test for creating unique file names.
   */
  private static long testIndex = 0;

  /**
   * The results of tests with method level granularity.
   */
  private static List<TestInfo> testResults = new LinkedList<TestInfo>();

  /**
   * Information about the test which is running at the moment.
   */
  private static TestInfo actualTestInfo = null;

  /**
   * Statistics about the test suite.
   */
  private static Map<JUnitStatus, Long> testStats = new HashMap<JUnitStatus, Long>();
  
  private static int reset = 0;
  private static int dump = 0;
  private static Stack<Integer> idStack = new Stack<Integer>();

  /**
   * Initializes the output directory and the log output stream.
   */
  static {
    try {
      outputDirectory = Constants.COVERAGE_DIR.toFile();

      if (!outputDirectory.exists()) {
        outputDirectory.mkdirs();
      }

      // Configuring the logger.
      FileHandler fileHandler = new FileHandler(new File(Constants.BASE_DIR, "CustomJUnitExecutionListener.log").getAbsolutePath(), true);
      fileHandler.setFormatter(new SimpleFormatter());

      LOGGER.addHandler(fileHandler);

      // Initializing the statistics.
      for (JUnitStatus status : JUnitStatus.values()) {
        testStats.put(status, Long.valueOf(0));
      }

      LOGGER.info("Custom run listener has been initialized successfully.");
    } catch (SecurityException | IOException e) {
      System.err.println(e);
    }
  }

  /**
   * Writes the collected test results, and the hash mapping to files in the output directory.
   * The results will be written into the <{@link Constants#BASE_DIR}>/<{@link #revisionNumber}>/TestResults.r<{@link #revision}> file.
   * The mapping will be written into the <{@link Constants#BASE_DIR}>/<{@link #revisionNumber}>/{@link Constants#MAP_FILE}.r<{@link #revision}> file.
   * 
   * @param testResults
   *          List of {@link TestInfo test information} object.
   * @param revision
   *          The version identifier of the actual program under test.
   */
  public static void dumpTestResults() {
    File resultsDir = new File(Constants.BASE_DIR, revision);

    if (!resultsDir.exists()) {
      resultsDir.mkdirs();
    }

    File resultsFile = new File(resultsDir, String.format("TestResults.r%s", revision));
    File mapFile = new File(resultsDir, String.format("%s.r%s", Constants.MAP_FILE, revision));

    try (
        BufferedWriter resultOutput = new BufferedWriter(new FileWriter(resultsFile, true));
        BufferedWriter mapOutput = new BufferedWriter(new FileWriter(mapFile, true))
    ) {
      for (TestInfo result : testResults) {
        resultOutput.write(String.format("%s: %s\n", result.getFinalStatus().getOutcome(), result.getTestName()));
        mapOutput.write(String.format("%s%s%s\n", result.getHash(), Constants.MAP_FILE_SEPARATOR, result.getTestName()));
      }
    } catch (IOException e) {
      LOGGER.warning("Cannot dump test results because: " + e.getMessage());
    }
  }

  /**
   * Saves then resets the actual coverage.
   * 
   * @param coverageFile
   *          The file in which the coverage data should be stored.
   * 
   * @return True if the coverage data has been dumped, false if the data was only reset.
   */
  public static boolean dumpAndResetCoverage(File coverageFile) {
    boolean dump = false;

    try {
      if (!coverageFile.exists()) {
        dump = true;
      }

      ExecDumpClient client = new ExecDumpClient();
      client.setReset(true);
      client.setDump(dump);

      ExecFileLoader loader = client.dump(Constants.JACOCO_AGENT_ADDRESS, Constants.JACOCO_AGENT_PORT);

      if (dump) {
        loader.save(coverageFile, false);
      }
    } catch (IOException e) {
      LOGGER.warning("Cannot dump and reset coverage because: " + e.getMessage());
    }

    return dump;
  }

  /**
   * Resets the actual coverage.
   */
  public static void resetCoverage(int id) {
    boolean doReset = false;

    if (idStack.isEmpty()) {
      doReset = true;
    }

    idStack.push(id);

    if (doReset) {
      ++reset;

      try {
        ExecDumpClient client = new ExecDumpClient();
        client.setReset(true);
        client.setDump(false);

        client.dump(Constants.JACOCO_AGENT_ADDRESS, Constants.JACOCO_AGENT_PORT);
      } catch (IOException e) {
        LOGGER.warning("Cannot reset coverage because: " + e.getMessage());
      }
    }
  }
  
  /**
   * Saves then resets the actual coverage.
   */
  public static void dumpCoverage(int id) {
    boolean doDump = false;
    int act;

    try {
      act = idStack.peek();
    } catch (EmptyStackException e) {
      throw new Error(String.format("Stack was empty when tried to dump at #%d.", id));
    }

    if (act == id) {
      idStack.pop();
    } else {
      throw new Error(String.format("Reset/dump got desyncronized on dump at #%d.", id));
    }

    if (idStack.isEmpty()) {
      doDump = true;
    }

    if (doDump) {
      ++dump;
      File coverageFile = new File(outputDirectory, actualTestInfo.getHash() + '.' + Constants.COVERAGE_FILE_EXT);

      if (dumpAndResetCoverage(coverageFile)) {
        testResults.add(actualTestInfo);
      } else {
        LOGGER.warning(String.format("Coverage data already exists for test '%s' in file '%s'",
            actualTestInfo.getTestName(), coverageFile.getPath()));
      }
    }
  }

  // //////////////////////////////////////////////////////////////////////////
  // JUnit ////////////////////////////////////////////////////////////////////
  // //////////////////////////////////////////////////////////////////////////

  /**
   * Creates a name for the given test and updates the status of that test.
   * 
   * @param description
   *          The {@link Description description} of the test.
   * @param status
   *          The {@link JUnitStatus status} of the test.
   */
  private void handleEvent(Description description, JUnitStatus status) {
    testStats.put(status, testStats.get(status).longValue() + 1);

    actualTestInfo.addStatus(status);

    LOGGER.info(String.format("%s %s", actualTestInfo.getTestName(), status));
  }

  @Override
  public void testRunStarted(Description description) throws Exception {
    LOGGER.info("JUNIT TEST RUN STARTED");
  }

  @Override
  public void testIgnored(Description description) throws Exception {
    actualTestInfo = new TestInfo(TestInfo.getTestName(description));

    handleEvent(description, JUnitStatus.IGNORED);

    super.testIgnored(description);
  }

  @Override
  public void testStarted(Description description) throws Exception {
    actualTestInfo = new TestInfo(TestInfo.getTestName(description));

    handleEvent(description, JUnitStatus.STARTED);

    reset = dump = 0;

    super.testStarted(description);
  }

  @Override
  public void testAssumptionFailure(Failure failure) {
    handleEvent(failure.getDescription(), JUnitStatus.ASSUMPTION_FAILED);

    super.testAssumptionFailure(failure);
  }

  @Override
  public void testFailure(Failure failure) throws Exception {
    handleEvent(failure.getDescription(), JUnitStatus.FAILED);

    super.testFailure(failure);
  }

  @Override
  public void testFinished(Description description) throws Exception {
    handleEvent(description, JUnitStatus.FINISHED);
    
    if (!(reset == 1 && dump == 1)) {
      throw new Error(String.format("%s was not instrumented properly, D=%d R=%d", actualTestInfo.getTestName(), dump, reset));
    }

    super.testFinished(description);
  }

  @Override
  public void testRunFinished(Result result) throws Exception {
    LOGGER.info(String.format("JUNIT TEST RUN FINISHED in %dms", result.getRunTime()));
    LOGGER.info(String.format("JUnit stats: {tests=%d, ignored=%d, failed=%d}", result.getRunCount(), result.getIgnoreCount(), result.getFailureCount()));
    LOGGER.info(String.format("Listener stats: %s", testStats));

    dumpTestResults();

    super.testRunFinished(result);
  }

  // //////////////////////////////////////////////////////////////////////////
  // TestNG ///////////////////////////////////////////////////////////////////
  // //////////////////////////////////////////////////////////////////////////

  /**
   * Creates a name for the given test and updates the status of that test.
   * 
   * @param result
   *          The {@link ITestResult result} of the test.
   */
  private void handleEvent(ITestResult result) {
    String testName = TestInfo.getTestName(result);
    TestNGStatus status = TestNGStatus.createFrom(result);

    actualTestInfo = new TestInfo(testName, status);

    LOGGER.info(String.format("%s %s", testName, status));

    if (status != TestNGStatus.STARTED && status != TestNGStatus.SKIPPED) {
      if (!(reset == 1 && dump == 1)) {
        throw new Error(String.format("%s was not instrumented properly, D=%d R=%d", actualTestInfo.getTestName(), dump, reset));
      }
    }
  }

  @Override
  public void onTestStart(ITestResult result) {
    handleEvent(result);

    reset = dump = 0;
  }

  @Override
  public void onTestSuccess(ITestResult result) {
    handleEvent(result);
  }

  @Override
  public void onTestFailure(ITestResult result) {
    handleEvent(result);
  }

  @Override
  public void onTestSkipped(ITestResult result) {
    handleEvent(result);
  }

  @Override
  public void onTestFailedButWithinSuccessPercentage(ITestResult result) {
    handleEvent(result);
  }

  @Override
  public void onStart(ITestContext context) {
    LOGGER.info(String.format("TESTNG TEST (%s) STARTED", context.getName()));
  }

  @Override
  public void onFinish(ITestContext context) {
    LOGGER.info(String.format("TESTNG TEST (%s) FINISHED in %dms", context.getName(), context.getEndDate().getTime() - context.getStartDate().getTime()));
    LOGGER.info(String.format("TestNG stats: {tests=%d, skipped=%d, succeeded=%d, failed=%d, percent=%d, index=%d}",
        context.getAllTestMethods().length, context.getSkippedTests().size(), context.getPassedTests().size(), context.getFailedTests().size(), context.getFailedButWithinSuccessPercentageTests().size(), testIndex));

    dumpTestResults();
  }
}