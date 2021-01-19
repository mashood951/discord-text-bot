import discord
from decouple import config
from discord.message import Message
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

hello = ["hello", "hey", "hi", "hello!", "hey!", "hi!"]

good_health = ["fine", "doing good"]

sad_words = ["sad", "depressed", "depressing", "unhappy", "angry", "miserable"]

thanks = ["thanks", "thankyou", "thank you", "thank"]

starter_hello = [
    "Hello!",
    "Hey!",
    "Hi there!",
    "Hey! How are you?"
]

starter_good_health = [
    "Glad to hear that!"
]

starter_encouragements = [
    "Cheer up!",
    "Hang in there.",
    "You are a great person!",
    "Don't be sad! Watch the beauty of world.",
    "This world needs a hero. And that hero is you!"
]

starter_thanks = [
    "You are welcome",
    "No worries",
    "No problem",
    "I will always be here for you."
]

if "responding" not in db.keys():
    db["responding"] = True

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " ---> " + json_data[0]['a']
    return(quote)

def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]

def delete_encouragements(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    if message.content.startswith("$bot"):
        value = message.content.split("$bot ", 1)[1]

        if value.lower() == "on":
            db["responding"] = True
            await message.channel.send("Bot is turned on.")
        elif value.lower() == "off":
            db["responding"] = False
            await message.channel.send("Bot is turned off.")

    if db["responding"]:
        if any(word in msg for word in hello):
            await message.channel.send(random.choice(starter_hello))

        if any(word in msg for word in good_health):
            await message.channel.send(random.choice(starter_good_health))

        if message.content.startswith('$inspire'):
            quote = get_quote()
            await message.channel.send(quote)

        # if message.content.startswith('$speak'):
            # speak_message = message.content.split("$speak ", 1)[1]
            
        if message.content.startswith('$help'):
            await message.channel.send(
                "**Use $ as prefix**\n\n"
                "**DON'T WRITE <> BRACKETS**\n"
                "It is still in its development phase\n"
                "This is a chat bot that will reply to your comments\n\n"
                "**$bot**\non for turing on and off\n"
                "for turning off\n\n**$inspire**\nFor getting inspiration quote\n\n"
                "**$add**\nFor adding replies to sad comments\n$add <Your comment>\n\n"
                "**$del**\nFor deleting your added comments\n$del <number of your comment starts with 0>\n\n"
                "**$list**\nFor displaying list of your added replies from database"
            )


        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(starter_encouragements))
        
        if any(word in msg for word in thanks):
            await message.channel.send(random.choice(starter_thanks))

        if message.content.startswith("$add"):
            encouraging_message = message.content.split("$add ", 1)[1]
            update_encouragements(encouraging_message)
            await message.channel.send("Your message added to database.")

        if message.content.startswith("$del"):
            encouragements = []
            if "encouragements" in db.keys():
                index = int(message.content.split("$del ", 1)[1])
                delete_encouragements(index)
                encouragements = db["encouragements"]
                await message.channel.send(encouragements)

        if message.content.startswith("$list"):
            encouragements = []
            if "encouragements" in db.keys():
                encouragements = db["encouragements"]
            await message.channel.send(encouragements)


token = config('TOKEN')
keep_alive()
client.run(token)