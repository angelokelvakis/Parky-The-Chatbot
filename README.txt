Angelo Kelvakis
Version: 1.0
Last Edited: 3/15/23

Welcome to Parky the Chatbot software!
This model uses an SVM model with data inputted from a folder of text documents. The intents are classified by the model and matched with a bot response which is fed back to the user in a simple input / output system that, if given the correct query, will scrape the Chicago Parks Department Event website: https://anc.apm.activecommunities.com/chicagoparkdistrict/activity/search?onlineSiteId=0&locale=en-US&activity_select_param=2&open_spots=1&viewMode=list

The model edits the json file and is then sent to the site through a post, using continually generated cookies. The json data was collected from cURL using the dev tools feature on google chrome. Once the json is posted, it returns a list of activities that the user can do with pagination which is also controlled by sending a separate post command of the same data, with the page number iterated through.

The user interface requires the user to enter their park and their neighborhood before continuing on. This allows the user to use language like 'near me' which enters their neighborhood as the location for the json post. The flow of the main 'enter_chat' function is as follows:
1. Set up user park and neighborhood
2. Query user and enter a loop for basic questions
3. If the user asked a question requiring a web scrape like: "Give me a list of activities I can do at Wilson Park on Wednesday" the extract_keywords function will process the text given the predicted intent assigned by the model. This is compared to lists of days of the week, and lists of all the parks in the database.
4. The json data is constructed, based on what the user entered.
5. The json data is posted to the site and the raw data is returned.
6. The user enters a page loop where the same data is returned, iterating on the page value of the json data.
7. The user can exit the page loop and continue chatting with the bot.

At any point, the user can enter the word 'exit' to end the program.


IMPORTANT FILES
Please make sure to include the raw Intents folder containing all the intent documents to construct the model. The directory path can be found in the run_model function. There is also json file structure data held in the encoding_data file which the path to that file is kept within the init_encoding_data function. If the code is failing to start, please check that these two file paths are set up correctly.