# floorproject/administrator/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser
from .forms import UserCreationForm, UserChangeForm
import json
import os
from django.conf import settings
from django.http import JsonResponse
from .decorators import role_required  # Import the decorator

def administrator_index(request):
    return render(request, 'administrator/index.html')

def administrator_cartes(request):
    return render(request, 'administrator/cartes.html')

def administrator_plans(request):
    return render(request, 'administrator/plans.html')

# Function to display the list of users
@login_required
@role_required(['admin'])
def administrator_users(request):
    # Recover all users
    users = CustomUser.objects.all()
    return render(request, 'administrator/users.html', {'users': users})

# Function to add a new user
@login_required
@role_required(['admin'])  # Only admin can add users
def administrator_add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administrator-users')
    else:
        form = UserCreationForm()
    return render(request, 'administrator/user_form.html', {'form': form, 'action': 'Ajouter'})


# Function to modify an existing user
@login_required
@role_required(['admin'])  # Only admin can add users
def administrator_edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    # Allow users to edit their own profile
    if request.user.id != user.id and request.user.role != 'admin':
        messages.error(request, "You cannot edit this user.")
        return redirect('administrator-users')

    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('administrator-users')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'administrator/user_form.html', {'form': form, 'action': 'Modifier'})

# Function to delete a user
@login_required
@role_required(['admin'])  # Only admin can delete users
def administrator_delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('administrator-users')
    return render(request, 'administrator/delete_user.html', {'user': user})

# New view for editing the global map
@login_required
@role_required(['admin', 'carte'])
def administrator_edit_carte(request):
    # Path to the JSON file
    json_file_path = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'json', 'global_map.json')

    # If it is a POST request, we update the JSON file
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            # Retrieve JSON data sent by AJAX request
            data = json.loads(request.body)
            action = data.get('action')

            # Lire le fichier JSON existant
            with open(json_file_path, 'r') as file:
                map_data = json.load(file)

            # Process the requested action
            if action == 'update_setview':
                map_data['setView'] = data.get('setView')
            elif action == 'crud_icon':
                icon_action = data.get('icon_action')
                icon_name = data.get('icon_name')

                if icon_action == 'create' or icon_action == 'update':
                    if 'icons' not in map_data:
                        map_data['icons'] = {}
                    map_data['icons'][icon_name] = data.get('icon_data')
                elif icon_action == 'delete':
                    if 'icons' in map_data and icon_name in map_data['icons']:
                        del map_data['icons'][icon_name]
            elif action == 'crud_marker':
                marker_action = data.get('marker_action')
                marker_id = data.get('marker_id')

                if marker_action == 'create' or marker_action == 'update':
                    if 'markers' not in map_data:
                        map_data['markers'] = {}
                    map_data['markers'][marker_id] = data.get('marker_data')
                elif marker_action == 'delete':
                    if 'markers' in map_data and marker_id in map_data['markers']:
                        del map_data['markers'][marker_id]

            # Write updated data to JSON file
            with open(json_file_path, 'w') as file:
                json.dump(map_data, file, indent=2)

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

        # For a GET request, we load the current data from the JSON
    try:
        json_file_path = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'json', 'global_map.json')
        with open(json_file_path, 'r') as file:
            map_data = json.load(file)
    except:
        # If the file does not exist or is invalid, we create a base template
        map_data = {
            "setView": {"lat": 43.12568, "lng": 5.94334, "zoom": 18},
            "icons": {},
            "markers": {}
        }

        # Retrieve the list of marker image files
    markers_dir = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'markers')
    marker_files = []
    if os.path.exists(markers_dir):
        marker_files = [f for f in os.listdir(markers_dir) if
                        f.startswith('marker-') and f.endswith(('.png', '.jpg', '.jpeg'))]

    # Rendering the template with the data
    return render(request, 'administrator/edit_carte.html', {
        'map_data': json.dumps(map_data),
        'marker_files': marker_files
    })


