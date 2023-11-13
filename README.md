# Atdcodeanalyzer
The Prototype of the ATDCodeAnalyzer Method and Tool

[Proposed Approach](https://github.com/Technical-Debt-Large-Scale/atdcodeanalyzer/blob/main/docs/diagrams/SummaryofSysRepoAnalysis.png)

[Steps of Approach](https://github.com/Technical-Debt-Large-Scale/atdcodeanalyzer/blob/main/docs/diagrams/AnalysisCassandraRepositoryFlow.png)

We identified the need for an automated method to identify classes affected by ATD without relying on expert analysis in software architecture design [1].

We saved all commits and all modified files using the [Pydriller](https://github.com/ishepard/pydriller) tool.

We used the [Arcan](https://essere.disco.unimib.it/wiki/arcan/#:~:text=Arcan%20is%20a%20Java%20software,are%20less%20stable%20than%20itself.) [2] tool and [Designite](https://www.designite-tools.com/) to extract Architectural Smells [3] and Design Smells [4], respectively. 

We loaded these datasets and performed an exploratory data analysis, using various Python libraries and Data Science techniques to identify patterns that could characterize ATD in source code repositories.

We calculated the following metrics to aid our analysis: *cyclomatic complexity*, *file occurrence in commits*, and *accumulated modified LOCs* over time to analyze the source code's behavior related to the maintenance effort. Besides, we used the following Archictural Smells to select files that can indicate architectural issues: *cyclic dependency* and *hub-like dependency*.

## Phases of the Method

### Phase 1

[Extracting main information about commits and modified files](https://github.com/Technical-Debt-Large-Scale/atdcodeanalyzer/blob/main/docs/diagrams/p1.png)

### Phase 2

[Selecting AS and calculate metrics](https://github.com/Technical-Debt-Large-Scale/atdcodeanalyzer/blob/main/docs/diagrams/p2.png)

### Phase 3

[Calculating quartiles and selecting critical files](https://github.com/Technical-Debt-Large-Scale/atdcodeanalyzer/blob/main/docs/diagrams/p3.png)

### Phase 4

[Selecting critial classes](https://github.com/Technical-Debt-Large-Scale/atdcodeanalyzer/blob/main/docs/diagrams/p4.png)

## Samples of Data analyzed

You can access [Cassandra Treemap Repository](https://giselesousar.github.io/cassandra-treemap/) to get Cassandra treemap visualization for each variable analysed.

You can acess [Kafka Treemap Repository](https://armandossrecife.github.io/kafka-treemap/) to get Kafka treemap visualization for each variable analysed.

You can acess [ActiveMQ Treemap Repository](https://armandossrecife.github.io/kafka-treemap/) to get ActiveMQ treemap visualization for each variable analysed.

You can acess [Hadoop Treemap Repository](https://armandossrecife.github.io/kafka-treemap/) to get Hadoop treemap visualization for each variable analysed.

The Treemap and Data extraction are performed by [SysRepoAnalysis](https://github.com/Technical-Debt-Large-Scale/sysrepoanalysis). SysRepoAnalysis is an open-source, multi-user web tool that allows online analysis of git repositories by extracting historical information from source code files over time, using mining software repository techniques [5].

## Referencies

[[1]](https://doi.org/10.1145/3613372.3613399) Sousa, A., Rocha, L. and Britto, R., 2023, September. Architectural Technical Debt-A Systematic Mapping Study. In Proceedings of the XXXVII Brazilian Symposium on Software Engineering (pp. 196-205).

[[2]](https://dl.acm.org/doi/abs/10.1145/2851613.2851963) Fontana, F.A., Pigazzini, I., Roveda, R., Tamburri, D., Zanoni, M. and Di Nitto, E., 2017, April. Arcan: A tool for architectural smells detection. In 2017 IEEE International Conference on Software Architecture Workshops (ICSAW) (pp. 282-285). IEEE.

[[3]](https://ieeexplore.ieee.org/abstract/document/4812762) Garcia, J., Popescu, D., Edwards, G. and Medvidovic, N., 2009, March. Identifying architectural bad smells. In 2009 13th European Conference on Software Maintenance and Reengineering (pp. 255-258). IEEE.

[4] Suryanarayana, G., Samarthyam, G. and Sharma, T., 2014. Refactoring for software design smells: managing technical debt. Morgan Kaufmann. 

[[5]](https://dl.acm.org/doi/abs/10.1145/3555228.3555281) Sousa, A., Ribeiro, G., Avelino, G., Rocha, L. and Britto, R., 2022, October. SysRepoAnalysis: A tool to analyze and identify critical areas of source code repositories. In Proceedings of the XXXVI Brazilian Symposium on Software Engineering (pp. 376-381).
