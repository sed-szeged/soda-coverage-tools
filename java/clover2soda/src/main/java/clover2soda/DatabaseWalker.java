package clover2soda;

import java.io.PrintStream;

import com.atlassian.clover.CloverDatabase;
import com.atlassian.clover.api.registry.ClassInfo;
import com.atlassian.clover.api.registry.FileInfo;
import com.atlassian.clover.api.registry.MethodInfo;
import com.atlassian.clover.api.registry.PackageInfo;
import com.atlassian.clover.registry.entities.FullProjectInfo;

public class DatabaseWalker {
  
  private CloverDatabase database;
  private Visitor visitor;
  private PrintStream out = System.out;
  
  public void setOut(PrintStream out) {
    this.out = out;
  }

  public DatabaseWalker(CloverDatabase db, Visitor v) {
    this.database = db;
    this.visitor = v;
  }
  
  public void run() {
    run(database.getRegistry().getProject());
  }

  private void run(FullProjectInfo projectInfo) {
    out.println("Project: " + projectInfo.getName());
    
    visitor.visit(projectInfo);
    
    for (PackageInfo packageInfo : projectInfo.getAllPackages()) {
      run(packageInfo);
    }
  }

  private void run(PackageInfo packageInfo) {
    out.println("Package: " + packageInfo.getName());
    
    visitor.visit(packageInfo);
    
    for (FileInfo fileInfo : packageInfo.getFiles()) {
      run(fileInfo);
    }
  }

  private void run(FileInfo fileInfo) {
    out.println("File: " + fileInfo.getName());
    
    visitor.visit(fileInfo);
    
    for (ClassInfo classInfo : fileInfo.getClasses()) {
      run(classInfo);
    }
  }

  private void run(ClassInfo classInfo) {
    out.println("Class: " + classInfo.getQualifiedName());
    
    visitor.visit(classInfo);
    
    for (MethodInfo methodInfo : classInfo.getAllMethods()) {
      run(methodInfo);
    }
  }

  private void run(MethodInfo methodInfo) {
    out.print(String.format("Method #%d: %s", methodInfo.getDataIndex(), methodInfo.getQualifiedName()));
    
    boolean skip = skip(methodInfo);
    
    out.println();
    
    if (!skip) {
      visitor.visit(methodInfo);
    }
  }

  private boolean skip(MethodInfo method) {
    if (method.isTest()) {
      out.print(" [skipped: test method]");
      
      return true;
    }
    
    if (method.isLambda()) {
      out.print(" [skipped: lambda method]");
      
      return true;
    }

    FileInfo containingFile = method.getContainingFile();

    if (containingFile.isTestFile()) {
      out.print(" [skipped: test file]");
      
      return true;
    }

    for (ClassInfo ci : containingFile.getAllClasses()) {
      if (ci.isTestClass()) {
        out.print(" [skipped: test class]");
        
        return true;
      }
    }

    for (MethodInfo mi : containingFile.getAllMethods()) {
      if (mi.isTest()) {
        out.print(" [skipped: test method neighbour]");
        
        return true;
      }
    }

    return false;
  }

}
