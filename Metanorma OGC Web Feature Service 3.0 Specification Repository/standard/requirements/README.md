This is the README for the POI Requirements section of the specification. Most of the WFS requirements have been deleted from this folder, however, the "core" and "html" and the requirements class core .adoc have been kept for purposes of illustration and to provide a template for POI Requirements. 

Original README text below:

This folder contains requirements description.

Each file is a single requirement. The naming convention for these files is:

"REQn.adoc" where "n" corresponds to the requirement number. Numbers should have preceeding zeros appropriate for the total number of requirements in the project (e.g., the first requirement could be REQ001 if less than 1000 requirements are anticipated).

The requirement files are integrated into the main document as links.

The requirement is expressed according to this pattern:

NOTE: for each requirement, there should be a corresponding Abstract Test in the "abstract_tests" folder.

NOTE: sample code may reference one or more requirements and should state which requirements are included in the code by adding the following line to the Extended Description:

"#REQS: reqnum1,reqnum2,...reqnumn"
