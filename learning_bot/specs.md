

## Core Features v1:
- Ability to have a simple conversation with the user based on certain commands
- Integration with Chat-GPT (3.5 or 4) enabling the /GPT "Message" command feature where users are able to talk directly to ChatGPT using telegram

## Core Features v2:
### Commands to manipulate and save responses from GPT

#### /summarize
- Command to "summarize" a response into key bullet points of what needs to be remembered / learnt
-- /summarize (in-reply to message to be saved)
-- summarizing will be done in a specific format such that the first line may be the topic and the key to later access saved conversations.

#### /save
- Command to "save" lessons or responses into a separate log (likely, a txt file in v1)
-- /save (in-reply to a message to be saved)

The common usage here would be to "summarize" a specific response from GPT and "save" it for later remind / usage


### Command to display, access and manage saved summaries and messages
#### /display_saved
- Command to "display" all lessons learnt so far and provide options for all of the 
-- /display_saved
-- returns a list of all the saved messages and filenames
a

#### /read
- Command to "read" a saved message
-- /read 

#### /delete
- Command to "delete" a saved message in the directories


# Core Feature v3:
v3 mainly contains the features for accelerated learning tools to allow for users to effectively learn and retain the lessons learned through GPT
The commands are around creating quizzes (potentially, even MCQs, but mostly dialogue based) and testing the users on key intervals to accelerate learning and retention through [spaced repeition](https://en.wikipedia.org/wiki/Spaced_repetition)

#### /generate_quiz


#### /test


#### /retain



NOTE:
A couple days to spec the project out, and then ideas on implementation / solutions using OOP.
A day or two to map out the modular development timeline / sequencing of what to develop.
Then executing and building, testing accordingly.
