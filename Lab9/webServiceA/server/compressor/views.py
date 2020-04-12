from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from background_task import background
import json
import zipfile,zlib
import os
import io, random, datetime
import threading
import pika
# Create your views here.

@api_view(['POST'])
def compress(request):
  if request.method == 'POST':
    routing_key = request.headers['X-Routing-Key']
    credentials = pika.PlainCredentials('0806444524','0806444524')
    connection = pika.BlockingConnection(
      pika.ConnectionParameters(
        host='152.118.148.95',
        virtual_host='/0806444524',
        credentials= credentials
      )
    )

    channel = connection.channel()
    channel.exchange_declare(exchange='1606878871', exchange_type='direct')
    body = request.data
    # print(body)

    file = body.get('pdf').file
    # print('file', file)

    tempLoc = "temp"
    with open(tempLoc,'wb') as out:
      out.write(file.read())
      out.close()

    zipName = "tmp.zip"
    # zf = zipfile.ZipFile(zipName,mode="w")

    t = threading.Thread(target=compressFile)
    t.start()
    progress = 0.1
    
    while t.is_alive():
      try:
        zip_progress = os.path.getsize("tmp.zip") / os.path.getsize(tempLoc)
        if(zip_progress > progress):
          message = str(int(progress * 100))+" %"
          progress += 0.1
          print(message)
          send_message(message,channel,routing_key)
      except Exception:
        pass

    print("100 %")
    send_message("100 %",channel, routing_key)
    
    res = {
      "result": "File Compressed!"
    }
    os.remove(tempLoc)
    os.remove('tmp.zip')
    return Response(res, status=200)

def compressFile():
  file = "temp"
  try:
    with zipfile.ZipFile("tmp.zip", "w") as zf:
      print("adding "+file)
      zf.write(file, compress_type=zipfile.ZIP_DEFLATED)
  finally:
    print("close zip")

def send_message(message,channel,routing_key):
  channel.basic_publish(
    exchange='1606878871',
    routing_key=routing_key,
    body=message
  )