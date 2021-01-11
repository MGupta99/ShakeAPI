import os

config = {
    'BUNDLE_ID': os.environ['BUNDLE_ID'],
    'SHAKE_KID': os.environ['SHAKE_KID'],
    'PRIVATE_KEY': os.environ['PRIVATE_KEY'],
    'TEAM_ID': os.environ['TEAM_ID'],
    'MONGO_CONNECTION': os.environ['MONGO_CONNECTION'],
    'TWILIO_SID': os.environ['TWILIO_SID'],
    'TWILIO_AUTH_TOKEN': os.environ['TWILIO_AUTH_TOKEN']
}
