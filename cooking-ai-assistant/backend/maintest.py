# bot.py

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer,ChatterBotCorpusTrainer
chatbot = ChatBot("Chatpot")

trainer = ListTrainer(chatbot)
trainer.train([
    "Hi",
    "Welcome, friend 🤗",
])
trainer.train([
    "Are you a plant?",
    "No, I'm the pot below the plant!",
])
trainer = ListTrainer(chatbot)
trainer.train([
        "Hi there!",
        "Hello! How can I help you?",
        "What are your hours?",
        "Our hours are 9 AM to 5 PM, Monday through Friday.",
        "Thank you.",
        "You're welcome!"
])


exit_conditions = (":q", "quit", "exit")
while True:
    query = input("> ")
    if query in exit_conditions:
        break
    else:
        print(f"🪴 {chatbot.get_response(query)}")

# hrbot = ChatBot(name="ttttttt",read_only=True,logic_adapters=["chatterbot.logic.BestMatch"])
# corpur_trainer = ChatterBotCorpusTrainer(hrbot)
# corpur_trainer.train("chatterbot.corpus.english")

# print(hrbot.get_response("hello"))


