# Machine Learning for Biomedical Imaging at the NIH

## Why are scientists interested?

* **One imaging trend**: growing capacity for and use of high-throughput imaging techniques across many imaging modalities. Datasets become difficult or impossible to analyze by hand.

* Computer vision offers to automate tedious data analysis tasks such as object detection, classification, and segmentation. Automation difficulty is data dependent - some tasks are easy and have been solved for decades. Harder ones remain significant bottlenecks to ongoing research efforts. **Examples**:
  - Large-scale biological structure segmentation in SBF-SEM and FIB-SEM.
  - Full-body cell detection, classification, and tracking during model organism development using optical fluorescence microscopy techniques[_?_]
  - [_What else?_]

* Right now, successfully applying new machine learning techniques (buzzword is "deep learning" but we should just say "neural networks") to the aforementioned problems requires both research and scientific computing/software development.

## Should we do anything about it?

* One possibility: 5 years from now, all of our imaging machine learning needs can be taken care of by turnkey commercial solutions. In that circumstance, it might not make sense to take active measures to support machine learning. I don't think this will be the case, however. **Why?**
  - There remain long-standing computer vision problems which are easily stated but remain out of reach, which are at the heart of the NIH's machine learning needs for imaging - basically, understanding an image the way a human does. 
  - Even incremental progress has brought great gains to many fields of science and technology, and our ability to fully exploit high-throughput imaging tools is tied to that progress. 
  - I don't think anybody in computer vision believes image understanding will be completely solved in the next 5-10 years. In the meantime progress is being made, and I believe the NIH should be producers, not just consumers, of that progress.
* Restricting ourselves to the vision problems relevant to biomedicine, there are several domains where the NIH may have a comparative advantage, assuming we can get enough of a team together:
  (1) "Universal" biomedical segmentation algorithms.
  (2) "Universal" computer assisted diagnostic algorithms.
  (3) "Universal" cell tracking and labeling algorithms.
  (4) [_What else?_]
  - "Universality": Algorithms which work across different problem instances without extensive retraining/supervised data generation. By problem instances, I mean different biological specimen type, different preparation conditions, different image acquisition methods, [_anything else?_].
  - A trans-institute machine learning team could greatly benefit from the data available across the spectra of imaging modalities and biological structure types.
* Even partial solutions have direct benefits for labs here and elsewhere.
* Even ignoring machine learning, labs at the NIH would benefit from better support for data science and scientific computing. Putting together and scaling an effective analysis pipeline for a high-throughput imaging device requires specialized scientific computing support, even when individual pipeline elements are addressing solved problems.
* Better support for machine learning and large-scale data analysis is integral to projects that are probably about 5 years away from completion if started today, such as:
  - Nanoscale 3D EM maps of macroscopic biological tissue structures (larval zebrafish brain, what about all the other organ systems?)
  - Microscale 4D whole-body developmental maps of model organisms using optical [_fluorescence?_] microscopy.
  - Safe, low-cost diagnostic software and hardware for medically-underserved regions. 
  - [_Surely there are other things_]
* If we manage to solve those problems, does anybody here believe we won't think of bigger ones?

## NIH machine learning 5 years from now

* TODO but i think we could do some great things. Expand on the project descriptions mentioned above as being about 5 years from completion.

## Organizational structure

### Machine learning support

* **Idea**: One centralized support group for machine learning for biomedical imaging.
* Scientific programmers in staff scientist or contractor roles, liasing with individual imaging labs to integrate machine learning tools (and other advanced scientific computing elements) into research pipelines.
* Group benefits from sharing process knowledge across image problem instances. **Example**: Even if labs have different image segmentation needs, the process for developing a segmentation pipeline for each lab will be broadly similar.
* Would support the NIH's intramural research programs, but would not engage in its own independent machine learning research projects.
* Look to the AIM resource for an organizational model. The AIM group puts together new microscopy hardware, then disseminates and supports it. We need a group that puts together new imaging software, then disseminates and supports it.

### Machine learning research

* In addition to machine learning support for biomedical research, there is also research that can be done at the NIH which would likely be of interest to the machine learning community if done right.
* Example: Progress towards "universal"-type algorithms described above for biomedical domains.
* In general, there are research problems which blur the line between machine learning and its application to biomedicine. The NIH already has examples of labs in this area, for example in the NLM or Ron Summers' group in the CC.
* **Idea**: Leave the research groups formally decentralized, but keep building up trans-institute lines of communication through SIGs, listservs, Slack channels, etc., to allow for more effective knowledge sharing. Such groups would also liaise with the hypothetical machine learning support group for software engineering assistance and to help disseminate innovations to other labs.
* Institutes that are strongly interested in expanding machine learning research relevant to their mission can just individually hire PIs.
