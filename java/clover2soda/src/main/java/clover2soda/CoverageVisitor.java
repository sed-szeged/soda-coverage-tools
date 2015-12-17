package clover2soda;

import java.util.Set;

import com.atlassian.clover.CloverDatabase;
import com.atlassian.clover.CoverageData;
import com.atlassian.clover.api.registry.MethodInfo;
import com.atlassian.clover.registry.CoverageDataRange;
import com.atlassian.clover.registry.entities.TestCaseInfo;
import com.atlassian.clover.util.SimpleCoverageRange;

import hu.sed.soda.data.CoverageMatrix;

public class CoverageVisitor extends Visitor {

  CloverDatabase database;
  CoverageMatrix matrix;

  public CoverageVisitor(CloverDatabase db, CoverageMatrix m) {
    this.matrix = m;
    this.database = db;
  }

  @Override
  public void visit(MethodInfo methodInfo) {
    Set<TestCaseInfo> tests = getTestsCovering(database.getCoverageData(), methodInfo);

    out.println("NoT: " + tests.size());

    for (TestCaseInfo testCaseInfo : tests) {
      matrix.setRelation(testCaseInfo.getQualifiedName(), Utils.getMethodName(methodInfo), true);

      out.println(String.format("test #%d: %s", testCaseInfo.getId(), testCaseInfo.getQualifiedName()));
    }
  }

  private Set<TestCaseInfo> getTestsCovering(CoverageData coverage, MethodInfo methodInfo) {
    CoverageDataRange target = new SimpleCoverageRange(methodInfo.getDataIndex(), methodInfo.getDataLength());

    return coverage.getTestsCovering(target);
  }

}
