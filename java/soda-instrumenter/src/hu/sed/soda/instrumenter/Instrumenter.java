package hu.sed.soda.instrumenter;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Hashtable;
import java.util.List;

import org.eclipse.core.runtime.IProgressMonitor;
import org.eclipse.jdt.core.ICompilationUnit;
import org.eclipse.jdt.core.JavaCore;
import org.eclipse.jdt.core.JavaModelException;
import org.eclipse.jdt.core.dom.AST;
import org.eclipse.jdt.core.dom.ASTParser;
import org.eclipse.jdt.core.dom.CompilationUnit;
import org.eclipse.jdt.core.formatter.DefaultCodeFormatterConstants;
import org.eclipse.jface.text.BadLocationException;
import org.eclipse.jface.text.Document;
import org.eclipse.text.edits.MalformedTreeException;
import org.eclipse.text.edits.TextEdit;

public class Instrumenter {

  private List<ICompilationUnit> units = new ArrayList<ICompilationUnit>();

  private InstrumenterVisitor v = new InstrumenterVisitor();

  public void addUnits(ICompilationUnit[] units) {
    this.units.addAll(Arrays.asList(units));
  }

  public int getNumUnits() {
    return units.size();
  }

  @SuppressWarnings("unchecked")
  private void instrument(ICompilationUnit unit) throws IOException, BadLocationException, JavaModelException {
    Document doc = new Document(unit.getSource());

    ASTParser parser = ASTParser.newParser(AST.JLS8);
    parser.setKind(ASTParser.K_COMPILATION_UNIT);
    parser.setSource(unit);
    parser.setResolveBindings(true);
    parser.setBindingsRecovery(true);

    // parser.setUnitName(filePath);
    // parser.setEnvironment(config.getClasspath(), config.getSources(), new String[] { "UTF-8" }, true);

    CompilationUnit cu = (CompilationUnit) parser.createAST(null);
    cu.recordModifications();
    cu.accept(v);

    Hashtable<String, String> options = JavaCore.getDefaultOptions();
    options.put(DefaultCodeFormatterConstants.FORMATTER_TAB_CHAR, JavaCore.SPACE);

    TextEdit edits = cu.rewrite(doc, options);
    unit.applyTextEdit(edits, null);
    unit.save(null, true);
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
