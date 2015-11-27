#!/usr/bin/env bash

function pause(){
    echo "$*"
    #read -p "$*. press [enter] to continue..."
}

id="mapdb"
mtype="return"
mkdir -p /home/geryxyz/$1/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/$1/$id/original_source annotated_source=/home/geryxyz/$1/$id/annotated_source mutant_source=/home/geryxyz/$1/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/$1/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics &>/home/geryxyz/$1/$id/$mtype/log.txt
pause "$id/$mtype is done"

id="mapdb"
mtype="if"
mkdir -p /home/geryxyz/$1/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/$1/$id/original_source annotated_source=/home/geryxyz/$1/$id/annotated_source mutant_source=/home/geryxyz/$1/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/$1/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics &>/home/geryxyz/$1/$id/$mtype/log.txt
pause "$id/$mtype is done"

id="oryx"
mtype="return"
mkdir -p /home/geryxyz/$1/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/$1/$id/original_source annotated_source=/home/geryxyz/$1/$id/annotated_source mutant_source=/home/geryxyz/$1/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/$1/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics &>/home/geryxyz/$1/$id/$mtype/log.txt
pause "$id/$mtype is done"

id="elasticsearch"
mtype="return"
mkdir -p /home/geryxyz/$1/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/$1/$id/original_source annotated_source=/home/geryxyz/$1/$id/annotated_source mutant_source=/home/geryxyz/$1/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/$1/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics &>/home/geryxyz/$1/$id/$mtype/log.txt
pause "$id/$mtype is done"

id="elasticsearch"
mtype="if"
mkdir -p /home/geryxyz/$1/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/$1/$id/original_source annotated_source=/home/geryxyz/$1/$id/annotated_source mutant_source=/home/geryxyz/$1/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/$1/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics &>/home/geryxyz/$1/$id/$mtype/log.txt
pause "$id/$mtype is done"

id="orientdb"
mtype="return"
mkdir -p /home/geryxyz/$1/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/$1/$id/original_source annotated_source=/home/geryxyz/$1/$id/annotated_source mutant_source=/home/geryxyz/$1/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/$1/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics &>/home/geryxyz/$1/$id/$mtype/log.txt
pause "$id/$mtype is done"

id="netty"
mtype="if"
mkdir -p /home/geryxyz/$1/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/$1/$id/original_source annotated_source=/home/geryxyz/$1/$id/annotated_source mutant_source=/home/geryxyz/$1/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/$1/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics &>/home/geryxyz/$1/$id/$mtype/log.txt
pause "$id/$mtype is done"