# New view for editing plans
@login_required
@role_required(['admin', 'plan'])
def administrator_edit_plans(request):
    # Path to the JSON file
    json_file_path = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'json', 'maps.json')

    # Si c'est une requête POST, nous mettons à jour le fichier JSON
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            # If it is a POST request, we update the JSON file
            data = json.loads(request.body)
            action = data.get('action')

            # Read existing JSON file
            with open(json_file_path, 'r') as file:
                map_data = json.load(file)

            # Process the requested action
            if action == 'update_bounds_map':
                map_data['bounds'] = data.get('bounds')
                map_data['map'] = data.get('map')
            elif action == 'crud_icon':
                icon_action = data.get('icon_action')
                icon_name = data.get('icon_name')

                if icon_action == 'create' or icon_action == 'update':
                    if 'icons' not in map_data:
                        map_data['icons'] = {}
                    map_data['icons'][icon_name] = data.get('icon_data')
                elif icon_action == 'delete':
                    if 'icons' in map_data and icon_name in map_data['icons']:
                        del map_data['icons'][icon_name]
            elif action == 'crud_marker':
                marker_action = data.get('marker_action')
                marker_id = data.get('marker_id')

                if marker_action == 'create' or marker_action == 'update':
                    if 'markers' not in map_data:
                        map_data['markers'] = []

                    # If this is a new marker or it was not found for update
                    updated = False
                    if marker_action == 'update':
                        for i, marker_group in enumerate(map_data['markers']):
                            if marker_id in marker_group:
                                map_data['markers'][i][marker_id] = data.get('marker_data')
                                updated = True
                                break

                    # If this is a new marker or it was not found for update
                    if not updated:
                        # Create a new object for this marker
                        new_marker = {marker_id: data.get('marker_data')}
                        map_data['markers'].append(new_marker)

                elif marker_action == 'delete':
                    # Find and delete the marker
                    for i, marker_group in enumerate(map_data['markers']):
                        if marker_id in marker_group:
                            del map_data['markers'][i][marker_id]
                            # If the group is empty, delete it
                            if not map_data['markers'][i]:
                                map_data['markers'].pop(i)
                            break
            elif action == 'crud_plan':
                plan_action = data.get('plan_action')
                plan_id = data.get('plan_id')

                if plan_action == 'create' or plan_action == 'update':
                    if 'plans' not in map_data:
                        map_data['plans'] = {}
                    map_data['plans'][plan_id] = data.get('plan_data')
                elif plan_action == 'delete':
                    if 'plans' in map_data and plan_id in map_data['plans']:
                        del map_data['plans'][plan_id]
                elif plan_action == 'reorder':
                    # Reorder the plans
                    new_order = data.get('new_order')
                    if new_order and 'plans' in map_data:
                        ordered_plans = {}
                        for plan_id in new_order:
                            if plan_id in map_data['plans']:
                                ordered_plans[plan_id] = map_data['plans'][plan_id]
                        map_data['plans'] = ordered_plans

            # Write updated data to JSON file
            with open(json_file_path, 'w') as file:
                json.dump(map_data, file, indent=2)

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # For a GET request, we simply load the current data from the JSON
    try:
        with open(json_file_path, 'r') as file:
            map_data = json.load(file)
    except:
        # If the file does not exist or is invalid, we create a base template
        map_data = {
            "bounds": [[0, 0], [2339, 3309]],
            "map": {
                "minZoom": -5,
                "zoomDelta": 0.25,
                "zoomSnap": 0,
                "layers": "",
                "xy": [1100, 1600],
                "z": -2
            },
            "icons": {},
            "plans": {},
            "markers": []
        }

    # Retrieve the list of image files in the plans folder
    plans_dir = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'plans')
    plan_files = []
    if os.path.exists(plans_dir):
        plan_files = [f for f in os.listdir(plans_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Retrieve the list of marker image files
    markers_dir = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'markers')
    marker_files = []
    if os.path.exists(markers_dir):
        marker_files = [f for f in os.listdir(markers_dir) if
                        f.startswith('marker-') and f.endswith(('.png', '.jpg', '.jpeg'))]

    # Rendering the template with the data
    return render(request, 'administrator/edit_plans.html', {
        'map_data': json.dumps(map_data),
        'plan_files': plan_files,
        'marker_files': marker_files  # Adding marker files
    })


@login_required
@role_required(['admin'])
def administrator_upload(request):
    """
    View to manage file uploads and deletions.
    Allows you to upload images with a prefix based on category:
    - 'marker-' for marker images (stored in /static/markers)
    - 'plan-' for floor plans (stored in /static/plans)
    """
    # Initialize lists to store existing files
    marker_files = []
    plan_files = []

    # Retrieve folder paths
    img_dir = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'markers')
    plans_dir = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'plans')

    # Retrieve the list of existing files
    if os.path.exists(img_dir):
        marker_files = [f for f in os.listdir(img_dir) if
                        f.startswith('marker-') and f.endswith(('.png', '.jpg', '.jpeg'))]

    if os.path.exists(plans_dir):
        plan_files = [f for f in os.listdir(plans_dir) if
                      f.startswith('plan-') and f.endswith(('.png', '.jpg', '.jpeg'))]

    # Processing POST requests (upload and delete)
    if request.method == 'POST':
        # If it is an AJAX request for deletion
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'delete' in request.POST:
            try:
                filename = request.POST.get('filename')
                category = request.POST.get('category')

                if category == 'marker':
                    file_path = os.path.join(img_dir, filename)
                else:  # floor plan
                    file_path = os.path.join(plans_dir, filename)

                # Check if the file exists before deleting it
                if os.path.exists(file_path):
                    os.remove(file_path)
                    return JsonResponse({'status': 'success', 'message': f'File {filename} successfully deleted.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'File not found.'})

            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})

        # If it is a normal upload request
        elif 'image' in request.FILES:
            try:
                uploaded_file = request.FILES['image']
                category = request.POST.get('category')

                # Check the file extension
                if not uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    return render(request, 'administrator/upload.html', {
                        'marker_files': marker_files,
                        'plan_files': plan_files,
                        'error': 'Only PNG, JPG and JPEG files are accepted.'
                    })

                # Determine prefix and path according to category
                if category == 'marker':
                    prefix = 'marker-'
                    target_dir = img_dir
                else:  # floor plan
                    prefix = 'plan-'
                    target_dir = plans_dir

                # Ensure the target folder exists
                os.makedirs(target_dir, exist_ok=True)

                # Create file name with prefix
                filename = prefix + uploaded_file.name
                file_path = os.path.join(target_dir, filename)

                # Save the file
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                # Update file lists
                if category == 'marker':
                    marker_files.append(filename)
                else:
                    plan_files.append(filename)

                return render(request, 'administrator/upload.html', {
                    'marker_files': marker_files,
                    'plan_files': plan_files,
                    'success': f'File {filename} uploaded successfully.'
                })

            except Exception as e:
                return render(request, 'administrator/upload.html', {
                    'marker_files': marker_files,
                    'plan_files': plan_files,
                    'error': f'Error while uploading: {str(e)}'
                })

    # GET request - simply display the page
    return render(request, 'administrator/upload.html', {
        'marker_files': marker_files,
        'plan_files': plan_files
    })