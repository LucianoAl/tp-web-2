import unittest
from electro_api import app

class TestElectrodomesticosAPI(unittest.TestCase):
    
    def setUp(self):
        # Configuramos el cliente de pruebas
        self.app = app.test_client()
        self.app.testing = True

    def test_1_listar_productos(self):
        respuesta = self.app.get('/productos')
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b'Heladera', respuesta.data)

    def test_2_agregar_al_carrito(self):
        # Agregamos la Heladera Samsung (ID 1)
        respuesta = self.app.post('/carrito/1')
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b'Agregado exitosamente', respuesta.data)

    def test_3_calcular_total(self):
        # Agregamos la Licuadora (ID 4) y calculamos el total
        self.app.post('/carrito/4') 
        respuesta = self.app.get('/carrito/total')
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b'El total de la compra es', respuesta.data)

    def test_4_eliminar_del_carrito(self):
        # Agregamos el Microondas (ID 3) y luego lo eliminamos
        self.app.post('/carrito/3')
        respuesta = self.app.delete('/carrito/Microondas BGH')
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b'Eliminado exitosamente', respuesta.data)

if __name__ == '__main__':
    unittest.main()