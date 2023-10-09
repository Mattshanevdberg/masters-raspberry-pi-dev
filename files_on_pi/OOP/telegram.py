import telepot
import sys
import time

### TELEGRAM ###
TELE_TOKEN = 'token'
TELE_SEND_ADDRESS = 'send_address'

class TelegramBot:
    def __init__(self, device_name):
        self.bot = telepot.Bot(TELE_TOKEN)
        self.device_name = device_name
    
    def print_error_to_file(self, e, function_name):
        #TESTED: 06-10-2023
        #print regular first
        print((f"Error in TelegramBot.{function_name}: {str(e)}"))
        # Store the original stdout stream
        original_stdout = sys.stdout
        # set output path
        file_path = time.strftime('%Y-%m-%d_%H-%M') + '_output_log.txt'
        # Call the function to redirect output to a file
        sys.stdout = open(file_path, 'w')
        print(f"Error in TelegramBot.{function_name}: {str(e)}")
        sys.stdout.close() #close the file
        sys.stdout = original_stdout  # Restore the original stdout
        #print((f"Error in TelegramBot.{function_name}: {str(e)}"))

    def get_text_after_last_colon(self, input_string, mode):
        #TESTED: 06-10-2023
        last_colon_index = input_string.rfind(':')
        if last_colon_index != -1:
            new_string = input_string[last_colon_index + 1:].strip()
            #remove the blank space if there is one
            if new_string[0] == ' ':
                new_string = new_string[1:]
            return new_string
        else:
            self.send_telegram('it seems that you did not include a colon in your message. The format to change the mode is: "user_name:mode" or "all:mode".The current mode will remain. Please try again.')
            return mode

    def receive_message(self, mode):
        #TESTED 06-10-2023 - still need to test no message for 24 hours
        '''returns the last message sent to the bot if it was addressed to it or all
            Params: current_mode
            Returns: new_mode (if changed)'''
        try:
            response = self.bot.getUpdates(limit=1, offset=-1)
            if response and 'message' in response[0]:
                message_text = response[0]['message']['text']
                #print('Received message:', message_text)
                #check that messages is for bot
                if self.device_name in message_text or 'all' in message_text:
                    return self.get_text_after_last_colon(message_text, mode)
                else:
                    self.send_telegram('Please address the message to all or a user_name. The format to change the mode is: "user_name:mode" or "all:mode". The current mode will remain. Please try again.') 
                    return mode 
            else:
                return mode
                #return 'No new messages in the last 24 hours'
        except Exception as e:
            # print error to file
            function_name = 'receive_telegram'
            self.print_error_to_file(e, function_name)
            return False

    def send_telegram(self, message):
        #TESTED: 06-10-2023
        '''sends message
            Params: message_to_be_sent'''
        try:
            self.bot.sendMessage(TELE_SEND_ADDRESS, self.device_name + ': ' + message)
            return True
        except Exception as e:
            # print error to file
            function_name = 'send_telegram'
            self.print_error_to_file(e, function_name)
            return False            

#test code
#TESTED: 06_10_2023
#bot = TelegramBot("matthew")
#print(bot.send_telegram("message test"))
#print(bot.receive_message('test'))