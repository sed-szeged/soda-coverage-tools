#!/usr/bin/env bash

id="mapdb"
mtype="return"
mkdir -p /home/geryxyz/solo/$id/$mtype
python3.4 ../stable/generate_mutants_testresults.py project=$id git_url=/home/geryxyz/repos/$id.git original_source=/home/geryxyz/solo/$id/original_source annotated_source=/home/geryxyz/solo/$id/annotated_source mutant_source=/home/geryxyz/solo/$id/$mtype/mutant_source mutation_type=$mtype mutant_testresult=/home/geryxyz/solo/$id/$mtype/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics
