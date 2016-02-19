package clover2soda;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.MissingOptionException;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;

import clover2soda.exceptions.AmbiguousMethodException;
import clover2soda.exceptions.MethodNotFoundException;
import hu.sed.soda.data.Changeset;

public class Main {

  static {
    System.loadLibrary("SoDAJni");
  }

  private static MethodFinder methodFinder = new MethodFinder();
  private static Map<Integer, Integer> idMap = new HashMap<Integer, Integer>();
  private static Map<Mutant, SMMethodInfo> mutants = new HashMap<Mutant, SMMethodInfo>();

  public static void main(String[] args) throws Exception {
    CommandLineParser parser = new DefaultParser();

    Options options = new Options();

    Option optMts = Option.builder("l")
                          .longOpt("log")
                          .desc("path to a mutants log file")
                          .hasArg()
                          .build();
    options.addOption(optMts);
    Option optSM = Option.builder("s")
                         .longOpt("sm")
                         .desc("path to a SourceMeter based method list file")
                         .hasArg()
                         .build();
    options.addOption(optSM);
    Option optChg = Option.builder("c")
                          .longOpt("changeset")
                          .desc("path to save the created changeset")
                          .hasArg()
                          .build();
    options.addOption(optChg);
    Option optMap = Option.builder("m")
                          .longOpt("map")
                          .desc("path to a mutants list file")
                          .hasArg()
                          .build();
    options.addOption(optMap);

    try {
      CommandLine cmdLine = parser.parse(options, args);

      if (args.length < 2 || cmdLine.hasOption("help")) {
        new HelpFormatter().printHelp("clover2soda.jar", options);
        return;
      }

      if (cmdLine.hasOption("log")) {
        String logPath = cmdLine.getOptionValue("log");

        try {
          List<String> lines = Files.readAllLines(Paths.get(logPath));

          for (String line : lines) {
            Mutant mutant = Mutant.createFromLog(line);
            mutants.put(mutant, null);
          }
        } catch (FileNotFoundException e) {
          System.err.println("File not found: " + logPath);
        } catch (IOException e) {
          System.err.println("IO error: " + e.getMessage());
        }
      } else {
        throw new MissingOptionException("Option -l,--log must be specified.");
      }

      if (cmdLine.hasOption("sm")) {
        String smPath = cmdLine.getOptionValue("sm");
        methodFinder.init(smPath);
      } else {
        throw new MissingOptionException("Option -s,--sm must be specified.");
      }

      boolean useMap = false;

      if (cmdLine.hasOption("map")) {
        String mapPath = cmdLine.getOptionValue("map");

        try {
          List<String> lines = Files.readAllLines(Paths.get(mapPath));

          for (String line : lines) {
            try {
              String[] columns = line.split(";");

              int id = Integer.valueOf(columns[0]);
              String dir = columns[5];
              String[] dirs = dir.split("[\\/]");
              int newID = Integer.valueOf(dirs[dirs.length - 1]);

              idMap.put(id, newID);
            } catch (ArrayIndexOutOfBoundsException | NumberFormatException e) {
              System.err.println(String.format("Cannot parse line '%s': %s", line, e));
            }
          }
        } catch (FileNotFoundException e) {
          System.err.println("File not found: " + mapPath);
        } catch (IOException e) {
          System.err.println("IO error: " + e.getMessage());
        }

        useMap = true;
      }

      for (Mutant mutant : mutants.keySet()) {
        try {
          SMMethodInfo method = methodFinder.findMethod(mutant);
          mutants.put(mutant, method);
        } catch (MethodNotFoundException e) {
          System.err.println("Not found: " + mutant);
        } catch (AmbiguousMethodException e) {
          System.err.println("Too many found: " + mutant);
        }
      }

      if (cmdLine.hasOption("changeset")) {
        String outPath = cmdLine.getOptionValue("changeset");

        Changeset changeset = new Changeset();

        int skipped = 0;

        for (Entry<Mutant, SMMethodInfo> entry : mutants.entrySet()) {
          if (entry.getValue() == null) {
            continue;
          }

          int id = entry.getKey().getId();

          if (useMap) {
            if (idMap.containsKey(id)) {
              id = idMap.get(id);
            } else {
              ++skipped;
            }
          }

          changeset.addRevision(id);
          changeset.addCodeElement(entry.getValue().getLongName());
        }

        if (skipped > 0) {
          System.err.println(String.format("%d mutant(s) have been skipped: id mapping is enabled, but cannot find new id in the map file.", skipped));
        }

        changeset.refitMatrixSize();

        for (Entry<Mutant, SMMethodInfo> entry : mutants.entrySet()) {
          if (entry.getValue() == null) {
            continue;
          }

          int id = entry.getKey().getId();

          if (useMap) {
            if (idMap.containsKey(id)) {
              id = idMap.get(id);
            } else {
              ++skipped;
            }
          }

          changeset.setChange(id, entry.getValue().getLongName(), true);
        }

        changeset.save(outPath);
        changeset.dispose();
      }
    } catch (Exception e) {
      System.err.println("ERROR: " + e.getMessage());
    }
  }

}
