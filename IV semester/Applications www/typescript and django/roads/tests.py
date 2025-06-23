from django.contrib.auth.models import User
from .models import BackgroundImage, Route, Point
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

class ViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user1', password='pass')
        cls.other = User.objects.create_user(username='user2', password='pass')
        cls.bg = BackgroundImage.objects.create(name='BG', image='backgrounds/bg.png')
        cls.route = Route.objects.create(user=cls.user, background=cls.bg, name='R1')
        cls.point = Point.objects.create(route=cls.route, x=10, y=20, order=1)

    def setUp(self):
        self.client = Client()

    def test_index_redirect_if_not_logged_in(self):
        url = reverse('roads:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('roads:login')))
    
    def test_index_shows_empty_message(self):
        self.client.login(username='user2', password='pass')
        url = reverse('roads:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Brak tras.')

    def test_index_shows_user_routes(self):
        self.client.login(username='user1', password='pass')
        url = reverse('roads:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        detail_url = reverse('roads:route_detail', args=[self.route.id])
        self.assertContains(response, detail_url)
        self.assertContains(response, 'R1')
    
    def test_route_detail_requires_login(self):
        url = reverse('roads:route_detail', args=[self.route.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('roads:login')))
    
    def test_route_detail_not_owner_404(self):
        self.client.login(username='user2', password='pass')
        url = reverse('roads:route_detail', args=[self.route.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_route_detail_shows_points_and_form(self):
        self.client.login(username='user1', password='pass')
        url = reverse('roads:route_detail', args=[self.route.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '(10.0, 20.0)')
        self.assertContains(response, 'X')
        self.assertContains(response, 'Y')

    def test_add_point_via_post(self):
        self.client.login(username='user1', password='pass')
        url = reverse('roads:route_detail', args=[self.route.id])
        data = {'x': 30, 'y': 40}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        points = Point.objects.filter(route=self.route).order_by('order')
        self.assertEqual(points.count(), 2)
        response = self.client.get(url)
        self.assertContains(response, '(30.0, 40.0)')

    def test_delete_point(self):
        self.client.login(username='user1', password='pass')
        url = reverse('roads:delete_point', args=[self.point.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Point.objects.filter(pk=self.point.id).exists())
        
    def test_delete_point_not_exist(self):
        self.client.login(username='user1', password='pass')
        url = reverse('roads:delete_point', args=[self.point.id + 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)   

    def test_create_route(self):
        self.client.login(username='user1', password='pass')
        url = reverse('roads:create_route')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {'name' : 'nowa trasa'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Route.objects.filter(user=self.user, name='nowa trasa').exists())

    def test_signup_view(self):
        url = reverse('roads:signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {'username': 'user3', 'password1': 'complexpw123', 'password2': 'complexpw123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='user3').exists())

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.bg = BackgroundImage.objects.create(name='Test Background', image='backgrounds/test.png')

    def test_create_background_image(self):
        bg = BackgroundImage.objects.get(pk=self.bg.pk)
        self.assertEqual(bg.name, 'Test Background')
        self.assertTrue(bg.image.name.endswith('test.png'))
        self.assertIsNotNone(bg.uploaded_at)

    def test_create_route(self):
        route = Route.objects.create(user=self.user, background=self.bg, name='Route 1')
        self.assertEqual(route.user, self.user)
        self.assertEqual(route.background, self.bg)
        self.assertEqual(route.name, 'Route 1')
        self.assertIsNotNone(route.created_at)
        self.assertIn(route, self.user.routes.all())
        self.assertIn(route, self.bg.routes.all())

    def test_create_point(self):
        route = Route.objects.create(user=self.user, background=self.bg, name='test route')
        p1 = Point.objects.create(route=route, x=10.5, y=20.5, order=1)
        p2 = Point.objects.create(route=route, x=30.0, y=40.0, order=2)
        self.assertEqual(p1.route, route)
        self.assertEqual(p1.order, 1)
        self.assertEqual(p2.order, 2)
        points = list(route.points.all())
        self.assertEqual(points, [p1, p2])
        self.assertEqual('test route (testuser)', str(route))
        self.assertEqual('Point 1 (test route)', str(p1))

class APIRouteAndPointTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='user1', password='pass')
        cls.token1 = Token.objects.create(user=cls.user1)
        cls.user2 = User.objects.create_user(username='user2', password='pass')
        cls.token2 = Token.objects.create(user=cls.user2)
        cls.bg = BackgroundImage.objects.create(name='BG', image='backgrounds/bg.png')
        cls.route1 = Route.objects.create(user=cls.user1, background=cls.bg, name='Route1')
        cls.point1 = Point.objects.create(route=cls.route1, x=1.0, y=2.0, order=1)

    def setUp(self):
        self.client1 = APIClient()
        self.client1.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        self.client2 = APIClient()
        self.client2.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')

    def test_list_routes_requires_auth(self):
        client = APIClient()
        resp = client.get(reverse('roads:trasy-list'))
        self.assertEqual(resp.status_code, 401)

    def test_list_routes_only_user1(self):
        resp = self.client1.get(reverse('roads:trasy-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0]['name'], 'Route1')

    def test_create_route(self):
        data = {'name': 'NewRoute', 'background': self.bg.id}
        resp = self.client1.post(reverse('roads:trasy-list'), data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Route.objects.filter(user=self.user1, name='NewRoute').exists())

    def test_retrieve_route_detail(self):
        url = reverse('roads:trasy-detail', args=[self.route1.id])
        resp = self.client1.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['id'], self.route1.id)

    def test_delete_route(self):
        url = reverse('roads:trasy-detail', args=[self.route1.id])
        resp = self.client1.delete(url)
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(Route.objects.filter(pk=self.route1.id).exists())

    def test_route_access_forbidden_for_other(self):
        url = reverse('roads:trasy-detail', args=[self.route1.id])
        resp = self.client2.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_list_points(self):
        url = reverse('roads:route-punkty-list', kwargs={'route_pk': self.route1.id})
        resp = self.client1.get(url)
        self.assertEqual(resp.status_code, 200)
        pts = resp.json()
        self.assertEqual(len(pts), 1)
        self.assertEqual(pts[0]['x'], 1.0)

    def test_add_point(self):
        url = reverse('roads:route-punkty-list', kwargs={'route_pk': self.route1.id})
        data = {'x': 5.5, 'y': 6.5}
        resp = self.client1.post(url, data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Point.objects.filter(route=self.route1).count(), 2)

    def test_delete_point(self):
        url = reverse('roads:route-punkty-detail', kwargs={'route_pk': self.route1.id, 'pk': self.point1.id})
        resp = self.client1.delete(url)
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(Point.objects.filter(pk=self.point1.id).exists())

    def test_point_access_forbidden_for_other(self):
        url = reverse('roads:route-punkty-detail', kwargs={'route_pk': self.route1.id, 'pk': self.point1.id})
        resp = self.client2.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_add_point_invalid_data(self):
        url = reverse('roads:route-punkty-list', kwargs={'route_pk': self.route1.id})
        data = {'x': 'not-a-number'}
        resp = self.client1.post(url, data, format='json')
        self.assertEqual(resp.status_code, 400)


