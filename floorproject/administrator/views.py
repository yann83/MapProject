# floorproject/administrator/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser
from .forms import UserCreationForm, UserChangeForm
import json
import os
from django.conf import settings
from django.http import JsonResponse
from .decorators import role_required  # Importez le décorateur

def administrator_index(request):
    return render(request, 'administrator/index.html')

def administrator_cartes(request):
    return render(request, 'administrator/cartes.html')

def administrator_plans(request):
    return render(request, 'administrator/plans.html')

# Fonction pour afficher la liste des utilisateurs
@login_required
@role_required(['admin'])
def administrator_users(request):
    # Récupérer tous les utilisateurs
    users = CustomUser.objects.all()
    return render(request, 'administrator/users.html', {'users': users})

# Fonction pour ajouter un nouvel utilisateur
@login_required
@role_required(['admin'])  # Seul l'admin peut ajouter des utilisateurs
def administrator_add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administrator-users')
    else:
        form = UserCreationForm()
    return render(request, 'administrator/user_form.html', {'form': form, 'action': 'Ajouter'})


# Fonction pour modifier un utilisateur existant
@login_required
@role_required(['admin'])  # Seul l'admin peut modifier des utilisateurs
def administrator_edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    # Autoriser les utilisateurs à modifier leur propre profil
    if request.user.id != user.id and request.user.role != 'admin':
        messages.error(request, "Vous ne pouvez pas modifier cet utilisateur.")
        return redirect('administrator-users')

    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('administrator-users')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'administrator/user_form.html', {'form': form, 'action': 'Modifier'})

# Fonction pour supprimer un utilisateur
@login_required
@role_required(['admin'])  # Seul l'admin peut supprimer des utilisateurs
def administrator_delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('administrator-users')
    return render(request, 'administrator/delete_user.html', {'user': user})

# Nouvelle vue pour l'édition de la carte globale
@login_required
@role_required(['admin', 'carte'])
def administrator_edit_carte(request):
    # Chemin vers le fichier JSON
    json_file_path = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'json', 'global_map.json')

    # Si c'est une requête POST, nous mettons à jour le fichier JSON
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            # Récupérer les données JSON envoyées par la requête AJAX
            data = json.loads(request.body)
            action = data.get('action')

            # Lire le fichier JSON existant
            with open(json_file_path, 'r') as file:
                map_data = json.load(file)

            # Traiter l'action demandée
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

            # Écrire les données mises à jour dans le fichier JSON
            with open(json_file_path, 'w') as file:
                json.dump(map_data, file, indent=2)

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

        # Pour une requête GET, nous chargeons les données actuelles du JSON
    try:
        json_file_path = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'json', 'global_map.json')
        with open(json_file_path, 'r') as file:
            map_data = json.load(file)
    except:
        # Si le fichier n'existe pas ou est invalide, nous créons un modèle de base
        map_data = {
            "setView": {"lat": 43.12568, "lng": 5.94334, "zoom": 18},
            "icons": {},
            "markers": {}
        }

        # Récupérer la liste des fichiers d'images de marqueurs
    markers_dir = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'markers')
    marker_files = []
    if os.path.exists(markers_dir):
        marker_files = [f for f in os.listdir(markers_dir) if
                        f.startswith('marker-') and f.endswith(('.png', '.jpg', '.jpeg'))]

    # Rendu du template avec les données
    return render(request, 'administrator/edit_carte.html', {
        'map_data': json.dumps(map_data),
        'marker_files': marker_files
    })


