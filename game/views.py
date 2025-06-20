from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import AStarPath, DijkstraPath
import csv, heapq, json
from django import forms
from django.contrib.auth import logout
from django.utils import timezone
from django.views.decorators.http import require_POST
import datetime

# ---------- Utilities ----------
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.g = float("inf")
        self.f = float("inf")
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def get_neighbors(node, grid, ROWS, COLS, obstacles):
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    neighbors = []
    for dr, dc in directions:
        r, c = node.row + dr, node.col + dc
        if 0 <= r < ROWS and 0 <= c < COLS and (r, c) not in obstacles:
            neighbors.append(Node(r, c))
    return neighbors

def reconstruct_path(end):
    path = []
    current = end
    while current.parent:
        path.append((current.col, current.row))
        current = current.parent
    path.reverse()
    return path

# ---------- Forms ----------
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user

# ---------- Views ----------
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can log in now.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'game/register.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User account created. You can log in now.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'game/user_register.html', {'form': form})

def admin_register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Admin account created. You can log in now.")
            return redirect('login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'game/admin_register.html', {'form': form})

@login_required
def dashboard(request):
    context = {
        'is_admin': request.user.is_staff
    }
    return render(request, 'game/dashboard.html', context)

@login_required
def game_view(request):
    return render(request, 'game/game.html')

@login_required
def run_astar(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        grid = data['grid']
        start_col, start_row = data['start']
        goal_col, goal_row = data['goal']

        ROWS = len(grid)
        COLS = len(grid[0])
        obstacles = {(r, c) for r in range(ROWS) for c in range(COLS) if grid[r][c] == 'obstacle'}

        start = Node(start_row, start_col)
        goal = Node(goal_row, goal_col)
        start.g = 0
        start.f = heuristic(start, goal)

        open_set = []
        heapq.heappush(open_set, (start.f, start))
        visited = set()

        found = False
        while open_set:
            _, current = heapq.heappop(open_set)
            if (current.row, current.col) == (goal.row, goal.col):
                found = True
                goal.parent = current.parent
                break

            visited.add((current.row, current.col))
            for neighbor in get_neighbors(current, grid, ROWS, COLS, obstacles):
                if (neighbor.row, neighbor.col) in visited:
                    continue
                temp_g = current.g + 1
                if temp_g < neighbor.g:
                    neighbor.g = temp_g
                    neighbor.f = temp_g + heuristic(neighbor, goal)
                    neighbor.parent = current
                    heapq.heappush(open_set, (neighbor.f, neighbor))

        if found:
            path = reconstruct_path(current)
            AStarPath.objects.create(
                user=request.user,
                start_row=start_row, start_col=start_col,
                goal_row=goal_row, goal_col=goal_col,
                path=';'.join(map(str, path)),
                path_length=len(path)
            )
            return JsonResponse({'success': True, 'path': path})
        else:
            return JsonResponse({'success': False})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def run_dijkstra(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        grid = data['grid']
        start_col, start_row = data['start']
        goal_col, goal_row = data['goal']

        ROWS = len(grid)
        COLS = len(grid[0])
        obstacles = {(r, c) for r in range(ROWS) for c in range(COLS) if grid[r][c] == 'obstacle'}

        start = Node(start_row, start_col)
        goal = Node(goal_row, goal_col)
        start.g = 0

        open_set = []
        heapq.heappush(open_set, (start.g, start))
        visited = set()

        found = False
        while open_set:
            _, current = heapq.heappop(open_set)
            if (current.row, current.col) == (goal.row, goal.col):
                found = True
                goal.parent = current.parent
                break

            visited.add((current.row, current.col))
            for neighbor in get_neighbors(current, grid, ROWS, COLS, obstacles):
                if (neighbor.row, neighbor.col) in visited:
                    continue
                temp_g = current.g + 1
                if temp_g < neighbor.g:
                    neighbor.g = temp_g
                    neighbor.parent = current
                    heapq.heappush(open_set, (neighbor.g, neighbor))

        if found:
            path = reconstruct_path(current)
            DijkstraPath.objects.create(
                user=request.user,
                start_row=start_row, start_col=start_col,
                goal_row=goal_row, goal_col=goal_col,
                path=';'.join(map(str, path)),
                path_length=len(path)
            )
            return JsonResponse({'success': True, 'path': path})
        else:
            return JsonResponse({'success': False})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def show_db(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    filter_opt = request.GET.get('filter', 'all')
    now = timezone.now()
    if filter_opt == '1d':
        since = now - datetime.timedelta(days=1)
    elif filter_opt == '1w':
        since = now - datetime.timedelta(weeks=1)
    elif filter_opt == '1m':
        since = now - datetime.timedelta(days=30)
    else:
        since = None
    if since:
        astar = AStarPath.objects.filter(created_at__gte=since)
        dijkstra = DijkstraPath.objects.filter(created_at__gte=since)
    else:
        astar = AStarPath.objects.all()
        dijkstra = DijkstraPath.objects.all()
    return render(request, 'game/show_db.html', {
        'astar_paths': astar,
        'dijkstra_paths': dijkstra,
        'filter': filter_opt,
    })

import io
import zipfile

@login_required
def export_zip_csv(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    astar_qs = AStarPath.objects.all()
    dijkstra_qs = DijkstraPath.objects.all()

    if not astar_qs.exists() and not dijkstra_qs.exists():
        from django.contrib import messages
        messages.error(request, "Download cannot be done as there is no data.")
        return redirect('dashboard')

    # Create in-memory ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Create A* CSV
        astar_buffer = io.StringIO()
        astar_writer = csv.writer(astar_buffer)
        astar_writer.writerow(['User', 'Start', 'Goal', 'Path', 'Length', 'Created'])
        for p in astar_qs:
            astar_writer.writerow([
                p.user.username,
                f"({p.start_row},{p.start_col})",
                f"({p.goal_row},{p.goal_col})",
                p.path,
                p.path_length,
                p.created_at
            ])
        zip_file.writestr('astar_paths.csv', astar_buffer.getvalue())

        # Create Dijkstra CSV
        dijkstra_buffer = io.StringIO()
        dijkstra_writer = csv.writer(dijkstra_buffer)
        dijkstra_writer.writerow(['User', 'Start', 'Goal', 'Path', 'Length', 'Created'])
        for p in dijkstra_qs:
            dijkstra_writer.writerow([
                p.user.username,
                f"({p.start_row},{p.start_col})",
                f"({p.goal_row},{p.goal_col})",
                p.path,
                p.path_length,
                p.created_at
            ])
        zip_file.writestr('dijkstra_paths.csv', dijkstra_buffer.getvalue())

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="paths.zip"'
    return response

def home(request):
    return render(request, 'game/home.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'game/profile.html', {'user': user})

@login_required
def user_activity_data(request):
    user = request.user
    from django.utils import timezone
    import datetime
    now = timezone.now()
    # Get last 7 days (including today)
    days = [(now - datetime.timedelta(days=i)).date() for i in range(6, -1, -1)]
    day_labels = [d.strftime('%b %d') for d in days]  # e.g., ['Jun 10', 'Jun 11', ...]
    values = []
    for d in days:
        start_dt = timezone.make_aware(datetime.datetime.combine(d, datetime.time.min))
        end_dt = timezone.make_aware(datetime.datetime.combine(d, datetime.time.max))
        count_astar = AStarPath.objects.filter(user=user, created_at__gte=start_dt, created_at__lte=end_dt).count()
        count_dijkstra = DijkstraPath.objects.filter(user=user, created_at__gte=start_dt, created_at__lte=end_dt).count()
        values.append(count_astar + count_dijkstra)
    return JsonResponse({'labels': day_labels, 'values': values})

@login_required
def increment_games_played(request):
    if request.method == 'POST':
        user = request.user
        profile = getattr(user, 'profile', None)
        if profile:
            profile.games_played = getattr(profile, 'games_played', 0) + 1
            profile.save()
            return JsonResponse({'success': True, 'games_played': profile.games_played})
        return JsonResponse({'success': False, 'error': 'No profile found.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)

@login_required
@require_POST
def clear_path_data(request):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    option = request.POST.get('option', 'all')
    from django.utils import timezone
    import datetime
    now = timezone.now()
    if option == '1d':
        since = now - datetime.timedelta(days=1)
    elif option == '1w':
        since = now - datetime.timedelta(weeks=1)
    elif option == '1m':
        since = now - datetime.timedelta(days=30)
    else:
        since = None
    if since:
        astar_deleted = AStarPath.objects.filter(created_at__gte=since).delete()
        dijkstra_deleted = DijkstraPath.objects.filter(created_at__gte=since).delete()
    else:
        astar_deleted = AStarPath.objects.all().delete()
        dijkstra_deleted = DijkstraPath.objects.all().delete()
    return JsonResponse({'success': True})
