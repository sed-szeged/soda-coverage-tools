package hu.sed.soda.sonarqube.plugin;

import org.sonar.api.resources.Java;
import org.sonar.api.server.debt.DebtRemediationFunction;
import org.sonar.api.server.debt.internal.DefaultDebtRemediationFunction;
import org.sonar.api.server.rule.RulesDefinition;

public class SodaRuleDefinition
implements RulesDefinition
{
    public static final String REPO_KEY = "soda";
    public static final String SODA_METHOD_COVERAGE_KEY = "soda-method-coverage";

    @Override
    public void define(Context context) {
        NewRepository repository = context.createRepository(REPO_KEY, Java.KEY);
        repository.setName("SoDA");
        repository.createRule(SODA_METHOD_COVERAGE_KEY)
                .setName("SoDA aggregated method coverage")
                .setMarkdownDescription("foo")
                .setDebtSubCharacteristic("UNIT_LEVEL")
                .setDebtRemediationFunction(
                    new DefaultDebtRemediationFunction(
                        DebtRemediationFunction.Type.LINEAR, "1h", null));
        repository.done();
    }
}
