import slixmpp
import asyncio
from slixmpp.exceptions import IqError, IqTimeout

class EchoBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.recipient = recipient
        self.message = message

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message_received)
        self.add_event_handler("message_receipt", self.receipt_received)

        # Enable delivery receipts
        self.register_plugin('xep_0184')

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        # Send a message with a receipt request
        self.send_message(mto=self.recipient,
                          mbody=self.message,
                          mtype='chat',
                          mreceipt=True)

        print("Message sent, awaiting receipt...")

    def message_received(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print(f"Received message from {msg['from']}: {msg['body']}")

    def receipt_received(self, msg):
        print(f"Receipt received for message: {msg['id']}")

if __name__ == '__main__':
    # Your JID, password, recipient, and message
    jid = "user@example.com"
    password = "pemba"
    recipient = "user1@example.com"
    message = "Hello from Python!"

    # Create an instance of EchoBot
    xmpp = EchoBot(jid, password, recipient, message)
    
    # Run the XMPP client using asyncio event loop
    xmpp.connect()

    try:
        xmpp.process(forever=False)
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        loop = asyncio.get_event_loop()
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
            try:
                loop.run_until_complete(task)
            except asyncio.CancelledError:
                pass
        loop.close()
