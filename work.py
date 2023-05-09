from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.types import InputPeerChannel

# Replace the values below with your own
api_id = 27009009
api_hash = 'a5197085aa87788a5730bd3aaf06cd91'
bot_token = '5985008411:AAGi500oaWtIFU0419YKedFVVUSiCwhgvcE'
source_channel = -1875615561
destination_channel = -1768382602

# Create a Telegram client
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Define the event handler for new messages in the source channel
@client.on(events.NewMessage(chats=source_channel))
async def forward_message(event):
    # Forward the message to the destination channel
    full_channel = await client(GetFullChannelRequest(source_channel))
    input_channel = InputPeerChannel(full_channel.full_chat.id, full_channel.full_chat.access_hash)
    await client(ForwardMessagesRequest(from_peer=input_channel, to_peer=destination_channel, id=[event.id]))

# Define the event handler for the bot being online
@client.on(events.ChatAction)
async def send_alive_message(event):
    if event.user_joined or event.user_added:
        # Send the alive message to the source channel
        await client.send_message(source_channel, 'ALIVE ⏰⏰⏰')
        # Delete the alive message after 5 seconds
        await client.delete_messages(source_channel, [event.id], revoke=True)

# Start the client
client.run_until_disconnected()
