id="mapdb"
mtype="return"
mkdir -p /home/geryxyz/mass/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/mass/$id/original_source annotated_source=/home/geryxyz/mass/$id/annotated_source mutant_source=/home/geryxyz/mass/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/mass/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics &>/home/geryxyz/mass/$id/$mtype/log.txt && echo "$id/$mtype done" &

id="mapdb"
mtype="if"
mkdir -p /home/geryxyz/mass/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/mass/$id/original_source annotated_source=/home/geryxyz/mass/$id/annotated_source mutant_source=/home/geryxyz/mass/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/mass/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics &>/home/geryxyz/mass/$id/$mtype/log.txt && echo "$id/$mtype done" &

id="oryx"
mtype="return"
mkdir -p /home/geryxyz/mass/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/mass/$id/original_source annotated_source=/home/geryxyz/mass/$id/annotated_source mutant_source=/home/geryxyz/mass/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/mass/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics &>/home/geryxyz/mass/$id/$mtype/log.txt && echo "$id/$mtype done" &

id="elasticsearch"
mtype="return"
mkdir -p /home/geryxyz/mass/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/mass/$id/original_source annotated_source=/home/geryxyz/mass/$id/annotated_source mutant_source=/home/geryxyz/mass/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/mass/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics &>/home/geryxyz/mass/$id/$mtype/log.txt && echo "$id/$mtype done" &

id="elasticsearch"
mtype="if"
mkdir -p /home/geryxyz/mass/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/mass/$id/original_source annotated_source=/home/geryxyz/mass/$id/annotated_source mutant_source=/home/geryxyz/mass/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/mass/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics &>/home/geryxyz/mass/$id/$mtype/log.txt && echo "$id/$mtype done" &

id="orientdb"
mtype="return"
mkdir -p /home/geryxyz/mass/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/mass/$id/original_source annotated_source=/home/geryxyz/mass/$id/annotated_source mutant_source=/home/geryxyz/mass/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/mass/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics &>/home/geryxyz/mass/$id/$mtype/log.txt && echo "$id/$mtype done" &

id="netty"
mtype="if"
mkdir -p /home/geryxyz/mass/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/mass/$id/original_source annotated_source=/home/geryxyz/mass/$id/annotated_source mutant_source=/home/geryxyz/mass/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/mass/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics &>/home/geryxyz/mass/$id/$mtype/log.txt && echo "$id/$mtype done" &
