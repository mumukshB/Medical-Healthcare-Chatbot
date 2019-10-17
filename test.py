import re
import time
import spacy
import en_core_web_sm
import pandas as pd
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier


nlp = en_core_web_sm.load()

bot = "BOT: {0}"
user =  "USER: {0}"

intents = {
	'hi' : ['hello','hey','hi!','hi'],
	'bye' : ['goodbye','buhbye','bye'],
	'depression' : ['depressed','sad','worried','despair','misery'],
	'anxiety' : ['anxiety','anxious','nervous','stress','strain','tension','discomfort','tensed']
}

responses = {
	'hi' : 'Hello, i am a medical healthcare chatbot!',
	'bye' : 'Thank you for your time!',
	'default' : 'Sorry, i am not able to understand you'
}

dictionary = {
	'not at all':0,
	'several days' : 0,
	'more than half a day' : 0,
	'all the days' : 0
}

s = {
	'not at all':0,
	'several days' : 1,
	'more than half a day' : 2,
	'all the days' : 3
}

questions = ["Do you have little interest or pleasure in doing things?","Feeling down, depressed, or hopeless","Trouble falling or staying asleep, or sleeping too much","Feeling tired or having little energy","Poor appetite or overeating","Feeling bad about yourself - or that you are a failure or have let yourself or your family down","Trouble concentrating on things, such as reading the newspaper or watching television","Moving or speaking so slowly that other people could have noticed","Thoughts that you would be better off dead, or of hurting yourself"]


def clean_data(data):
    review_text = BeautifulSoup(data,features="html.parser").get_text() 
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    words = letters_only.lower().split()                             
    stops = set(stopwords.words("english"))                  
    meaningful_words = [w for w in words if not w in stops]   
    return( " ".join(meaningful_words))   


def sentiment_analysis(message,vectorizer,forest):
	clean = []
	message = clean_data(message)
	clean.append(message)
	message_features = vectorizer.transform(clean)
	message_features = message_features.toarray()
	result = forest.predict(message_features)
	return result


def depression(name):
	time.sleep(0.8)
	print(bot.format('Gosh, that is tough'))
	time.sleep(0.8)
	print(bot.format('I am sorry to hear that,'),name)
	time.sleep(0.8)
	print(bot.format('Here is a thought that might motivate you!'))
	time.sleep(0.8)
	print(bot.format('There you go...let it all slide out.Unhappiness cannot stick in a person\'s soul when it\'s slick with tear.'))
	#time.sleep(0.8)

def anxiety(name):
	time.sleep(0.8)
	print(bot.format('Gosh, that is tough'))
	time.sleep(0.8)
	print(bot.format('I am sorry to hear that,'),name)
	time.sleep(0.8)
	print(bot.format('Here is a thought that might motivate you!'))
	time.sleep(0.8)
	print(bot.format('Take a deep breath, listen to your thoughts, try to figure them out. Then take things one day at a time.'))


def greet(vectorizer,forest):
	while True:
		print(bot.format('Hello, i am a medical healthcare chatbot!'))
		time.sleep(0.8)
		print(bot.format('Before we proceed, may I know your name?'))
		message = input()
		name = name_extraction(message)
		time.sleep(0.8)
		print(bot.format("Nice to meet you,"),name+"!")
		time.sleep(0.8)
		print(bot.format("How are you feeling today"),name+"?")
		message = input().lower()
		#sentiment = sentiment_analysis(message,vectorizer,forest)
		sentiment = (1,1)
		m_intent = intent(message)
		if sentiment[0]==1 and m_intent=='default':
			print(bot.format("That's awesome! You are showing improvement!"))
		else:
			time.sleep(0.8)
			if(m_intent == 'depression'):
				depression(name)
			else:
				anxiety(name)
			time.sleep(1)
			print(bot.format('I have got great tools for people dealing with stress,wanna give it a go,Yes/No?'))
			time.sleep(0.8)
			message = input().lower()
			#sentiment = sentiment_analysis(message,vectorizer,forest)
			if  message == 'yes':
				print(bot.format("Great! Thanks for trusting me",name))
				time.sleep(0.8)
				print(bot.format("Let's start with a small mental assessment test,so buckle up!"))
				time.sleep(0.8)
				quiz()
			else:
				print(bot.format("Please ask me for help whenever you feel like it! I'm always online."))
	    
	   
	    
	    
def train(vectorizer,forest):
	train = pd.read_csv("labeledTrainData.tsv", header=0, \
                    delimiter="\t", quoting=3)
	num_reviews = train["review"].size
	clean_train_reviews = []
	for i in range(0,num_reviews):
		clean_train_reviews.append(clean_data(train["review"][i]))
	train_data_features = vectorizer.fit_transform(clean_train_reviews)
	train_data_features = train_data_features.toarray()
	forest = forest.fit(train_data_features,train["sentiment"])
	return (vectorizer,forest)
    

def name_extraction(message):
	doc = nlp(message)
	name = ''
	for ent in doc.ents:
		if ent.label_=="PERSON":
			return str(ent)
	x = message.split()
	if len(x)<=2:
		return (x[0])
	elif (' '.join(x[0:3]).lower())=='my name is':
		return ''.join(x[3:])



def intent(message):
	for words in intents.keys():
	    pattern = re.compile('|'.join([syn for syn in intents[words]]))
	    match = pattern.search(message)
	    if match:
	    	return words
	return 'default'

def respond(message):
    word = intent(message)
    return responses[word]


def score():
	sc = 0
	for k in dictionary.keys():
		sc += dictionary[k]*s[k]
	print("Your mental assessmant score is "+sc)


def quiz():
	print()
	print(bot.format("Now we're starting with a small assessment and hopefully at the end of the assessment,we'll be able to evaluate your mental health"))
	print()
	time.sleep(0.8)
	print(bot.format("To respond please type the following answer depending upon your choice"))
	print("A. not at all")
	print("B. several days")
	print("C. more than half a day")
	print("D. all the days")
	print()
	time.sleep(0.5)
	print("Now we'll be starting with the quiz,type okay if you're ready!")
	inp = input().lower()
	if inp == 'okay':
		for sentence in questions:
			time.sleep(0.5)
			print(bot.format(sentence))
			resp = input().lower()
			dictionary[resp]=dictionary[resp]+1
	print()
	print("Thank you for taking the assessment!")
	for k in dictionary.keys():
		print(k,dictionary[k])
	score()



if __name__ == '__main__':
	vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)
	forest = RandomForestClassifier(n_estimators = 100)
	(vectorizer,forest) = train(vectorizer,forest)
	greet(vectorizer,forest)
		
