package hu.sed.soda.eclipse.plugin.actions;

import java.io.FileWriter;
import java.io.IOException;
import java.util.Map.Entry;
import java.util.Set;

import org.eclipse.core.runtime.IAdaptable;
import org.eclipse.core.runtime.IProgressMonitor;
import org.eclipse.core.runtime.IStatus;
import org.eclipse.core.runtime.Status;
import org.eclipse.core.runtime.jobs.Job;
import org.eclipse.jdt.core.IPackageFragment;
import org.eclipse.jdt.core.JavaModelException;
import org.eclipse.jface.action.IAction;
import org.eclipse.jface.dialogs.MessageDialog;
import org.eclipse.jface.text.BadLocationException;
import org.eclipse.jface.viewers.ISelection;
import org.eclipse.jface.viewers.IStructuredSelection;
import org.eclipse.swt.SWT;
import org.eclipse.swt.widgets.FileDialog;
import org.eclipse.swt.widgets.Shell;
import org.eclipse.text.edits.MalformedTreeException;
import org.eclipse.ui.IActionDelegate;
import org.eclipse.ui.IObjectActionDelegate;
import org.eclipse.ui.IWorkbenchPart;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.PlatformUI;

import hu.sed.soda.instrumenter.Instrumenter;
import hu.sed.soda.instrumenter.InstrumenterVisitor;

public class InstrumenterAction implements IObjectActionDelegate {

  private Shell shell;

  /**
   * Constructor for InstrumenterAction.
   */
  public InstrumenterAction() {
    super();
  }

  /**
   * @see IObjectActionDelegate#setActivePart(IAction, IWorkbenchPart)
   */
  public void setActivePart(IAction action, IWorkbenchPart targetPart) {
    shell = targetPart.getSite().getShell();
  }

  /**
   * @see IActionDelegate#run(IAction)
   */
  public void run(IAction action) {
    FileDialog dialog = new FileDialog(shell, SWT.SAVE);
    dialog.setText("Select a file in which the data should be saved...");
    final String path = dialog.open();

    if (path.isEmpty()) {
      return;
    }

    boolean start = MessageDialog.openConfirm(shell, "SoDA", "Do You really want to start instrumenting?");

    if (!start) {
      return;
    }

    IWorkbenchWindow window = PlatformUI.getWorkbench().getActiveWorkbenchWindow();

    if (window != null) {
      IStructuredSelection selection = (IStructuredSelection) window.getSelectionService().getSelection();

      final InstrumenterVisitor visitor = new InstrumenterVisitor();
      final Instrumenter instrumenter = new Instrumenter(visitor);

      for (Object element : selection.toList()) {
        if (element instanceof IAdaptable) {
          IAdaptable adaptable = (IAdaptable) element;
          IPackageFragment selectedPackage = adaptable.getAdapter(IPackageFragment.class);

          try {
            instrumenter.addUnits(selectedPackage.getCompilationUnits());
          } catch (JavaModelException e) {
            System.err.println(String.format("Cannot get the compilation units of package (%s).", selectedPackage.getElementName()));
          }
        }
      }

      final int n = instrumenter.getNumUnits();

      if (n > 0) {
        Job job = new Job("SoDA") {

          @Override
          protected IStatus run(IProgressMonitor monitor) {
            monitor.beginTask("Instrumentation", n);

            try {
              instrumenter.run(monitor);
            } catch (JavaModelException | MalformedTreeException | BadLocationException | IOException e) {
              // TODO Auto-generated catch block
              e.printStackTrace();
            }

            System.err.println("DATA: " + visitor.getData().size());

            try (FileWriter out = new FileWriter(path)) {
              for (Entry<String, Set<String>> entry : visitor.getData().entrySet()) {
                String test = entry.getKey();

                for (String method : entry.getValue()) {
                  out.write(String.format("%s;%s\n", test, method));
                }
              }
            } catch (IOException e) {
              e.printStackTrace();
            }

            return Status.OK_STATUS;
          }
        };

        job.schedule();
      }
    }
  }

  /**
   * @see IActionDelegate#selectionChanged(IAction, ISelection)
   */
  public void selectionChanged(IAction action, ISelection selection) {
  }

}
