package clover2soda;

import java.io.PrintStream;

import com.atlassian.clover.api.registry.ClassInfo;
import com.atlassian.clover.api.registry.FileInfo;
import com.atlassian.clover.api.registry.MethodInfo;
import com.atlassian.clover.api.registry.PackageInfo;
import com.atlassian.clover.registry.entities.FullProjectInfo;

public class Visitor {

  protected PrintStream out = System.out;
  
  public void setOut(PrintStream out) {
    this.out = out;
  }
  
  public Visitor() {
  }
  
  public void visit(FullProjectInfo projectInfo) {
  }
  
  public void visit(PackageInfo packageInfo) {
  }
  
  public void visit(FileInfo fileInfo) {
  }
  
  public void visit(ClassInfo classInfo) {
  }
  
  public void visit(MethodInfo methodInfo) {
  }

}
