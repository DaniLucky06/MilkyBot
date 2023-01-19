import discord, os, sys, asyncio, requests, random, traceback, json
from keepalive import keep_alive

#from mcstatus import JavaServer

ip = '81.16.61.58'
url = f'https://api.mcsrvstat.us/2/{ip}'
emojilist = ['🇰', '🇪', '🇷', '🇲', '🇮', '🇹']
TOKEN = os.environ["TOKEN"]
apiIP = "127.0.0.1"
cognome = os.environ['cognome']
kermitping = True
prevplayers = []
praisephrases = [
    "Praise Kermit!", "God's will is in Kermit's hand",
    "Your mistakes will have consequences",
    "Kermit will bring salvation for those who praise it", "...just why?",
    "May your L's be many, and your partners few", "**no.**", "Kermit, the immortal"
]
lastpraise = ""
blankstring = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

def filterString(_string):
	_allowedChars = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0"," "]
	_result = ""
	for i in _string :
		if i in _allowedChars:
			_result += i
	return _result

#server = JavaServer.lookup(ip)
#status = server.status()

intents = discord.Intents.all()
client = discord.Client(intents=intents) # I dont fucking know why i had to add the intents thing but eihg 

async def getUserById(username):
    user = await client.fetch_user(username)
    return user

def parseInterestedRoles(_guild):
    userList = []
    usrListTmp = []
    for i in _guild.members:
        interestedRoles = [954349361154900049, 973177697461239828, 991732194483654677, 970767639691546755, 1046194175885971456, 1040337661581344909]
        for j in i.roles:
            if j.id in interestedRoles:
                if i.name not in usrListTmp:
                    usrListTmp.append(i.name)
                    userList.append({
                        "name": filterString(str(i.name)),
                        "discriminator": str(i.discriminator),
                        "id": filterString(str(i.id)),
                        "avatar": str(i.avatar),
                    })
    print(usrListTmp)
    _data ='{ "users": ' + json.dumps(userList) + '}'
    open("./data/users.json","w").write(_data)

@client.event
async def on_ready():
    global prevplayers
    global milkyway
    channel = client.get_channel(973943985552908328)
    channel2 = client.get_channel(1047182602005651628)
    milkyway = client.get_guild(954125943495065661) # Milkyway server ID
    print('Logged in')
    try:
        onlineList = ['oogey boogey onliny booby']
        await channel.send(onlineList[random.randint(0, len(onlineList)-1)])
    except:
        print("Error whilst sending message. Is the bot in the milkyway server with the right privilages? :P")

    parseInterestedRoles(milkyway) # This function gets the interested roles and writes them to ./data/user.json

    while True:
        pars = requests.get(url, ).json()

        if pars['online'] == True:
            online = pars['players']['online']
        else:
            online = 0

        await client.change_presence(activity=discord.Game(
            f'Milkyway, Online: {str(pars["online"])}, {online} players online'
        ))

        players = []
        if online != 0:
            players = list(pars['players']['list'])

        if prevplayers != players:
            if len(prevplayers) <= len(players):
                joinedplayers = list(set(players) - set(prevplayers))
                for p in joinedplayers:
                    try:
                        await channel2.send(f'```diff\n+ {p} joined!\n```')
                    except:
                        pass
            elif len(prevplayers) >= len(players):
                leftplayers = list(set(prevplayers) - set(players))
                for p in leftplayers:
                    try:
                        await channel2.send(f'```diff\n- {p} left!\n```')
                    except:
                        pass
        prevplayers = players

        parseInterestedRoles(milkyway)

        await asyncio.sleep(5)

