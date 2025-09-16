# Information-Retrieval

### How to Run the Program

Follow these steps to set up the project in a Google Cloud VM:

1. **Create a Virtual Environment**  
   First, create a virtual environment to isolate the project dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**  
   Install the required libraries:

   ```bash
   pip install requests nltk
   ```

3. **Run the Program**  
   Use the following command to run the program:

   ```bash
   python3 main.py <google_api_key> <google_engine_id> <precision> <query>
   ```

   - Replace `<google_api_key>` with Google Custom Search Engine API Key.
   - Replace `<google_engine_id>` with Google Custom Search Engine Engine ID.
   - Replace `<precision>` with the desired precision level.
   - Replace `<query>` with the search query you want to process.

### Internal Design of the Project

The program iteratively changes a search query. It enhances the query and improves its relevancy by using input from search results. The program's essential elements consist of:

- **Query Modification:** To increase precision, new keywords are added to the query based on user feedback (the relevance of search results).
- **Google Search Integration:** The program retrieves the top 10 search results depending on the query using Google's Search Engine API.
- **Precision Handling:** The precision is assessed following each round of query modification. The program adds new terms to the query if the precision falls short of the desired level. Until the desired level of precision is attained, this procedure keeps going.

### Query-Modification Method

The query-modification approach ranks new keywords using the Rocchio algorithm after choosing them based on feedback from search results. Iteratively, new keywords are added to the query, and depending on user feedback, the query word order may be changed to give priority to the most significant terms. When the desired level of precision is achieved, the program stops changing the query.

### Google Custom Search Engine API Key and Engine ID

Please replace the placeholders `<google_api_key>` and `<google_engine_id>` in the command above with own keys.

### References

- [Stanford IR Book on Term Weighting and Vector Space Model](https://nlp.stanford.edu/IR-book/html/htmledition/scoring-term-weighting-and-the-vector-space-model-1.html)
- Singhal, A. "Modern Information Retrieval: A Brief Overview," IEEE Data Engineering Bulletin, 2001.
- Manning, C. D., Raghavan, P., and Schütze, H. "Introduction to Information Retrieval," Chapter 9: "Relevance Feedback & Query Expansion."
