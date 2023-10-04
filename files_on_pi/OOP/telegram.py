import telepot

### TELEGRAM ###
TELE_TOKEN = '6670579130:AAHkXkTqTLd_vm-H5aASyMByv06p2K8Y5GM'
TELE_SEND_ADDRESS = '6392570521'
device_name =  'matt_test_computer: '

class TelegramBot:
    def __init__(self, device_name):
        self.bot = telepot.Bot(TELE_TOKEN)
        self.device_name = device_name

    def receive_message(self):
        response = self.bot.getUpdates(limit=1, offset=-1)
        if response and 'message' in response[0]:
            message_text = response[0]['message']['text']
            print('Received message:', message_text)
            #return message_text
        else:
            print('No messages received in the last 24 hours')
            #return 'No new messages in the last 24 hours'


    def send_telegram(self, message):
        self.bot.sendMessage(TELE_SEND_ADDRESS, self.device_name + message)
        print('message sent to ' + self.device_name + message)
        #return None

#test code
'''    
bot = TelegramBot("MATT")
bot.send_telegram("message test")
bot.receive_message()
'''