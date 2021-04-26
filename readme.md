# Music Analysis | Spotify Dataset

This little project it is about exploring a Kaggle Dataset, obtained by using the Spotify API.  
At first, I just begun by exploring the datasets to see what interesting insights could be found.  


In one of my explorations i realized that songs from the 30's and 40's seemed to be lots more lyrical that the newer ones, less danceable. That made me thinkgit di of the hypothesis that that could be related to the WW II, by artists making more songs about war so I created a scraper for this.  
The scrapers search for the lyrics of the songs and then the data retrieved is consumed by one of the notebooks.  

### Notebooks

Notebooks are located in the **notebooks/** directory. In there you will find three notebooks with the work I have done so far

### Scraper

Scraper is located in the **scraper/** directory. This scraper is written to be able to use selenium or by simple requests by just changing some calls to methods

### Datasets

The input datasets are located in the **in/** directory. These are the datasets from Kaggle  
the output datasets (retrieved by the scraper) are located at the **out/** directory
