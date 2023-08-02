import json

import cv2
import requests
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from api.models import Vehicle


@api_view(['POST'])
def get_details(request):
    if request.method == "POST":
        image_file = request.FILES.get('image')
        selected_services = request.POST.get('services')
        location = request.POST.get('location')
        maxreads = request.POST.get('reads')
        if image_file is not None:
            multipart_data = {
                'image': (image_file.name, image_file),
                'service': (None, selected_services),
                'location': (None, location),
                'maxreads': (None, maxreads),
            }
            resp = requests.post('https://api.cloud.adaptiverecognition.com/vehicle/eur',
                                 files=multipart_data,
                                 headers={'X-Api-Key': '46c567c67bea7b5129710bac47e18417504586ed'})

            if resp.ok:
                resp_dict = json.loads(resp.text)
                data = Vehicle.objects.create(data=resp_dict)
                data.save()
                messages.success(request, "Submitted Successfully")
            else:
                messages.error(request, f"API Error: {resp.status_code} - {resp.reason}")

        else:
            messages.error(request, "No image file found in the request.")
        return redirect('/')
    return render(request, 'index.html')


@api_view(['GET'])
def vehicle_list(request):
        data = Vehicle.objects.all()
        vehicle_data = []

        for vehicle in data:
            data_dict = vehicle.data
            if 'data' in data_dict and 'vehicles' in data_dict['data'] and len(data_dict['data']['vehicles']) > 0:
                vehicle_info = data_dict['data']['vehicles'][0]
                plate_info = vehicle_info.get('plate', {})
                mmr_info = vehicle_info.get('mmr', {})
                plate_found = plate_info.get('found', False)
                country = plate_info.get('country', '')
                unicode_text = plate_info.get('unicodeText', '')
                separated_text = plate_info.get('separatedText', '')
                category = mmr_info.get('category', '')
                mmr_make = mmr_info.get('make', '')
                mmr_model = mmr_info.get('model', '')
                vehicle_data.append({
                    'plate_found': plate_found,
                    'country': country,
                    'unicode_text': unicode_text,
                    'separated_text': separated_text,
                    'category': category,
                    'mmr_make': mmr_make,
                    'mmr_model': mmr_model
                })
            else:
                messages.warning(request, "No vehicle data found for this entry.")


        # Pagination
        paginator = Paginator(vehicle_data, 10)
        page = request.GET.get('page')

        try:
            vehicles = paginator.page(page)
        except PageNotAnInteger:
            vehicles = paginator.page(1)
        except EmptyPage:
            vehicles = paginator.page(paginator.num_pages)
        return render(request, 'list_vehicle.html', {'vehicles': vehicles})


def index(request):

    return render(request, 'index.html')

def video_index(request):

    return render(request, 'video_index.html')


@api_view(['POST'])
def process_video(request):
    if request.method == 'POST':
        # Get the video file from the request
        video_file = request.FILES.get('video')
        print("video_file", video_file)
        if video_file is not None:
            # Create a VideoCapture object to read the video
            video_path = default_storage.save('tmp_video.mp4', ContentFile(video_file.read()))
            print("video_path", video_path)

            video_capture = cv2.VideoCapture(video_path)
            # Set the parameters for image capture (adjust as needed)
            capture_interval = 30  # Capture an image every 30 frames
            frame_count = 0
            screenshots = []

            while True:
                # Read a frame from the video
                ret, frame = video_capture.read()

                if not ret:
                    # Break the loop if no more frames
                    break

                frame_count += 1

                if frame_count % capture_interval == 0:
                    # Append the frame to the screenshots list
                    screenshots.append(frame)

            # Release the video capture object
            video_capture.release()

            # Process the screenshots (send to API, save to disk, etc.)
            for i, screenshot in enumerate(screenshots):
                # Convert the NumPy array to a JPEG image (you can change the format if needed)
                _, buffer = cv2.imencode('.jpg', screenshot)
                image_data = buffer.tobytes()

                # Prepare the multipart data with the captured image
                multipart_data = {
                    'image': ('screenshot.jpg', image_data),
                    'service': (None, 'anpr,mmr'),  # Other services as required
                    'location': (None, 'HUN'),  # Change this based on user selection
                    'maxreads': (None, 1),
                }

                # Send the request to the Adaptive Recognition API
                api_url = 'https://api.cloud.adaptiverecognition.com/vehicle/eur'
                api_key = '46c567c67bea7b5129710bac47e18417504586ed'  # Replace this with your actual API key
                headers = {'X-Api-Key': api_key}
                resp = requests.post(api_url, files=multipart_data, headers=headers)
                print("resp", resp.text)
                resp_dict = json.loads(resp.text)
                print("resp.dict", resp_dict)
                # Rest of the view code...

            # Return a JSON response with the results
            return JsonResponse({'message': 'Video processing completed.'})
        else:
            return JsonResponse({'error': 'No video file found in the request.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


@api_view(['POST'])
def webcam_video(request):
    if request.method == 'POST':
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        # Check if video file was uploaded or webcam is used
        print("request", request)
        using_webcam = 'webcam' in request.POST
        print("using_webcam", using_webcam)
        print("**********************")
        # Use webcam for video capture
        video_capture = cv2.VideoCapture(0)  # 0 indicates the default webcam

        # Set the parameters for image capture (adjust as needed)
        capture_interval = 30  # Capture an image every 30 frames
        frame_count = 0
        screenshots = []

        while True:
            # Read a frame from the video
            ret, frame = video_capture.read()
            if not ret:
                # Break the loop if no more frames
                break

            frame_count += 1

            if frame_count % capture_interval == 0:
                # Append the frame to the screenshots list
                screenshots.append(frame)

            # Display the frame in the video player on the webpage
            cv2.imshow('Video', frame)
            # Check for the 'q' key to stop capturing
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video capture object
        video_capture.release()
        cv2.destroyAllWindows()

        # Process the screenshots (send to API, save to disk, etc.)
        for i, screenshot in enumerate(screenshots):
            # Convert the frame to JPEG format for sending to the API
            _, buffer = cv2.imencode('.jpg', screenshot)
            image_data = buffer.tobytes()

            # Prepare the multipart data with the captured image
            multipart_data = {
                'image': ('screenshot.jpg', image_data),
                'service': (None, 'anpr,mmr'),  # Other services as required
                'location': (None, 'HUN'),  # Change this based on user selection
                'maxreads': (None, 1),
            }

            # Send the request to the Adaptive Recognition API
            api_url = 'https://api.cloud.adaptiverecognition.com/vehicle/eur'
            api_key = '46c567c67bea7b5129710bac47e18417504586ed'  # Replace this with your actual API key
            headers = {'X-Api-Key': api_key}
            resp = requests.post(api_url, files=multipart_data, headers=headers)
            print("resp", resp.text)
            resp_dict = json.loads(resp.text)
            print("resp.dict", resp_dict)

        # Return response
        return JsonResponse({'message': 'Webcam processing completed successfully.'})

    return render(request, 'video_index.html')

