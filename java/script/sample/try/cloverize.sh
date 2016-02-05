#!/usr/bin/env bash
for prj in "netty"
do
    mkdir /home/geryxyz/clover-cov/${prj}
    for type in "return"
    do
        mkdir /home/geryxyz/clover-cov/${prj}/${type}
        python3.4 ~/soda-coverage-tools/java/script/sample/try/generate_mutant_coveragedata.py git_url=/home/geryxyz/repos/${prj}.git annotated_source=/home/geryxyz/clover-cov/${prj}/${type}/annotated_source mutant_source=/home/geryxyz/clover-cov/${prj}/${type}/mutant_source mutation_type=${type} mutant_list=/home/geryxyz/clover-cov/M3-${prj}-${type}.list.csv mutant_coveragedata=/home/geryxyz/clover-cov/${prj}/${type} soda_jni_path=/home/geryxyz/soda-java/build/src/main/cpp soda_clover2soda_path=/home/geryxyz/soda-coverage-tools/java/clover2soda/target/clover2soda-0.0.1.jar &> ${prj}-${type}.log.txt
    done
done