package hu.sed.soda.sonarqube.plugin;

import java.util.Arrays;
import java.util.List;
import org.sonar.api.measures.Metric;

public class SodaClassCoverageMetric
implements org.sonar.api.measures.Metrics{

    public static final Metric CLASS_COVERAGE_METRIC =
            new Metric.Builder("soda_class_coverage", "SoDA Class Coverage", Metric.ValueType.PERCENT)
            .setDescription("The test coverage measured (and processed) by SoDA framework")
            .setQualitative(true)
            .setDomain("Test")
            .create();
    
    @Override
    public List<Metric> getMetrics() {
        return Arrays.asList(CLASS_COVERAGE_METRIC);
    }    
}
