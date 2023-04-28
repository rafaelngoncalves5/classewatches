from django.test import TestCase

from .models import User, Produto, password_token

from datetime import datetime

from django.utils import timezone

ps = password_token.objects.get(data_cr = '2023-04-28 00:41:59.750972')
ps_data = ps.data_cr

# Create your tests here.
class UserTests(TestCase):

    def test_input_users(self):
        new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        return new_user
    
    def test_input_users_2(self):
        new_user = User.objects.create_user(123, '123@123', '123')
        return new_user
    
    def test_input_product(self):
        # Eu suponho que o SQLite elimina vários erros que aconteceriam em SGBDs de tipagem forte
        new_product = Produto.objects.create(id_produto=5, titulo='abc123456', descricao='fndkfdkf', preco=10.90, quantidade=20)
        self.assertIs(new_product.id_produto, 5)
        return new_product
    
class TokenTests(TestCase):
    def test_token_input(self):
        self.assertLess(ps_data, timezone.now())