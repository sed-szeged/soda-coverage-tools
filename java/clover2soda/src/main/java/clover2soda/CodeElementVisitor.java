package clover2soda;

import com.atlassian.clover.api.registry.MethodInfo;

import hu.sed.soda.data.CoverageMatrix;

public class CodeElementVisitor extends Visitor {

  CoverageMatrix matrix;

  public CodeElementVisitor(CoverageMatrix m) {
    this.matrix = m;
  }

  @Override
  public void visit(MethodInfo methodInfo) {
    matrix.addCodeElementName(Utils.getMethodName(methodInfo));
  }

}
