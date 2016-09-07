package hu.sed.soda.instrumenter;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.eclipse.core.runtime.IProgressMonitor;
import org.eclipse.jdt.core.ICompilationUnit;
import org.eclipse.jdt.core.JavaModelException;
import org.eclipse.jdt.core.dom.AST;
import org.eclipse.jdt.core.dom.ASTParser;
import org.eclipse.jdt.core.dom.CompilationUnit;
import org.eclipse.jface.text.BadLocationException;
import org.eclipse.text.edits.MalformedTreeException;

public class Instrumenter {

  private List<ICompilationUnit> units;
  private InstrumenterVisitor visitor;

  public Instrumenter(InstrumenterVisitor visitor) {
    this.units = new ArrayList<ICompilationUnit>();
    this.visitor = visitor;
  }

  public void addUnits(ICompilationUnit[] units) {
    this.units.addAll(Arrays.asList(units));
  }

  public int getNumUnits() {
    return units.size();
  }

  private void instrument(ICompilationUnit unit) throws IOException, BadLocationException, JavaModelException {
    ASTParser parser = ASTParser.newParser(AST.JLS8);
    parser.setKind(ASTParser.K_COMPILATION_UNIT);
    parser.setSource(unit);
    parser.setResolveBindings(true);
    parser.setBindingsRecovery(true);

    // parser.setUnitName(filePath);
    // parser.setEnvironment(config.getClasspath(), config.getSources(), new String[] { "UTF-8" }, true);

    CompilationUnit cu = (CompilationUnit) parser.createAST(null);
    cu.accept(visitor);
  }

  public void run(IProgressMonitor monitor) throws JavaModelException, MalformedTreeException, BadLocationException, IOException {
    int i = 0, n = units.size();

    for (ICompilationUnit unit : units) {
      monitor.subTask(String.format("%d/%d %s", ++i, n, unit.getPath()));

      instrument(unit);

      monitor.worked(1);
    }
  }

}
