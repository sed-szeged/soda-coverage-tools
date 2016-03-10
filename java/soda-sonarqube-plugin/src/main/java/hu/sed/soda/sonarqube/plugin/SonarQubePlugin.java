package hu.sed.soda.sonarqube.plugin;

import java.util.Arrays;
import java.util.List;

public class SonarQubePlugin
extends org.sonar.api.SonarPlugin{

    @Override
    public List getExtensions() {
        return Arrays.asList(
                SodaClassCoverageMetric.class,
                SodaCoverageSensor.class,
                SodaRuleDefinition.class
        );
    }    
}
