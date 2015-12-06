package hu.sed.soda.instrumenter;

import org.eclipse.jdt.core.dom.AST;
import org.eclipse.jdt.core.dom.ASTNode;
import org.eclipse.jdt.core.dom.ASTVisitor;
import org.eclipse.jdt.core.dom.Block;
import org.eclipse.jdt.core.dom.MethodDeclaration;
import org.eclipse.jdt.core.dom.MethodInvocation;
import org.eclipse.jdt.core.dom.Name;
import org.eclipse.jdt.core.dom.Statement;
import org.eclipse.jdt.core.dom.TryStatement;

public class InstrumenterVisitor extends ASTVisitor {

  private static final Statement createCall(String methodName, AST ast) {
    Name name = ast.newName(new String[] { "hu", "sed", "soda", "tools", "CustomTestExecutionListener" });

    MethodInvocation mthInv = ast.newMethodInvocation();
    mthInv.setExpression(name);
    mthInv.setName(ast.newSimpleName(methodName));

    return ast.newExpressionStatement(mthInv);
  }

  @SuppressWarnings("unchecked")
  @Override
  public boolean visit(MethodDeclaration method) {
    if (!Utils.isJUnit3TestMethod(method) && !Utils.isJUnit4TestMethod(method)) {
      return true;
    }

    TryStatement tryStmt = method.getAST().newTryStatement();

    Block tryBody = (Block) ASTNode.copySubtree(tryStmt.getAST(), method.getBody());
    tryBody.statements().add(0, createCall("resetCoverage", method.getAST()));
    tryStmt.setBody(tryBody);

    Block fin = method.getAST().newBlock();
    fin.statements().add(createCall("dumpCoverage", method.getAST()));

    tryStmt.setFinally(fin);

    Block newBody = method.getAST().newBlock();
    newBody.statements().add(tryStmt);

    method.setBody((Block) ASTNode.copySubtree(method.getAST(), newBody));

    return true;
  }
}