import ssl, re, urllib, json, telebot;
from urllib.request import urlopen

bot = telebot.TeleBot('BOT-TOKEN');
context = ssl.SSLContext()

def getattachment(name):
    response = urlopen('https://stalcraft.wiki/_next/data/qiM5yjo753IBQuV-V9pRu/ru/items/attachments.json?category=attachments', context=context)
    if response:
        data = json.load(response);
        att_data = data['pageProps']['data'];
        items = {};

        for item in att_data:
            id = item['exbo_id']
            name_ru, name_en = item['lines']['ru'], item['lines']['en']
            if (name.lower() in name_ru.lower() or name.lower() in name_en.lower()) and name_ru not in items:
                items[name_ru] = id;
        return True, items;
    else:
        return False, 'меня послали нахуй, с моим запросом =)'

def canattach(name, wep):
    result = getattachment(name);
    if result[0] == False:
        return result[1]
    
    result = result[1];
    suitables = {};
    
    for name in result:
        id = result[name];
        
        response = urlopen('https://stalcraft.wiki/_next/data/qiM5yjo753IBQuV-V9pRu/ru/items/attachments/' + id + '.json?category=attachments&item=' + id, context=context)
        if response:
            data = json.load(response);
            suitable = data['pageProps']['data']['suitableFor']

            for item in suitable:
                name_ru, name_en = item['lines']['ru'], item['lines']['en']
                if (wep.lower() in name_ru.lower() or wep.lower() in name_en.lower()) and name not in suitables:
                    suitables[name] = True
        else:
            return False, 'меня послали нахуй, с моим запросом =)'

    return result, suitables

@bot.message_handler(content_types=['text'])
def start(message):
    split = message.text.split(' ', 1)
    if len(split) > 1:
        args = re.findall(r'"([^"]*)"', split[1])
        if not args:
            args = message.text
    else:
        args = message.text.split(' ')[1:]

    if message.text.startswith('/suitable'):
        if len(args) >= 2:
            bot.send_message(message.from_user.id, 'ща чекну');
            print(args)

            result = canattach(args[0], args[1])
            if len(result) <= 1:
                bot.send_message(message.from_user.id, result);
                return
            elif result[0] == False:
                bot.send_message(message.from_user.id, result[1]);
                return

            atts = result[0]
            suitables = result[1]

            text = ' ';
            for name in atts:
                text += name + ': ' + ('✔️' if name in suitables else '❌') + '\n'

            bot.send_message(message.from_user.id, text);
        else:
            bot.send_message(message.from_user.id, 'затупок ебанный два аругмента здесь два');
    else:
        bot.send_message(message.from_user.id, 'пошел нахуй неизвестная команда ебанный в рот');

bot.polling();

# if __name__ == "__main__":
#     print(canattach('ПП-91', 'АКС-74У'))