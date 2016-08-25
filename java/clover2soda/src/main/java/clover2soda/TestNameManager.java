package clover2soda;

import java.util.HashSet;
import java.util.Set;

import com.atlassian.clover.registry.entities.TestCaseInfo;

/**
 * This class is used as a workaround for the cases where clover.db has different
 * test with the same name although the additional listener is utilized.
 *
 * TODO: Fix this if possible
 */
public class TestNameManager {

  private Set<String> names = new HashSet<String>();

  /**
   * Creates a unique name for the given test by appending its id to the end of its qualified name.
   *
   * @param test A {@link TestCaseInfo test}
   * @return The unique name of the given test: {@link TestCaseInfo#getQualifiedName() qualified-name}#{@link TestCaseInfo#getId() clover-id}.
   */
  public String getUniqueNameFor(TestCaseInfo test) {
    return test.getQualifiedName() + "#" + test.getId();
  }

  public void reset() {
    names.clear();
  }

}
