

## Feature Set

### 1. Simple call back / response handling
Simply: user sends a request and the telebot simply pings the ChatGPT API and returns a response in telegram.
The prompt is engineered such that the response from ChatGPT is formatted to fit the character limitations of a telegram message.


### 2. LangChain empowered responses
- In general, all chat history is going to be saved (and, using regex, PIDs will be anonymized - should it be inputted;)
- It should basically first store all conversation as context

- It should also be able to take in or receive documents, text files, pdfs or a whole directory of parsed files.
-- this sparks an important question on how the bot will be used:
--- does it mean that you can send the bot txt files to save? OR does the bot operator have to add the files to the directory themselves?
--- initially, it should be the latter, and then eventually with proper handling of files we could accept .txt or .cal files as context.

Similar to peepo bot, this should have a similar architecture of saving logs of conversations, configs and context files;


### 3. Button and configurations integrations:
- Button to summarize and save the files -> both into a question into a MCQ;
- Settings and configurations for xyz per chat.




### 4. Load up to date coding documentation for up to date usage / guidelines;


### 5. Load up to date coding documentation for up to date usage / guidelines;


### 5. Bug fixes + context aware bug fixes and architecture;
- load


### 6. Birthday and spaced repetition quizzing; Time aware bot / reminder messages -> constant polling or asked;






### Uncategorized;
- __main__ and other types of python specific learning;






