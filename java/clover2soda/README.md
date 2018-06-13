# Clover2SoDA

The aim of Clover2SoDA is to provide an interface for converting [Clover](https://bitbucket.org/atlassian/clover)'s code coverage and test result data to [SoDA](https://github.com/sed-szeged/soda) (Software Development Analysis framework) compatible formats.

## How to build

### Dependencies

- Java 8+
- [SoDA-Java](https://github.com/sed-szeged/soda-java)

### Build

```bash
mvn clean package
```

After executing this command You should find Clover2SoDA in the `{CLOVER2SODA_DIR}/target` directory as `clover2soda-{VER}.jar`

## How to use

1. First, You need the coverage and results data. See [this guide](https://confluence.atlassian.com/clover/clover-for-maven-2-and-3-quick-start-guide-160399608.html) to learn how to analyze Your target project using Clover. If everything works fine you should find a `clover.db` file in the `/target/clover` directory of the target project.
2. Next, the `clover.db` file can be converted to SoDA compatible format by executing the following command:
```bash
java -Djava.library.path={LIB_DIR} -jar clover2soda-0.0.1.jar -d clover.db -c myCoverage.SoDA -r myResults.SoDA
```
**Please make sure that `-Djava.library.path=...` is the very first argument.**

The `{LIB_DIR}` parameter must be the path to the directory which contains the SoDA-Java library (_libSoDAJni.so_). By default it is the `{SODA_JAVA_DIR}/build/src/main/cpp` directory.
