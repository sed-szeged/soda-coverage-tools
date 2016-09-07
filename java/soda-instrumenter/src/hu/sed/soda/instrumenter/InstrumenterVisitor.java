package hu.sed.soda.instrumenter;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import org.eclipse.jdt.core.dom.ASTVisitor;
import org.eclipse.jdt.core.dom.ClassInstanceCreation;
import org.eclipse.jdt.core.dom.ConstructorInvocation;
import org.eclipse.jdt.core.dom.IMethodBinding;
import org.eclipse.jdt.core.dom.MethodDeclaration;
import org.eclipse.jdt.core.dom.MethodInvocation;
import org.eclipse.jdt.core.dom.SuperConstructorInvocation;
import org.eclipse.jdt.core.dom.SuperMethodInvocation;
import org.eclipse.jdt.core.dom.TypeDeclaration;

public class InstrumenterVisitor extends ASTVisitor {

  int depth;
  IMethodBinding testMethodContext;
  Map<String, Set<String>> data;

  private void addCall(IMethodBinding method) {
    if (testMethodContext != null) {
      String testName = testMethodContext.getDeclaringClass().getQualifiedName() + "." + testMethodContext.getName();

      if (!data.containsKey(testName)) {
        data.put(testName, new HashSet<String>());
      }

      String signature = Utils.getSignature(method);
      data.get(testName).add(signature);

      System.err.println(String.format("\t%s", signature));
    }
  }

  public Map<String, Set<String>> getData() {
    return data;
  }

  public InstrumenterVisitor() {
    super();
    depth = 0;
    testMethodContext = null;
    data = new HashMap<String, Set<String>>();
  }

  @Override
  public boolean visit(TypeDeclaration node) {
    System.out.println(String.format("type: %s", node.getName()));
    return true;
  }

  @Override
  public boolean visit(MethodDeclaration method) {
    ++depth;

    boolean j3 = Utils.isJUnit3TestMethod(method);
    boolean j4 = Utils.isJUnit4TestMethod(method);

    IMethodBinding binding = method.resolveBinding();
    String fullname = binding.getDeclaringClass().getQualifiedName() + '.' + binding.getName();
    System.out.print(String.format("method declaration: %s, j3: %s, j4: %s", fullname, j3, j4));

    if (depth == 1 && (j3 || j4)) {
      testMethodContext = binding;
      System.out.println(" do(j) ...");
      return true;
    } else if (depth > 1) {
      System.out.println(" do(t) ...");
      return true;
    } else {
      System.out.println(" skip...");
      return false;
    }
  }

  @Override
  public void endVisit(MethodDeclaration node) {
    --depth;
    if (depth == 0) {
      testMethodContext = null;
    }
    System.out.println(String.format("method declaration: %s ... done.", node.resolveBinding().getName()));
  }

  @Override
  public boolean visit(MethodInvocation node) {
    if (depth < 1) {
      return false;
    }

    addCall(node.resolveMethodBinding());

    return true;
  }

  @Override
  public boolean visit(SuperMethodInvocation node) {
    if (depth < 1) {
      return false;
    }

    addCall(node.resolveMethodBinding());

    return true;
  }

  @Override
  public boolean visit(ConstructorInvocation node) {
    if (depth < 1) {
      return false;
    }

    addCall(node.resolveConstructorBinding());

    return true;
  }

  @Override
  public boolean visit(SuperConstructorInvocation node) {
    if (depth < 1) {
      return false;
    }

    addCall(node.resolveConstructorBinding());

    return true;
  }

  @Override
  public boolean visit(ClassInstanceCreation node) {
    if (depth < 1) {
      return false;
    }

    addCall(node.resolveConstructorBinding());

    return true;
  }
}