# Nouvelle vue pour l'édition des plans
@login_required
@role_required(['admin', 'plan'])
def administrator_edit_plans(request):
    # Chemin vers le fichier JSON
    json_file_path = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'json', 'maps.json')

    # Si c'est une requête POST, nous mettons à jour le fichier JSON
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            # Récupérer les données JSON envoyées par la requête AJAX
            data = json.loads(request.body)
            action = data.get('action')

            # Lire le fichier JSON existant
            with open(json_file_path, 'r') as file:
                map_data = json.load(file)

            # Traiter l'action demandée
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

                    # Vérifier si le marqueur existe déjà pour le mettre à jour
                    updated = False
                    if marker_action == 'update':
                        for i, marker_group in enumerate(map_data['markers']):
                            if marker_id in marker_group:
                                map_data['markers'][i][marker_id] = data.get('marker_data')
                                updated = True
                                break

                    # Si c'est un nouveau marqueur ou qu'il n'a pas été trouvé pour mise à jour
                    if not updated:
                        # Créer un nouvel objet pour ce marqueur
                        new_marker = {marker_id: data.get('marker_data')}
                        map_data['markers'].append(new_marker)

                elif marker_action == 'delete':
                    # Trouver et supprimer le marqueur
                    for i, marker_group in enumerate(map_data['markers']):
                        if marker_id in marker_group:
                            del map_data['markers'][i][marker_id]
                            # Si le groupe est vide, le supprimer
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
                    # Réordonner les plans
                    new_order = data.get('new_order')
                    if new_order and 'plans' in map_data:
                        ordered_plans = {}
                        for plan_id in new_order:
                            if plan_id in map_data['plans']:
                                ordered_plans[plan_id] = map_data['plans'][plan_id]
                        map_data['plans'] = ordered_plans

            # Écrire les données mises à jour dans le fichier JSON
            with open(json_file_path, 'w') as file:
                json.dump(map_data, file, indent=2)

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # Pour une requête GET, nous chargeons simplement les données actuelles du JSON
    try:
        with open(json_file_path, 'r') as file:
            map_data = json.load(file)
    except:
        # Si le fichier n'existe pas ou est invalide, nous créons un modèle de base
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

    # Récupérer la liste des fichiers d'images dans le dossier plans
    plans_dir = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'plans')
    plan_files = []
    if os.path.exists(plans_dir):
        plan_files = [f for f in os.listdir(plans_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Récupérer la liste des fichiers d'images de marqueurs
    markers_dir = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'markers')
    marker_files = []
    if os.path.exists(markers_dir):
        marker_files = [f for f in os.listdir(markers_dir) if
                        f.startswith('marker-') and f.endswith(('.png', '.jpg', '.jpeg'))]

    # Rendu du template avec les données
    return render(request, 'administrator/edit_plans.html', {
        'map_data': json.dumps(map_data),
        'plan_files': plan_files,
        'marker_files': marker_files  # Ajout des fichiers de marqueurs
    })


@login_required
@role_required(['admin'])
def administrator_upload(request):
    """
    Vue pour gérer l'upload et la suppression des fichiers.
    Permet de téléverser des images avec préfixe selon la catégorie :
    - 'marker-' pour les images de marqueurs (stockées dans /static/markers)
    - 'plan-' pour les plans d'étage (stockées dans /static/plans)
    """
    # Initialiser les listes pour stocker les fichiers existants
    marker_files = []
    plan_files = []

    # Récupérer les chemins des dossiers
    img_dir = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'markers')
    plans_dir = os.path.join(settings.BASE_DIR, 'floorproject', 'static', 'plans')

    # Récupérer la liste des fichiers existants
    if os.path.exists(img_dir):
        marker_files = [f for f in os.listdir(img_dir) if
                        f.startswith('marker-') and f.endswith(('.png', '.jpg', '.jpeg'))]

    if os.path.exists(plans_dir):
        plan_files = [f for f in os.listdir(plans_dir) if
                      f.startswith('plan-') and f.endswith(('.png', '.jpg', '.jpeg'))]

    # Traitement des requêtes POST (upload et suppression)
    if request.method == 'POST':
        # Si c'est une requête AJAX pour la suppression
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'delete' in request.POST:
            try:
                filename = request.POST.get('filename')
                category = request.POST.get('category')

                if category == 'marker':
                    file_path = os.path.join(img_dir, filename)
                else:  # plan
                    file_path = os.path.join(plans_dir, filename)

                # Vérifier si le fichier existe avant de le supprimer
                if os.path.exists(file_path):
                    os.remove(file_path)
                    return JsonResponse({'status': 'success', 'message': f'Fichier {filename} supprimé avec succès.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Fichier non trouvé.'})

            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})

        # Si c'est une requête d'upload normal
        elif 'image' in request.FILES:
            try:
                uploaded_file = request.FILES['image']
                category = request.POST.get('category')

                # Vérifier l'extension du fichier
                if not uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    return render(request, 'administrator/upload.html', {
                        'marker_files': marker_files,
                        'plan_files': plan_files,
                        'error': 'Seuls les fichiers PNG, JPG et JPEG sont acceptés.'
                    })

                # Déterminer le préfixe et le chemin selon la catégorie
                if category == 'marker':
                    prefix = 'marker-'
                    target_dir = img_dir
                else:  # plan
                    prefix = 'plan-'
                    target_dir = plans_dir

                # S'assurer que le dossier cible existe
                os.makedirs(target_dir, exist_ok=True)

                # Créer le nom de fichier avec le préfixe
                filename = prefix + uploaded_file.name
                file_path = os.path.join(target_dir, filename)

                # Sauvegarder le fichier
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                # Mettre à jour les listes de fichiers
                if category == 'marker':
                    marker_files.append(filename)
                else:
                    plan_files.append(filename)

                return render(request, 'administrator/upload.html', {
                    'marker_files': marker_files,
                    'plan_files': plan_files,
                    'success': f'Fichier {filename} téléversé avec succès.'
                })

            except Exception as e:
                return render(request, 'administrator/upload.html', {
                    'marker_files': marker_files,
                    'plan_files': plan_files,
                    'error': f'Erreur lors du téléversement: {str(e)}'
                })

    # Requête GET - afficher simplement la page
    return render(request, 'administrator/upload.html', {
        'marker_files': marker_files,
        'plan_files': plan_files
    })