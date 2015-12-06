package hu.sed.soda.eclipse.plugin.actions;

import java.io.IOException;

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
import org.eclipse.swt.widgets.Shell;
import org.eclipse.text.edits.MalformedTreeException;
import org.eclipse.ui.IActionDelegate;
import org.eclipse.ui.IObjectActionDelegate;
import org.eclipse.ui.IWorkbenchPart;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.PlatformUI;

import hu.sed.soda.instrumenter.Instrumenter;

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
    boolean start = MessageDialog.openConfirm(shell, "SoDA", "Do You really want to start instrumenting?");

    if (!start) {
      return;
    }

    IWorkbenchWindow window = PlatformUI.getWorkbench().getActiveWorkbenchWindow();

    if (window != null) {
      IStructuredSelection selection = (IStructuredSelection) window.getSelectionService().getSelection();

      Instrumenter instrumenter = new Instrumenter();

      for (Object element : selection.toList()) {
        if (element instanceof IAdaptable) {
          IAdaptable adaptable = (IAdaptable) element;
          IPackageFragment selectedPackage = adaptable.getAdapter(IPackageFragment.class);

          try {
            instrumenter.addUnits(selectedPackage.getCompilationUnits());
          } catch (JavaModelException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
          }
        }
      }

      int n = instrumenter.getNumUnits();

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
