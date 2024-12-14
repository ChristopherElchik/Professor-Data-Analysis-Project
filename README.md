# Professor Insights: Clustering Quality and Difficulty Across NCSU Colleges

## Project for CSC522: Automated Learning and Data Analysis

This was a group project completed by Christopher Elchik, Nathan Lorenc, Brandon Troy, and Rishi Jeswani for a graduate data mining course at North Carolina State University.

This was a data science project that uses the [RateMyProfessors](https://www.ratemyprofessors.com/) website to scrape data on professors and their ratings, and [Gradient](https://gradient.ncsu.edu/) to scrape data on grade distributions for each professor. The data was then used to cluster the professors based on their quality, difficulty, and average GPA, and identify similarities and differences of the rating distributions across colleges.

[Link to the research paper where we discuss our findings](https://github.com/ChristopherElchik/Professor-Data-Analysis-Project/blob/db0ab9a398ed5222983c6502594471dca9065b92/paper/P8_Professor_Clustering.pdf)

### Usage

The pipeline for this project is broken down into the following files:
- [data_collection.ipynb](data_collection.ipynb): This notebook scrapes, processes, and aggregates the data into a single CSV file appropriate for analysis.
- [aggregate_analysis.ipynb](aggregate_analysis.ipynb): This notebook, for data exploration, generates plots which visualize the aggregate distribution of the data.
- [clustering_eval.ipynb](clustering_eval.ipynb): This notebook is used to determine the optimal clustering algorithm and hyperparameter values for the data.
- [college_clustering.ipynb](college_clustering.ipynb): This notebook executes the clustering algorithm on the data and generates 2D and 3D plots which visualize the clustering results across the colleges.

All of the processed data is stored in the `data` directory, so the `data_collection.ipynb` notebook does not need to be re-ran unless the scraping or pre-processing logic needs to be updated (both of those tasks can be ran separately). If you do need to re-run the scraping for Gradient, follow the instructions in the data collection notebook to set up your authorization headers.

The source files for the paper can be found in the `paper` directory. The final PDF version of the paper itself is [P8_Professor_Clustering.pdf](paper/P8_Professor_Clustering.pdf).

To run the pipeline, you will need to install the following Python packages:

- [NumPy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [Scikit-learn](https://scikit-learn.org/)
- [Seaborn](https://seaborn.pydata.org/)

