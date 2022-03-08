# iKNOW
Leveraging Knowledge Graphs for iDiv and Biodiversity

This repository is dedicated to our research in tool management in Knowledge Graph platforms. 
We propose a semantic feature-based recommendation system to help users find suitable tools for the Knowledge Graphs generation process.

## Parameters
We identified four important parameters to be considered:
- **Available tools in the platform**: A list of available tools in each step of KG creation along with their characteristics should be accessible for the matcher.
- **Dataset or intermediate result**: The matcher needs to know the characteristics of the initial dataset in the first step and the intermediate results in other steps of the KG creation. These characteristics, such as the size of data or format type, affect choosing the proper tool in each step.
- **User request**: The matcher should suggest a set of tools to users according to their requests.
- **Previous choices of the user**: E.g., if the user tends to use a specific tool for a particular dataset, the matcher should consider the previous choices. 

## Features
We used [OntoSoft-VFF](http://ontosoft-earthcube.github.io/ontosoft/ontosoft%20ontology/v1.0.1/doc/) to describe these four parameters (For the full list, please check the OntoSoft-VFF page):

<table>
<thead>
  <tr>
    <th></th>
    <th>Features</th>
    <th>Description</th>
    <th>Values</th>
    <th>Type of features</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="19">Tool</td>
    <td>FileI/O</td>
    <td>Indicates a file based input to, or file based output from a software</td>
    <td>file type e.g., csv, txt</td>
    <td>Primary</td>
  </tr>
  <tr>
    <td>Function</td>
    <td>The functions of the software</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>InputParameter</td>
    <td>Indicates a parameter used by a software</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>Input</td>
    <td>The input of the software</td>
    <td>text based value</td>
    <td>Primary</td>
  </tr>
  <tr>
    <td>Output</td>
    <td>The output of the software</td>
    <td>text based value</td>
    <td>Primary</td>
  </tr>
  <tr>
    <td>Algorithm</td>
    <td>The algorithm of the software</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>Identifier</td>
    <td>A text based identifier</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>MeasurementEntity</td>
    <td>A numeric value with units</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>Software</td>
    <td>A tool includes one or more function(s) supporting a specific purpose.</td>
    <td>name of the software</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>SoftwareCategory</td>
    <td>A category of the software</td>
    <td>text based value e.g., cleaning, NER, interlinking, visualization, etc.</td>
    <td>Primary</td>
  </tr>
  <tr>
    <td>SoftwareVersion</td>
    <td>A version of a piece of software</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>UseLimitations</td>
    <td>The constraints on use, situations it is not designed for, simplifications</td>
    <td>text based value</td>
    <td>Primary</td>
  </tr>
  <tr>
    <td>hasDependency</td>
    <td>What other software does the software version require to be installed?</td>
    <td>text based value</td>
    <td>Primary</td>
  </tr>
  <tr>
    <td>hasAverageRunTime</td>
    <td>Runtime of this software version on average</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>affectsSoftwareFunction</td>
    <td>Parameters that affect the software function</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>hasInputFile</td>
    <td>The required input file of the function</td>
    <td>text based value</td>
    <td>Primary</td>
  </tr>
  <tr>
    <td>hasInputFileArgument</td>
    <td>The argument of the input file</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>hasInputFileDataType</td>
    <td>The input file type</td>
    <td>text based value e.g., String, Tabular, Text, etc.</td>
    <td>Primary</td>
  </tr>
  <tr>
    <td>hasInputFileDataFormat</td>
    <td>The data format of the input file</td>
    <td>text based value</td>
    <td>Primary</td>
  </tr>
  <tr>
    <td rowspan="6">Dataset</td>
    <td>DataFormat</td>
    <td>Format of data</td>
    <td>text based value e.g., JSON, RDF, HTML, etc.</td>
    <td>Primary</td>
  </tr>
  <tr>
    <td>DataType</td>
    <td>Type of data</td>
    <td>text based value e.g., String, Tabular, Text, etc.</td>
    <td>Primary</td>
  </tr>
  <tr>
    <td>Identifier</td>
    <td>A text based identifier of the dataset</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>hasVersionId</td>
    <td>The version id of the dataset</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>MeasurementEntity</td>
    <td>desired processing run time (a numeric value with units)</td>
    <td>text based value in the time unit</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>hasAverageRunTime</td>
    <td>desired processing run time (a numeric value with units)</td>
    <td>text based value in the time unit</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td rowspan="4">User request</td>
    <td>hasVersionId</td>
    <td>version of dataset</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>Algorithm</td>
    <td>desired algorithm type</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>MeasurementEntity</td>
    <td>desired processing run time (a numeric value with units)</td>
    <td>text based value in the time unit</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>hasAverageRunTime</td>
    <td>desired processing run time (a numeric value with units)</td>
    <td>text based value in the time unit</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td rowspan="2">User history</td>
    <td>hasVersionId</td>
    <td>A version of the previously used dataset</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td>Algorithm</td>
    <td>used algorithm type</td>
    <td>text based value</td>
    <td>Auxiliary</td>
  </tr>
  <tr>
    <td rowspan="17">Features for the tools embedding process</td>
    <td>DockerImage</td>
    <td>A docker image available for this software version</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>DockerImageInstructionInformation</td>
    <td>Information about how to run the docker image of this software</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>ImplementationDetails</td>
    <td>Details about implementation of the code (parallelization, etc)</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>License</td>
    <td>A class of licenses that the software is released under</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>OperatingSystem</td>
    <td>Operating Systems that the software runs on</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>ProgramingLanguage</td>
    <td>The class of programming languages</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>SoftwarePublisher</td>
    <td>An agent that publishes software</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>SoftwareDescription</td>
    <td>An informal text-based description of software</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>Location</td>
    <td>A location URL</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>UseLimitations</td>
    <td>Constraints on use of the software, any simplifications, situations it isn't designed for</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>UsesAndAssumptions</td>
    <td>Description of how the software is used, and any assumptions made for using the software</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>hasActiveDevelopment</td>
    <td>How is the software being developed or maintained?</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>hasDependency</td>
    <td>What other software does the software version require to be installed?</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>hasEmailContact</td>
    <td>What is the e-mail contact for this software?</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>hasExecutableLocation</td>
    <td>What is the URL for the executable?</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>hasFunctionInvocation</td>
    <td>What is the invocation line for this function?</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>requiresAverageMemory</td>
    <td>The memory requirements for this software version</td>
    <td>-</td>
    <td>-</td>
  </tr>
</tbody>
</table>

## More 
We plan to apply the proposed matcher in the KG generation platform in the biodiversity domain at the [iKNOW project](https://planthub.idiv.de/iknow).

Our research study is submitted to the [ESWC Poster and Demo track](https://2022.eswc-conferences.org/call-for-posters-and-demos/).
