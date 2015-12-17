package clover2soda;

import com.atlassian.clover.api.registry.MethodInfo;

public class Utils {

  public static String getMethodName(MethodInfo method) {
    return method.getContainingClass().getQualifiedName() + "." + method.getName();
  }

}