@client.event
async def on_message(message):
    global kermitping
    global lastpraise
    a = 1
    if message.author == client.user:
        return

    if cognome in message.content.lower():
        await asyncio.sleep(0.2)
        await message.delete()
    # bot channel commands
    if message.channel == client.get_channel(973943985552908328):
        if message.content.startswith(
                '?statsus') or message.content.startswith('?sus'):
            with open('amogus.png', 'rb') as img:
                pic = discord.File(img)
            await message.channel.send(file=pic)

        if message.content.startswith('?kermit'):
            msg = await message.channel.send(
                ':regional_indicator_k: :regional_indicator_e: :regional_indicator_r: :regional_indicator_m: :regional_indicator_i: :regional_indicator_t:'
            )
            for emoji in emojilist:
                await msg.add_reaction(emoji)

        if '🇰' in message.content and '🇪' in message.content and '🇷' in message.content and '🇲' in message.content and '🇮' in message.content and '🇹' in message.content and message.author.id == 525288877771063298:
            for emoji in emojilist:
                await message.add_reaction(emoji)

        if message.content.startswith('?modding'):
            pars = requests.get(url).json()
            modslist = ''
            if pars['online']:
                for mod in pars['mods']['names']:
                    modslist += mod + ', '
                await message.channel.send('The mods are: ' + modslist +
                                           '\n**Total: ' +
                                           str(len(pars['mods']['names'])) +
                                           '**')
            else:
                await message.channel.send('Server offline')

        if message.content.startswith('?har'):
            with open('har.gif', 'rb') as ha:
                har = discord.File(ha)
                await message.channel.send(file=har)

        if message.content.startswith('?platy'):
            await message.channel.send('https://imgur.com/a/6rwwTZI')

        if message.content.startswith('?help'):
            commlist = '?help, ?kermit, ?status, ?statsus, ?sus, ?c, ?modding, ?har, ?platy, ?boycottkermit, ?piston'
            embedHelp = discord.Embed(title='Help', color=0xf00000)
            embedHelp.add_field(name='Commands availiable:', value=commlist)
            await message.channel.send(embed=embedHelp)

        if message.content.startswith(
                '?alph') and message.author.id == 790909302566813717:
            letters = '🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹'
            for letter in letters:
                if letter != ' ':
                    await message.add_reaction(letter)

        if message.content.startswith('?piston'):
            with open('piston.gif', 'rb') as pis:
                piston = discord.File(pis)
                await message.channel.send(file=piston)
    # all channels commands

    if message.content.startswith('?status'):
        pars = requests.get(url).json()
        if pars['online'] == True:
            online = pars['players']['online']
        else:
            online = 0
        embedVar = discord.Embed(title='Server Status', color=0x03a9f4)
        embedVar.add_field(name='Online', value=pars['online'])
        embedVar.add_field(name='Players online:', value=online)
        players = ''
        if online != 0:
            for player in pars['players']['list']:
                players = players + player + ', '
        else:
            players = 'No players online!'
        players = players.rstrip(', ')
        if online != 1:
            embedVar.add_field(name='Players:', value=players)
        else:
            embedVar.add_field(name='Player:', value=players)
        await message.channel.send(embed=embedVar)
        if pars['online'] == False:
            print('server offline')
            #await message.channel.send('<@713656894891491328> the server is offline!')

    if message.content.startswith('?c '):
        towrite = ''
        msg = str(message.content).replace('?c ', '')
        for letter in msg:
            if letter != ' ' and letter.lower() in [
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                    'y', 'z'
            ]:
                towrite += ':regional_indicator_' + letter.lower() + ':'
            elif letter == ' ':
                towrite += '   '
            else:
                towrite += letter
        await message.channel.send(towrite)
        await message.delete()
    if 'wowza' in message.content:
        await message.channel.send('<:wowza:974932545152106606>')

    for word in message.content.lower().split(" "):
        if word == "rip":
            with open('rip-coffin.gif', 'rb') as file:
                gif = discord.File(file)
            await message.channel.send(file=gif)
    
    if message.content.startswith('?nosummon') and (
            message.author.id == 790909302566813717
            or message.author.id == 525288877771063298):
        kermitping = False
        await message.channel.send('Not summoning you')
        await asyncio.sleep(600)
        kermitping = True

    if message.content.startswith('?summon') and (
            message.author.id == 790909302566813717
            or message.author.id == 525288877771063298):
        kermitping = True
        await message.channel.send('I will summon you again!')

    permlist = [
        715057265048289282, 790909302566813717, 548863702334439434,
        713656894891491328, 525288877771063298
    ]
    if message.author.id in permlist and 'kermit i summon you' in message.content.lower(
    ) and kermitping:
        for i in range(5):
            await message.channel.send('<@525288877771063298>')
    if message.author.id in permlist and 'pouffy i summon you' in message.content.lower(
    ) and kermitping:
        for i in range(5):
            await message.channel.send('<@713656894891491328>')
    if message.content.startswith('?boycottkermit'):
        while a == 1:
            chosenpraise = random.choice(praisephrases)
            if chosenpraise != lastpraise:
                lastpraise = chosenpraise
                await message.channel.send(chosenpraise)
                a = 0
            else:
                a = 1
    if str(message.author) == 'DaniLucky#6874' and message.content.startswith(
            '?blank'):
        await message.channel.send(blankstring)
    if str(message.author) == 'DaniLucky#6874' and message.content.startswith(
            '?restart'):
        await message.channel.send(f'Stopping, {message.author}')
        python = sys.executable
        os.execl(python, python, *sys.argv)

    if message.content.startswith(
            '?del ') and message.author.id == 790909302566813717:
        if ', ' not in message.content:
            msg = await message.channel.fetch_message(
                int(message.content.replace('?del ', '')))
            await asyncio.sleep(0.2)
            await msg.delete()
            await message.delete()
        else:
            mess = message.content.replace('?del', '').split(', ')
            await asyncio.sleep(0.2)
            for id in mess:
                msg = await message.channel.fetch_message(int(id))
                await msg.delete()
            await message.delete()

keep_alive()

try:
    client.run(TOKEN)
except:
    print(f'\n\n\nERROR OCCURED WHILST CONNECTING TO DISCORD API: {traceback.print_exc()}\nRESTARTING NOW\n\n\n')
    os.system('python restarting.py')
    os.system("kill 1")
