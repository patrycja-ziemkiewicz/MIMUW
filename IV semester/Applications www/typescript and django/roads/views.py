from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import BackgroundImage, Route, Point, GameBoard, Dot, GamePath
from django.urls import reverse
from .forms import RouteForm, PointForm, GameBoardForm
import json
from django.http import JsonResponse, HttpResponseBadRequest
import time
from django.http import StreamingHttpResponse
from .events import event_stream
from .scrapping import scrap, scrap_pages

@login_required
def index(request):
    routes = Route.objects.filter(user=request.user)
    boards = GameBoard.objects.filter(user=request.user)
    all_boards = GameBoard.objects.all()
    return render(request, 'index.html', {'routes': routes, 'boards': boards, 'all_boards': all_boards})

@login_required
def scrap_page(request):
    
    relative_url = reverse('roads:index') 
    full_url = request.build_absolute_uri(relative_url)
    sessionid = request.COOKIES.get('sessionid')
    if not sessionid:
        return HttpResponseBadRequest("Brak ciasteczka sesji – nie jesteś zalogowany?")
    
    n_links = scrap(full_url, sessionid)
    list = scrap_pages()
    
    return render(request, "scrap2.html", {'list': list})
    

@login_required
def create_game(request):
    if request.method == 'POST':
        form = GameBoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.user = request.user
            board.save()
            return redirect('roads:game_detail', board.id)
    else:
        form = GameBoardForm()

    return render(request, 'create_game.html', {'form': form})

@login_required
def game_detail(request, board_id):
    board = get_object_or_404(GameBoard, pk=board_id, user=request.user)
    form = GameBoardForm(instance=board)

    dots_qs = board.dots.all().values('row', 'col', 'color')
    dots_list = list(dots_qs) 

    return render(request, 'game_detail.html', {
        'board': board,
        'form': form,
        'initial_dots_json': json.dumps(dots_list),
    })
    
@login_required
def game_play(request, board_id):
    board = get_object_or_404(GameBoard, pk=board_id)

    dots_qs = board.dots.all().values('row', 'col', 'color')
    dots_list = list(dots_qs) 
    
    try:
        gp = GamePath.objects.get(user=request.user, board=board)
        paths_data = gp.data
    except GamePath.DoesNotExist:
        paths_data = {}

    return render(request, 'game_play.html', {
        'board': board,
        'initial_dots_json': json.dumps(dots_list),
        'initial_paths_json': json.dumps(paths_data),
    })
    
@login_required
def save_path(request, board_id):
    if request.method != 'POST' or request.content_type != 'application/json':
        return HttpResponseBadRequest('Invalid request')
    board = get_object_or_404(GameBoard, pk=board_id)
    payload = json.loads(request.body)
    paths = payload.get('paths')
    if not isinstance(paths, dict):
        return HttpResponseBadRequest('Invalid payload')

    GamePath.objects.update_or_create(
        user=request.user,
        board=board,
        defaults={ 'data': paths },
    )
    return JsonResponse({'status': 'ok'})

@login_required
def route_detail(request, route_id):
    route = get_object_or_404(Route, pk=route_id, user=request.user)
    points = route.points.all()

    if request.method == 'POST':
        form = PointForm(request.POST)
        if form.is_valid():
            point = form.save(commit=False)
            point.route = route
            point.order = points.count() + 1
            point.save()
            return redirect('roads:route_detail', route.id)
    else:
        form = PointForm()

    return render(request, 'route_detail.html', {
        'route': route,
        'points': points,
        'form': form
    })
    
@login_required
def delete_point(request, pt_id):
    pt = get_object_or_404(Point, pk=pt_id, route__user=request.user)
    route = pt.route
    pt.delete()
    for idx, p in enumerate(route.points.order_by('order'), start=1):
        if p.order != idx:
            p.order = idx
            p.save()
    return redirect('roads:route_detail', route.id)

@login_required
def delete_route(request, route_id):
    if request.method == 'POST':
        route = get_object_or_404(Route, pk=route_id, user=request.user)
        route.delete()
    return redirect('roads:index')

@login_required
def delete_board(request, board_id):
    if request.method == 'POST':
        board = get_object_or_404(GameBoard, pk=board_id, user=request.user)
        board.delete()
    return redirect('roads:index')

@login_required
def create_route(request):
    bg_id = request.session.get('selected_bg_id')
    background = None
    if bg_id:
        background = get_object_or_404(BackgroundImage, pk=bg_id)

    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            route.user = request.user
            route.background = background
            route.save()
            return redirect('roads:route_detail', route.id)
    else:
        form = RouteForm(initial={'name': 'Nowa trasa'})

    return render(request, 'create_route.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('roads:login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def select_background(request):
    bg = BackgroundImage.objects.all()
    try:
        selected_bg = bg.get(pk=request.POST["bg"])
    except (KeyError, BackgroundImage.DoesNotExist):
        return render(
            request, 
            'choose_background.html', 
            {
                'backgrounds': bg,
                'error_message' :'Nie wybrales tla!' 
             },
        ) 
    else:
        request.session['selected_bg_id'] = selected_bg.id
        return redirect('roads:create_route')
    
@login_required
def background(request):
    bg = BackgroundImage.objects.all()
    return render(request, 'choose_background.html', {'backgrounds': bg})

@login_required
def save_board(request, board_id):
    if request.method != 'POST' or request.content_type != 'application/json':
        return HttpResponseBadRequest('Invalid request')
    board = get_object_or_404(GameBoard, pk=board_id, user=request.user)
    try:
        data = json.loads(request.body)
        board.rows = data['rows']
        board.cols = data['cols']
        board.save()
        board.dots.all().delete()
        for dot in data['dots']:
            Dot.objects.create(
                board=board,
                row=dot['row'],
                col=dot['col'],
                color=dot['color']
            )
        board.game_paths.all().delete()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
def sse_notifications(request):

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')

    response['Cache-Control'] = 'no-cache'
    return response
