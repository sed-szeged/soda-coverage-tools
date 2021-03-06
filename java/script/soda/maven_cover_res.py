from .feedback import *

print(info("Maven cover resource are imported."))
soda_coverage_profile = """
<profile>
  <id>soda-coverage</id>
  <activation>
    <activeByDefault>true</activeByDefault>
  </activation>
  <properties>
    <soda.plugin.version>0.0.3</soda.plugin.version>
    <jacoco.address>127.0.0.1</jacoco.address>
    <jacoco.port>9999</jacoco.port>
    <jacoco.output>tcpserver</jacoco.output>
  </properties>
  <dependencies>
    <dependency>
      <groupId>hu.sed.soda.tools</groupId>
      <artifactId>soda-maven-plugin</artifactId>
      <version>${soda.plugin.version}</version>
      <type>maven-plugin</type>
      <scope>test</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.jacoco</groupId>
        <artifactId>jacoco-maven-plugin</artifactId>
        <version>0.7.5.201505241946</version>
        <executions>
          <execution>
            <id>default-prepare-agent</id>
            <goals>
              <goal>prepare-agent</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
      <plugin>
        <artifactId>maven-surefire-plugin</artifactId>
        <configuration>
          <testFailureIgnore>true</testFailureIgnore>
          <properties>
            <listener>hu.sed.soda.tools.CustomTestExecutionListener</listener>
          </properties>
        </configuration>
      </plugin>
    </plugins>
  </build>
  <reporting>
    <plugins>
      <plugin>
        <groupId>hu.sed.soda.tools</groupId>
        <artifactId>soda-maven-plugin</artifactId>
        <version>${soda.plugin.version}</version>
      </plugin>
    </plugins>
  </reporting>
</profile>
"""

soda_coverage_profile_junit = """
<profile>
  <id>soda-coverage</id>
  <activation>
    <activeByDefault>true</activeByDefault>
  </activation>
  <properties>
    <soda.plugin.version>0.0.3</soda.plugin.version>
    <jacoco.address>127.0.0.1</jacoco.address>
    <jacoco.port>9999</jacoco.port>
    <jacoco.output>tcpserver</jacoco.output>
  </properties>
  <dependencies>
    <dependency>
      <groupId>hu.sed.soda.tools</groupId>
      <artifactId>soda-maven-plugin</artifactId>
      <version>${soda.plugin.version}</version>
      <type>maven-plugin</type>
      <scope>test</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.jacoco</groupId>
        <artifactId>jacoco-maven-plugin</artifactId>
        <version>0.7.5.201505241946</version>
        <executions>
          <execution>
            <id>default-prepare-agent</id>
            <goals>
              <goal>prepare-agent</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
      <plugin>
        <artifactId>maven-surefire-plugin</artifactId>
        <configuration>
          <testFailureIgnore>true</testFailureIgnore>
          <properties>
            <listener>hu.sed.soda.tools.CustomTestExecutionListener</listener>
              <dependencies>
                <dependency>
                  <groupId>org.apache.maven.surefire</groupId>
                  <artifactId>surefire-junit47</artifactId>
                  <version>2.18.1</version>
                </dependency>
              </dependencies>
          </properties>
        </configuration>
      </plugin>
    </plugins>
  </build>
  <reporting>
    <plugins>
      <plugin>
        <groupId>hu.sed.soda.tools</groupId>
        <artifactId>soda-maven-plugin</artifactId>
        <version>${soda.plugin.version}</version>
      </plugin>
    </plugins>
  </reporting>
</profile>
"""
