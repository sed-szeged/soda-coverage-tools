package hu.sed.soda.sonarqube.plugin;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.sonar.api.batch.SensorContext;
import org.sonar.api.batch.fs.internal.DefaultInputFile;
import org.sonar.api.batch.fs.internal.DefaultInputModule;
import org.sonar.api.batch.sensor.issue.internal.DefaultIssueLocation;
import org.sonar.api.component.ResourcePerspectives;
import org.sonar.api.issue.Issuable;
import org.sonar.api.measures.Measure;
import org.sonar.api.resources.Project;
import org.sonar.api.resources.Resource;
import org.sonar.api.rule.RuleKey;
import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

public class SodaCoverageSensor
implements org.sonar.api.batch.Sensor{

    private static final Logger LOG = LoggerFactory.getLogger(SodaCoverageSensor.class);

    ResourcePerspectives perspectives;
    
    public SodaCoverageSensor(ResourcePerspectives perspectives) {
        this.perspectives = perspectives;
    }
    
    @Override
    public void analyse(Project project, SensorContext sc) {
        String reportKey = "soda.coverage.report.class";
        if (!sc.settings().hasKey(reportKey)) {
            LOG.error(String.format("missing setting: %s", reportKey));
            return;
        }
        File report = new File(sc.settings().getString(reportKey));
        if (!report.exists()) {
            LOG.warn(String.format("Can not found report file at %s", report.getAbsolutePath()));
            return;
        }
        LOG.info(String.format("Loading class coverage from %s", report.getAbsolutePath()));
        String limitKey = "soda.coverage.limit.class";
        if (!sc.settings().hasKey(limitKey)) {
            LOG.error(String.format("missing setting: %s", limitKey));
            return;
        }
        Double limit = sc.settings().getDouble(limitKey);
        try {
            SAXParser parser = SAXParserFactory.newInstance().newSAXParser();
            ClassCoverageHandler handler = new ClassCoverageHandler();
            parser.parse(report, handler);
            RuleKey ruleKey = RuleKey.of(SodaRuleDefinition.REPO_KEY, SodaRuleDefinition.SODA_METHOD_COVERAGE_KEY);
            for (Map.Entry<String, Double> entry : handler.Values.entrySet()) {
                File source = new File(entry.getKey());
                if (source.exists()) {
                    LOG.info(String.format("setting coverage for %s to %s", entry.getKey(), entry.getValue()));
                    Resource resource = sc.getResource(new DefaultInputFile(project.getKey(), entry.getKey()));
                    sc.saveMeasure(resource, new Measure(SodaClassCoverageMetric.CLASS_COVERAGE_METRIC, entry.getValue()));
                    if (limit > entry.getValue()) {
                        sc.newIssue()
                            .at(new DefaultIssueLocation()
                                .on(new DefaultInputFile(project.getKey(), resource.getPath()))
                                .message(String.format("Coverage (%f) is lower than %f.", entry.getValue(), limit)))
                            .effortToFix(1.0)
                            .forRule(ruleKey)
                            .save();
                    }
                }
                else
                {
                    LOG.error(String.format("Can not found requested source file: %s", entry.getKey()));
                }
            }
        } catch (IOException | ParserConfigurationException | SAXException ex) {
            LOG.error(ex.toString());
        }
    }

    class ClassCoverageHandler
    extends DefaultHandler {
        public Map<String, Double> Values = new HashMap<>();
        
        @Override
        public void startElement(String uri, String localName, String qName, Attributes attributes) {
            if (qName.equalsIgnoreCase("class-coverage-entry")) {
                Values.put(attributes.getValue("path"), Double.parseDouble(attributes.getValue("coverage")));
            }
        }
    }
    
    @Override
    public boolean shouldExecuteOnProject(Project project) {
        return true;
    }    
}
