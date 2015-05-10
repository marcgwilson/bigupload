from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings

from models import Item

import json, os, shutil, datetime, hashlib

# Create your views here.
class GenerateUploadToken(View):
    def post(self, request, *args, **kwargs):
        try:
            token = hashlib.sha224(str(datetime.datetime.now())).hexdigest()
            return JsonResponse({ 'token': token }, status=201)
        except Exception as e:
            print 'e: %s' % e
            return JsonResponse({'status': 'error', 'reason': str(e)})

# file = request.FILES['filename']
# file.name           # Gives name
# file.content_type   # Gives Content type text/html etc
# file.size           # Gives file's size in byte
# file.read()

class ChunkedUpload(View):
    def post(self, request, *args, **kwargs):
        token = request.POST.get('token', None)

        if token is None:
            data = {'result': 'error', 'reason': 'valid upload token missing'}
            status = 400
        else:
            try:
                print 'request.FILES.keys() : %s' % request.FILES.keys()
                print 'request.POST.keys(): %s' % request.POST.keys()
                chunk = request.FILES['chunk']
                
                print 'token: %s' % token
                chunk_data = chunk.read()

                # Create temp upload directory using token if directory doesn't exist.
                directory = os.path.join(settings.TEMP_ROOT, token)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                # print "chunk name: %s, size: %s" % (chunk.name, chunk.size)
                output_path = os.path.join(directory, chunk.name)
                output = open(output_path, 'ab+')
                output.write(chunk_data)
                output.close()
                data = {'result': 'success'}
                status = 201
            except Exception as e:
                print 'error: %s' % str(e)
                data = {'result': 'error', 'reason': str(e)}
                status = 400
        return JsonResponse(data, status=status)


def generate_unique_filename(file_path):
    path, filename = os.path.split(file_path)
    fragments = filename.split('.')
    prefix = '.'.join(fragments[0:-1])
    extension = fragments[-1]

    if os.path.isfile(file_path):
        index = 1
        while os.path.isfile(os.path.join(path, '%s-%s.%s' % (prefix, index, extension))):
            index += 1
        return os.path.join(path, '%s-%s.%s' % (prefix, index, extension))
    else:
        return file_path


class ItemCreate(View):
    def post(self, request, *args, **kwargs):
        try:
            request_data = json.loads(request.body)
            token = request_data['token']

            token_dir = os.path.join(settings.TEMP_ROOT, token)

            # get the first/only file in video_dir
            video_file = os.listdir(token_dir)[0]

            unique_path = generate_unique_filename(os.path.join(settings.MEDIA_ROOT, 'data', video_file))
            shutil.move(os.path.join(settings.TEMP_ROOT, token, video_file), unique_path)
            
            # Now delete temporary directories
            os.rmdir(os.path.join(settings.TEMP_ROOT, token))

            item = Item.objects.create(data = os.path.join('data', os.path.basename(unique_path)))
            
            data = item.to_dict()
            status = 201
        except Exception as e:
            data = {'result': 'error', 'reason': str(e)}
            status = 400
        return JsonResponse(data, status=status)
